#!/usr/bin/env python3
"""
Sensei Agent - Automated Skill Improvement for Claudex

This agent reads evaluation feedback from GitHub issues and makes targeted
improvements to Claude Code skills based on that feedback.

Security:
- API key read from ANTHROPIC_API_KEY environment variable only
- File writes restricted to skills/* directory
- No sensitive data in logs

Usage:
    python scripts/automation/sensei_agent.py --issue 123 --repo owner/repo --skill skill-name
    python scripts/automation/sensei_agent.py --issue 123 --repo owner/repo --skill skill-name --dry-run

Environment Variables:
    ANTHROPIC_API_KEY - Required. Anthropic API key for Claude access.
    GITHUB_TOKEN - Optional. Used for gh CLI authentication.
"""

import argparse
import fnmatch
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


# Safety limits
MAX_TURNS = 20
ALLOWED_PATHS = ["skills/*", "skills/**/*"]

# Tool definitions for Claude
TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file from the repository.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file relative to repository root"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file. Only allowed for files in skills/ directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the file relative to repository root (must be in skills/)"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                }
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "list_files",
        "description": "List files in a directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to the directory relative to repository root"
                },
                "pattern": {
                    "type": "string",
                    "description": "Optional glob pattern to filter files (e.g., '*.md')"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "git_commit",
        "description": "Create a git commit with staged changes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Commit message following conventional commits format"
                }
            },
            "required": ["message"]
        }
    },
    {
        "name": "complete",
        "description": "Signal that the task is complete with a summary of changes made.",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Summary of changes made to the skill"
                }
            },
            "required": ["summary"]
        }
    }
]


