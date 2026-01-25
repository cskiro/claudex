#!/usr/bin/env python3
"""
Conversation Processor for Claude Code Insights

Parses JSONL conversation files from ~/.claude/projects/, extracts metadata,
and stores in SQLite for fast querying. Supports incremental processing.
"""

import json
import sqlite3
import base64
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import click
import re


@dataclass
class ConversationMetadata:
    """Structured conversation metadata"""
    id: str
    project_path: str
    timestamp: datetime
    message_count: int
    user_messages: int
    assistant_messages: int
    files_read: List[str]
    files_written: List[str]
    files_edited: List[str]
    tools_used: List[str]
    topics: List[str]
    first_user_message: str
    last_assistant_message: str
    conversation_hash: str
    file_size_bytes: int
    processed_at: datetime


class ConversationProcessor:
    """Processes Claude Code conversation JSONL files"""

    def __init__(self, db_path: Path, verbose: bool = False):
        self.db_path = db_path
        self.verbose = verbose
        self.conn = None
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database with schema"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

        # Create tables
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                project_path TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                message_count INTEGER NOT NULL,
                user_messages INTEGER NOT NULL,
                assistant_messages INTEGER NOT NULL,
                files_read TEXT,  -- JSON array
                files_written TEXT,  -- JSON array
                files_edited TEXT,  -- JSON array
                tools_used TEXT,  -- JSON array
                topics TEXT,  -- JSON array
                first_user_message TEXT,
                last_assistant_message TEXT,
                conversation_hash TEXT UNIQUE NOT NULL,
                file_size_bytes INTEGER NOT NULL,
                processed_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_timestamp ON conversations(timestamp);
            CREATE INDEX IF NOT EXISTS idx_project ON conversations(project_path);
            CREATE INDEX IF NOT EXISTS idx_processed ON conversations(processed_at);

            CREATE TABLE IF NOT EXISTS file_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                file_path TEXT NOT NULL,
                interaction_type TEXT NOT NULL,  -- read, write, edit
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            );

            CREATE INDEX IF NOT EXISTS idx_file_path ON file_interactions(file_path);
            CREATE INDEX IF NOT EXISTS idx_conversation ON file_interactions(conversation_id);

            CREATE TABLE IF NOT EXISTS tool_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                usage_count INTEGER NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            );

            CREATE INDEX IF NOT EXISTS idx_tool_name ON tool_usage(tool_name);

            CREATE TABLE IF NOT EXISTS processing_state (
                file_path TEXT PRIMARY KEY,
                last_modified TEXT NOT NULL,
                last_processed TEXT NOT NULL,
                file_hash TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def _log(self, message: str):
        """Log if verbose mode is enabled"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of file for change detection"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _needs_processing(self, file_path: Path, reindex: bool = False) -> bool:
        """Check if file needs (re)processing"""
        if reindex:
            return True

        file_stat = file_path.stat()
        file_hash = self._compute_file_hash(file_path)

        cursor = self.conn.execute(
            "SELECT last_modified, file_hash FROM processing_state WHERE file_path = ?",
            (str(file_path),)
        )
        row = cursor.fetchone()

        if not row:
            return True  # Never processed

        last_modified, stored_hash = row
        return stored_hash != file_hash  # File changed

    def _update_processing_state(self, file_path: Path):
        """Update processing state for file"""
        file_hash = self._compute_file_hash(file_path)
        last_modified = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()

        self.conn.execute("""
            INSERT OR REPLACE INTO processing_state (file_path, last_modified, last_processed, file_hash)
            VALUES (?, ?, ?, ?)
        """, (str(file_path), last_modified, datetime.now().isoformat(), file_hash))

    def _parse_jsonl_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse JSONL file with base64-encoded content"""
        messages = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    if line.strip():
                        data = json.loads(line)
                        messages.append(data)
                except json.JSONDecodeError as e:
                    self._log(f"Warning: Failed to parse line {line_num} in {file_path.name}: {e}")
        return messages

    def _extract_tool_uses(self, content: str) -> List[str]:
        """Extract tool names from assistant messages"""
        tools = []
        # Look for tool use patterns in content
        tool_patterns = [
            r'"name":\s*"([A-Z][a-zA-Z]+)"',  # JSON tool calls
            r'<tool>([A-Z][a-zA-Z]+)</tool>',  # XML tool calls
        ]

        for pattern in tool_patterns:
            matches = re.findall(pattern, content)
            tools.extend(matches)

        return list(set(tools))  # Unique tools

    def _extract_file_paths(self, content: str) -> Dict[str, List[str]]:
        """Extract file paths and their interaction types from content"""
        files = {
            'read': [],
            'written': [],
            'edited': []
        }

        # Patterns for file operations
        read_patterns = [
            r'Reading\s+(.+\.(?:py|js|ts|tsx|jsx|md|json|yaml|yml))',
            r'Read\s+file:\s*(.+)',
            r'"file_path":\s*"([^"]+)"',  # Tool parameters
        ]

        write_patterns = [
            r'Writing\s+(.+\.(?:py|js|ts|tsx|jsx|md|json|yaml|yml))',
            r'Created\s+file:\s*(.+)',
            r'Write\s+(.+)',
        ]

        edit_patterns = [
            r'Editing\s+(.+\.(?:py|js|ts|tsx|jsx|md|json|yaml|yml))',
            r'Modified\s+file:\s*(.+)',
            r'Edit\s+(.+)',
        ]

        for pattern in read_patterns:
            files['read'].extend(re.findall(pattern, content, re.IGNORECASE))
        for pattern in write_patterns:
            files['written'].extend(re.findall(pattern, content, re.IGNORECASE))
        for pattern in edit_patterns:
            files['edited'].extend(re.findall(pattern, content, re.IGNORECASE))

        # Deduplicate and clean
        for key in files:
            files[key] = list(set(path.strip() for path in files[key]))

        return files

    def _extract_topics(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract topic keywords from conversation"""
        # Combine first user message and some assistant responses
        text = ""
        user_count = 0
        for msg in messages:
            msg_type = msg.get('type', '')

            # Handle event-stream format
            if msg_type == 'user':
                message_dict = msg.get('message', {})
                content = message_dict.get('content', '') if isinstance(message_dict, dict) else ''

                # Handle content that's a list (content blocks)
                if isinstance(content, list):
                    message_content = ' '.join(
                        block.get('text', '') if isinstance(block, dict) and block.get('type') == 'text' else ''
                        for block in content
                    )
                else:
                    message_content = content

                if message_content:
                    text += message_content + " "
                    user_count += 1
                    if user_count >= 3:  # Only use first few user messages
                        break
            elif msg_type == 'assistant' and user_count < 3:
                # Also include some assistant responses for context
                message_dict = msg.get('message', {})
                content = message_dict.get('content', '') if isinstance(message_dict, dict) else ''

                # Handle content that's a list (content blocks)
                if isinstance(content, list):
                    message_content = ' '.join(
                        block.get('text', '') if isinstance(block, dict) and block.get('type') == 'text' else ''
                        for block in content
                    )
                else:
                    message_content = content

                if message_content:
                    text += message_content[:200] + " "  # Just a snippet

        # Extract common programming keywords
        keywords = []
        common_topics = [
            'authentication', 'auth', 'login', 'jwt', 'oauth',
            'testing', 'test', 'unit test', 'integration test',
            'bug', 'fix', 'error', 'issue', 'debug',
            'performance', 'optimization', 'optimize', 'slow',
            'refactor', 'refactoring', 'cleanup',
            'feature', 'implement', 'add', 'create',
            'database', 'sql', 'query', 'schema',
            'api', 'endpoint', 'rest', 'graphql',
            'typescript', 'javascript', 'react', 'node',
            'css', 'style', 'styling', 'tailwind',
            'security', 'vulnerability', 'xss', 'csrf',
            'deploy', 'deployment', 'ci/cd', 'docker',
        ]

        text_lower = text.lower()
        for topic in common_topics:
            if topic in text_lower:
                keywords.append(topic)

        return list(set(keywords))[:10]  # Max 10 topics

    def _process_conversation(self, file_path: Path, messages: List[Dict[str, Any]]) -> ConversationMetadata:
        """Extract metadata from parsed conversation"""
        # Generate conversation ID from filename
        conv_id = file_path.stem

        # Count messages by role
        user_messages = 0
        assistant_messages = 0
        first_user_msg = ""
        last_assistant_msg = ""
        all_tools = []
        all_files = {'read': [], 'written': [], 'edited': []}

        for msg in messages:
            msg_type = msg.get('type', '')

            # Handle event-stream format
            if msg_type == 'user':
                user_messages += 1
                message_dict = msg.get('message', {})
                content = message_dict.get('content', '') if isinstance(message_dict, dict) else ''

                # Handle content that's a list (content blocks)
                if isinstance(content, list):
                    message_content = ' '.join(
                        block.get('text', '') if isinstance(block, dict) and block.get('type') == 'text' else ''
                        for block in content
                    )
                else:
                    message_content = content

                if not first_user_msg and message_content:
                    first_user_msg = message_content[:500]  # First 500 chars

            elif msg_type == 'assistant':
                assistant_messages += 1
                message_dict = msg.get('message', {})
                content = message_dict.get('content', '') if isinstance(message_dict, dict) else ''

                # Handle content that's a list (content blocks)
                if isinstance(content, list):
                    message_content = ' '.join(
                        block.get('text', '') if isinstance(block, dict) and block.get('type') == 'text' else ''
                        for block in content
                    )
                    # Also extract tools from content blocks
                    for block in content:
                        if isinstance(block, dict) and block.get('type') == 'tool_use':
                            tool_name = block.get('name', '')
                            if tool_name:
                                all_tools.append(tool_name)
                else:
                    message_content = content

                if message_content:
                    last_assistant_msg = message_content[:500]

                    # Extract tools and files from assistant messages
                    tools = self._extract_tool_uses(message_content)
                    all_tools.extend(tools)

                    files = self._extract_file_paths(message_content)
                    for key in all_files:
                        all_files[key].extend(files[key])

        # Deduplicate
        all_tools = list(set(all_tools))
        for key in all_files:
            all_files[key] = list(set(all_files[key]))

        # Extract topics
        topics = self._extract_topics(messages)

        # File stats
        file_stat = file_path.stat()

        # Compute conversation hash
        conv_hash = self._compute_file_hash(file_path)

        # Extract timestamp (from filename or file mtime)
        try:
            # Try to get timestamp from file modification time
            timestamp = datetime.fromtimestamp(file_stat.st_mtime)
        except Exception:
            timestamp = datetime.now()

        return ConversationMetadata(
            id=conv_id,
            project_path=str(file_path.parent),
            timestamp=timestamp,
            message_count=len(messages),
            user_messages=user_messages,
            assistant_messages=assistant_messages,
            files_read=all_files['read'],
            files_written=all_files['written'],
            files_edited=all_files['edited'],
            tools_used=all_tools,
            topics=topics,
            first_user_message=first_user_msg,
            last_assistant_message=last_assistant_msg,
            conversation_hash=conv_hash,
            file_size_bytes=file_stat.st_size,
            processed_at=datetime.now()
        )

    def _store_conversation(self, metadata: ConversationMetadata):
        """Store conversation metadata in database"""
        # Store main conversation record
        self.conn.execute("""
            INSERT OR REPLACE INTO conversations
            (id, project_path, timestamp, message_count, user_messages, assistant_messages,
             files_read, files_written, files_edited, tools_used, topics,
             first_user_message, last_assistant_message, conversation_hash,
             file_size_bytes, processed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            metadata.id,
            metadata.project_path,
            metadata.timestamp.isoformat(),
            metadata.message_count,
            metadata.user_messages,
            metadata.assistant_messages,
            json.dumps(metadata.files_read),
            json.dumps(metadata.files_written),
            json.dumps(metadata.files_edited),
            json.dumps(metadata.tools_used),
            json.dumps(metadata.topics),
            metadata.first_user_message,
            metadata.last_assistant_message,
            metadata.conversation_hash,
            metadata.file_size_bytes,
            metadata.processed_at.isoformat()
        ))

        # Store file interactions
        self.conn.execute(
            "DELETE FROM file_interactions WHERE conversation_id = ?",
            (metadata.id,)
        )
        for file_path in metadata.files_read:
            self.conn.execute(
                "INSERT INTO file_interactions (conversation_id, file_path, interaction_type) VALUES (?, ?, ?)",
                (metadata.id, file_path, 'read')
            )
        for file_path in metadata.files_written:
            self.conn.execute(
                "INSERT INTO file_interactions (conversation_id, file_path, interaction_type) VALUES (?, ?, ?)",
                (metadata.id, file_path, 'write')
            )
        for file_path in metadata.files_edited:
            self.conn.execute(
                "INSERT INTO file_interactions (conversation_id, file_path, interaction_type) VALUES (?, ?, ?)",
                (metadata.id, file_path, 'edit')
            )

        # Store tool usage
        self.conn.execute(
            "DELETE FROM tool_usage WHERE conversation_id = ?",
            (metadata.id,)
        )
        for tool_name in metadata.tools_used:
            self.conn.execute(
                "INSERT INTO tool_usage (conversation_id, tool_name, usage_count) VALUES (?, ?, ?)",
                (metadata.id, tool_name, 1)
            )

    def process_file(self, file_path: Path, reindex: bool = False) -> bool:
        """Process a single conversation file"""
        if not self._needs_processing(file_path, reindex):
            self._log(f"Skipping {file_path.name} (already processed)")
            return False

        self._log(f"Processing {file_path.name}...")

        try:
            # Parse JSONL
            messages = self._parse_jsonl_file(file_path)

            if not messages:
                self._log(f"Warning: No messages found in {file_path.name}")
                return False

            # Extract metadata
            metadata = self._process_conversation(file_path, messages)

            # Store in database
            self._store_conversation(metadata)

            # Update processing state
            self._update_processing_state(file_path)

            self.conn.commit()

            self._log(f"✓ Processed {file_path.name}: {metadata.message_count} messages, "
                     f"{metadata.user_messages} user, {metadata.assistant_messages} assistant")

            return True

        except Exception as e:
            self._log(f"Error processing {file_path.name}: {e}")
            import traceback
            if self.verbose:
                traceback.print_exc()
            return False

    def process_project(self, project_name: str, reindex: bool = False) -> int:
        """Process all conversations for a project"""
        # Find conversation files
        claude_projects = Path.home() / ".claude" / "projects"

        if not claude_projects.exists():
            self._log(f"Error: {claude_projects} does not exist")
            return 0

        # Find project directory (may be encoded)
        project_dirs = list(claude_projects.glob(f"*{project_name}*"))

        if not project_dirs:
            self._log(f"Error: No project directory found matching '{project_name}'")
            return 0

        if len(project_dirs) > 1:
            self._log(f"Warning: Multiple project directories found, using {project_dirs[0].name}")

        project_dir = project_dirs[0]
        self._log(f"Processing conversations from {project_dir}")

        # Find all JSONL files
        jsonl_files = list(project_dir.glob("*.jsonl"))

        if not jsonl_files:
            self._log(f"No conversation files found in {project_dir}")
            return 0

        self._log(f"Found {len(jsonl_files)} conversation files")

        # Process each file
        processed_count = 0
        for jsonl_file in jsonl_files:
            if self.process_file(jsonl_file, reindex):
                processed_count += 1

        self._log(f"\nProcessed {processed_count}/{len(jsonl_files)} conversations")
        return processed_count

    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        cursor = self.conn.execute("""
            SELECT
                COUNT(*) as total_conversations,
                SUM(message_count) as total_messages,
                SUM(user_messages) as total_user_messages,
                SUM(assistant_messages) as total_assistant_messages,
                MIN(timestamp) as earliest_conversation,
                MAX(timestamp) as latest_conversation
            FROM conversations
        """)
        row = cursor.fetchone()

        stats = {
            'total_conversations': row['total_conversations'],
            'total_messages': row['total_messages'],
            'total_user_messages': row['total_user_messages'],
            'total_assistant_messages': row['total_assistant_messages'],
            'earliest_conversation': row['earliest_conversation'],
            'latest_conversation': row['latest_conversation']
        }

        # Top files
        cursor = self.conn.execute("""
            SELECT file_path, COUNT(*) as interaction_count
            FROM file_interactions
            GROUP BY file_path
            ORDER BY interaction_count DESC
            LIMIT 10
        """)
        stats['top_files'] = [
            {'file': row['file_path'], 'count': row['interaction_count']}
            for row in cursor.fetchall()
        ]

        # Top tools
        cursor = self.conn.execute("""
            SELECT tool_name, SUM(usage_count) as total_usage
            FROM tool_usage
            GROUP BY tool_name
            ORDER BY total_usage DESC
            LIMIT 10
        """)
        stats['top_tools'] = [
            {'tool': row['tool_name'], 'count': row['total_usage']}
            for row in cursor.fetchall()
        ]

        return stats

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


@click.command()
@click.option('--project-name', default='annex', help='Project name to process')
@click.option('--db-path', type=click.Path(), default='.claude/skills/cc-insights/.processed/conversations.db',
              help='SQLite database path')
@click.option('--reindex', is_flag=True, help='Reprocess all conversations (ignore cache)')
@click.option('--verbose', is_flag=True, help='Show detailed processing logs')
@click.option('--stats', is_flag=True, help='Show statistics after processing')
def main(project_name: str, db_path: str, reindex: bool, verbose: bool, stats: bool):
    """Process Claude Code conversations and store metadata"""
    db_path = Path(db_path)

    processor = ConversationProcessor(db_path, verbose=verbose)

    try:
        # Process conversations
        count = processor.process_project(project_name, reindex=reindex)

        print(f"\n✓ Processed {count} conversations")

        if stats:
            print("\n=== Statistics ===")
            stats_data = processor.get_stats()
            print(f"Total conversations: {stats_data['total_conversations']}")
            print(f"Total messages: {stats_data['total_messages']}")
            print(f"User messages: {stats_data['total_user_messages']}")
            print(f"Assistant messages: {stats_data['total_assistant_messages']}")
            print(f"Date range: {stats_data['earliest_conversation']} to {stats_data['latest_conversation']}")

            print("\nTop 10 Files:")
            for item in stats_data['top_files']:
                print(f"  {item['file']}: {item['count']} interactions")

            print("\nTop 10 Tools:")
            for item in stats_data['top_tools']:
                print(f"  {item['tool']}: {item['count']} uses")

    finally:
        processor.close()


if __name__ == '__main__':
    main()
