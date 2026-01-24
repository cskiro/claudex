# Sensei Agent

Automated skill improvement pipeline that uses Claude to fix skills based on evaluation feedback.

## Overview

The Sensei Agent is triggered when a GitHub issue receives the `agent-ready` label. It:

1. Reads evaluation feedback from the issue body
2. Analyzes the target skill
3. Makes targeted improvements (trigger phrases, disambiguation, etc.)
4. Creates a PR with the changes

## Setup

### 1. Configure ANTHROPIC_API_KEY Secret

1. Go to your repository: `github.com/<owner>/claudex`
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Configure:
   - **Name**: `ANTHROPIC_API_KEY`
   - **Value**: Your API key from [console.anthropic.com](https://console.anthropic.com) (starts with `sk-ant-`)
5. Click **Add secret**

### 2. Verify Workflow is Enabled

The workflow file `.github/workflows/run-sensei-agent.yml` should be automatically enabled when merged to main.

## Usage

### Triggering the Agent

1. **Create an issue** with evaluation feedback

   The issue body must contain the skill name in this format:
   ```
   **Skill**: `skill-name`
   ```

   Example issue body:
   ```markdown
   ## Evaluation Results

   **Skill**: `accessibility-audit`

   ### Issues Found

   - False positive rate: 45% (target: <20%)
   - Trigger phrase "check accessibility" conflicts with manual accessibility checks
   - Missing disambiguation for automated vs manual audits

   ### Suggested Fixes

   - Add "WCAG" to trigger phrases for specificity
   - Add "NOT for" section to clarify manual checks
   ```

2. **Add the `agent-ready` label** to trigger the workflow

3. **Wait for completion** - the agent will:
   - Create a branch: `fix/{skill-name}/{issue-number}`
   - Make targeted improvements
   - Create a PR linked to the issue
   - Update labels (`agent-ready` → `agent-completed`)

### Canceling a Run

Remove the `agent-ready` label before the workflow starts to cancel.

## Agent Capabilities

The agent can:

| Tool | Description | Restrictions |
|------|-------------|--------------|
| `read_file` | Read any file in the repository | None |
| `write_file` | Write/modify files | **Only `skills/*` directory** |
| `list_files` | List directory contents | None |
| `git_commit` | Create git commits | Conventional commit format |
| `complete` | Signal completion | Returns summary |

## Safety Mechanisms

1. **Path Restriction**: Writes only allowed to `skills/*` directory
2. **Max Turns**: Agent stops after 20 turns to prevent runaway
3. **Label Control**: Remove `agent-ready` to cancel
4. **Dry-Run Mode**: Test without creating changes

## Dry Run Testing

Test the agent locally without making changes:

```bash
# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Run in dry-run mode
python scripts/automation/sensei_agent.py \
  --issue 123 \
  --repo owner/claudex \
  --skill accessibility-audit \
  --dry-run
```

## Troubleshooting

### Agent Failed to Start

**Check ANTHROPIC_API_KEY secret**:
- Verify the secret exists in repository settings
- Ensure the key is valid and not expired
- Keys start with `sk-ant-`

### "Could not extract skill name"

**Issue body format incorrect**:
- Must contain: `**Skill**: \`skill-name\``
- Skill name must match a directory in `skills/`

### Agent Completed but No Changes

**Review the workflow logs**:
- Agent may have determined no changes were needed
- Evaluation feedback may be unclear
- Check if skill files are readable

### PR Creation Failed

**Check GitHub token permissions**:
- Workflow needs `contents: write` and `pull-requests: write`
- These are configured in the workflow file

## Architecture

```
GitHub Issue (with evaluation feedback)
         │
         ▼ (agent-ready label)
┌─────────────────────────────────────┐
│  GitHub Actions Workflow            │
│  .github/workflows/run-sensei-agent.yml
│  - Extracts skill name              │
│  - Creates feature branch           │
│  - Runs Python agent                │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  sensei_agent.py                    │
│  - Claude API (Sonnet)              │
│  - Tool execution loop              │
│  - Path-restricted writes           │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Pull Request                       │
│  - Linked to issue                  │
│  - Validation checklist             │
│  - Auto-labels applied              │
└─────────────────────────────────────┘
```

## Related

- [Skill Validation](../../scripts/validate-skills.py) - Run after agent changes
- [Marketplace Validation](../../scripts/validate-marketplace.py) - Verify marketplace integrity