def is_path_allowed(path: str) -> bool:
    """Check if a path is allowed for writing."""
    for pattern in ALLOWED_PATHS:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def get_issue_body(issue_number: int, repo: str) -> str:
    """Fetch issue body using gh CLI."""
    result = subprocess.run(
        ["gh", "issue", "view", str(issue_number), "--repo", repo, "--json", "body", "-q", ".body"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to fetch issue: {result.stderr}")
    return result.stdout.strip()


def execute_tool(name: str, args: dict, repo_root: Path, dry_run: bool = False) -> dict:
    """Execute a tool and return the result."""
    try:
        if name == "read_file":
            path = repo_root / args["path"]
            if not path.exists():
                return {"error": f"File not found: {args['path']}"}
            content = path.read_text()
            return {"content": content, "path": args["path"]}

        elif name == "write_file":
            path = args["path"]
            if not is_path_allowed(path):
                return {"error": f"Write not allowed outside skills/ directory: {path}"}

            full_path = repo_root / path

            if dry_run:
                print(f"[DRY RUN] Would write to: {path}")
                print(f"[DRY RUN] Content length: {len(args['content'])} chars")
                return {"success": True, "path": path, "dry_run": True}

            # Ensure parent directory exists
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(args["content"])

            # Stage the file
            subprocess.run(["git", "add", path], cwd=repo_root, check=True)

            return {"success": True, "path": path}

        elif name == "list_files":
            path = repo_root / args["path"]
            if not path.exists():
                return {"error": f"Directory not found: {args['path']}"}
            if not path.is_dir():
                return {"error": f"Not a directory: {args['path']}"}

            pattern = args.get("pattern", "*")
            files = []
            for item in path.iterdir():
                if fnmatch.fnmatch(item.name, pattern):
                    files.append({
                        "name": item.name,
                        "type": "directory" if item.is_dir() else "file"
                    })

            return {"files": sorted(files, key=lambda x: (x["type"] != "directory", x["name"]))}

        elif name == "git_commit":
            if dry_run:
                print(f"[DRY RUN] Would commit with message: {args['message']}")
                return {"success": True, "dry_run": True}

            result = subprocess.run(
                ["git", "commit", "-m", args["message"]],
                cwd=repo_root,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                # Check if there's nothing to commit
                if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                    return {"success": True, "message": "Nothing to commit"}
                return {"error": result.stderr}

            return {"success": True, "message": args["message"]}

        elif name == "complete":
            return {"complete": True, "summary": args["summary"]}

        else:
            return {"error": f"Unknown tool: {name}"}

    except Exception as e:
        return {"error": str(e)}


def run_agent(
    issue_number: int,
    repo: str,
    skill_name: str,
    dry_run: bool = False
) -> bool:
    """Run the Sensei agent to improve a skill based on issue feedback."""

    # Get API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        return False

    # Import anthropic here to fail gracefully if not installed
    try:
        import anthropic
    except ImportError:
        print("Error: anthropic package not installed. Run: pip install anthropic")
        return False

    # Initialize client
    client = anthropic.Anthropic(api_key=api_key)

    # Get repository root
    repo_root = Path.cwd()

    # Fetch issue body
    print(f"Fetching issue #{issue_number} from {repo}...")
    try:
        issue_body = get_issue_body(issue_number, repo)
    except Exception as e:
        print(f"Error fetching issue: {e}")
        return False

    # Verify skill exists
    skill_path = repo_root / "skills" / skill_name
    if not skill_path.exists():
        print(f"Error: Skill directory not found: skills/{skill_name}")
        return False

    # System prompt
    system_prompt = f"""You are Sensei, an expert at improving Claude Code skills based on evaluation feedback.

Your task is to improve the skill "{skill_name}" based on the evaluation feedback provided in the GitHub issue.

## Context

This is a skill in the claudex marketplace. Skills are defined by:
- SKILL.md: The main agent manifest with frontmatter (name, description) and workflow instructions
- README.md: User-facing documentation
- CHANGELOG.md: Version history

## Your Goals

1. Read the current skill files to understand the skill
2. Analyze the evaluation feedback in the issue
3. Make targeted improvements to address the feedback, such as:
   - Improving trigger phrases for better detection
   - Adding disambiguation to reduce false positives
   - Clarifying when the skill should NOT be used
   - Improving the workflow instructions
4. Update the CHANGELOG.md with your changes
5. Create a commit with your changes

## Guidelines

- Make minimal, targeted changes - don't rewrite the entire skill
- Focus on the specific issues identified in the feedback
- Maintain the existing style and structure
- Use conventional commit format: fix(skill-name): description

## Available Tools

- read_file: Read file contents
- write_file: Write to files (only in skills/ directory)
- list_files: List directory contents
- git_commit: Create a commit
- complete: Signal completion with summary

When you're done making changes, use the 'complete' tool with a summary of what you changed.
"""

    # Initial user message with issue content
    user_message = f"""Please improve the skill "{skill_name}" based on this evaluation feedback:

## Issue #{issue_number}

{issue_body}

Start by reading the current skill files in skills/{skill_name}/, then make targeted improvements based on the feedback."""

    messages = [{"role": "user", "content": user_message}]

    print(f"Starting agent for skill: {skill_name}")
    if dry_run:
        print("[DRY RUN MODE - No changes will be made]")

    # Agent loop
    for turn in range(MAX_TURNS):
        print(f"\n--- Turn {turn + 1}/{MAX_TURNS} ---")

        # Call Claude
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            tools=TOOLS,
            messages=messages
        )

        # Process response
        assistant_content = response.content
        messages.append({"role": "assistant", "content": assistant_content})

        # Check for tool use
        tool_uses = [block for block in assistant_content if block.type == "tool_use"]

        if not tool_uses:
            # No tool use - check for text response
            text_blocks = [block for block in assistant_content if block.type == "text"]
            if text_blocks:
                print(f"Agent response: {text_blocks[0].text[:200]}...")
            break

        # Execute tools and collect results
        tool_results = []
        completed = False

        for tool_use in tool_uses:
            print(f"Tool: {tool_use.name}")
            result = execute_tool(tool_use.name, tool_use.input, repo_root, dry_run)

            # Check for completion
            if tool_use.name == "complete":
                completed = True
                print(f"\nAgent completed: {result.get('summary', 'No summary')}")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": json.dumps(result)
            })

        messages.append({"role": "user", "content": tool_results})

        if completed:
            return True

    print(f"\nAgent stopped after {MAX_TURNS} turns without completion")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Sensei Agent - Automated skill improvement based on evaluation feedback"
    )
    parser.add_argument(
        "--issue",
        type=int,
        required=True,
        help="GitHub issue number containing evaluation feedback"
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="GitHub repository (owner/repo format)"
    )
    parser.add_argument(
        "--skill",
        type=str,
        required=True,
        help="Name of the skill to improve"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without making actual changes"
    )

    args = parser.parse_args()

    success = run_agent(
        issue_number=args.issue,
        repo=args.repo,
        skill_name=args.skill,
        dry_run=args.dry_run
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
