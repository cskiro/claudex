#!/usr/bin/env python3
"""
Search Interface for Claude Code Insights

Provides unified search across conversations using semantic (RAG) and keyword search.
Supports filtering by dates, files, and output formatting.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import click

try:
    from rag_indexer import RAGIndexer
except ImportError:
    print("Error: Cannot import rag_indexer. Ensure it's in the same directory.")
    exit(1)


class ConversationSearch:
    """Unified search interface for conversations"""

    def __init__(self, db_path: Path, embeddings_dir: Path, verbose: bool = False):
        self.db_path = db_path
        self.embeddings_dir = embeddings_dir
        self.verbose = verbose

        # Initialize RAG indexer for semantic search
        self.indexer = RAGIndexer(db_path, embeddings_dir, verbose=verbose)

        # Separate SQLite connection for metadata queries
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row

    def _log(self, message: str):
        """Log if verbose mode is enabled"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def _get_conversation_details(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get full conversation details from SQLite"""
        cursor = self.conn.execute("""
            SELECT * FROM conversations WHERE id = ?
        """, (conversation_id,))

        row = cursor.fetchone()
        if not row:
            return None

        return {
            'id': row['id'],
            'timestamp': row['timestamp'],
            'message_count': row['message_count'],
            'user_messages': row['user_messages'],
            'assistant_messages': row['assistant_messages'],
            'files_read': json.loads(row['files_read']) if row['files_read'] else [],
            'files_written': json.loads(row['files_written']) if row['files_written'] else [],
            'files_edited': json.loads(row['files_edited']) if row['files_edited'] else [],
            'tools_used': json.loads(row['tools_used']) if row['tools_used'] else [],
            'topics': json.loads(row['topics']) if row['topics'] else [],
            'first_user_message': row['first_user_message'],
            'last_assistant_message': row['last_assistant_message']
        }

    def semantic_search(
        self,
        query: str,
        limit: int = 10,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        file_pattern: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Perform RAG-based semantic search"""
        self._log(f"Semantic search: '{query}'")

        # TODO: Add ChromaDB filters for dates/files when supported
        results = self.indexer.search(query, n_results=limit * 2)  # Get extra for filtering

        # Enrich with full conversation details
        enriched_results = []
        for result in results:
            details = self._get_conversation_details(result['id'])
            if details:
                # Apply post-search filters
                if date_from and details['timestamp'] < date_from:
                    continue
                if date_to and details['timestamp'] > date_to:
                    continue
                if file_pattern:
                    all_files = details['files_read'] + details['files_written'] + details['files_edited']
                    if not any(file_pattern in f for f in all_files):
                        continue

                enriched_results.append({
                    **result,
                    **details
                })

            if len(enriched_results) >= limit:
                break

        return enriched_results

    def keyword_search(
        self,
        query: str,
        limit: int = 10,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        file_pattern: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Perform SQL-based keyword search"""
        self._log(f"Keyword search: '{query}'")

        # Build SQL query
        conditions = [
            "(first_user_message LIKE ? OR last_assistant_message LIKE ? OR topics LIKE ?)"
        ]
        params = [f"%{query}%", f"%{query}%", f"%{query}%"]

        if date_from:
            conditions.append("timestamp >= ?")
            params.append(date_from)

        if date_to:
            conditions.append("timestamp <= ?")
            params.append(date_to)

        if file_pattern:
            conditions.append(
                "(files_read LIKE ? OR files_written LIKE ? OR files_edited LIKE ?)"
            )
            params.extend([f"%{file_pattern}%"] * 3)

        where_clause = " AND ".join(conditions)

        cursor = self.conn.execute(f"""
            SELECT * FROM conversations
            WHERE {where_clause}
            ORDER BY timestamp DESC
            LIMIT ?
        """, params + [limit])

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row['id'],
                'timestamp': row['timestamp'],
                'message_count': row['message_count'],
                'user_messages': row['user_messages'],
                'assistant_messages': row['assistant_messages'],
                'files_read': json.loads(row['files_read']) if row['files_read'] else [],
                'files_written': json.loads(row['files_written']) if row['files_written'] else [],
                'files_edited': json.loads(row['files_edited']) if row['files_edited'] else [],
                'tools_used': json.loads(row['tools_used']) if row['tools_used'] else [],
                'topics': json.loads(row['topics']) if row['topics'] else [],
                'first_user_message': row['first_user_message'],
                'last_assistant_message': row['last_assistant_message']
            })

        return results

    def search_by_file(self, file_pattern: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Find all conversations that touched specific files"""
        self._log(f"File search: '{file_pattern}'")

        cursor = self.conn.execute("""
            SELECT DISTINCT c.*
            FROM conversations c
            JOIN file_interactions fi ON c.id = fi.conversation_id
            WHERE fi.file_path LIKE ?
            ORDER BY c.timestamp DESC
            LIMIT ?
        """, (f"%{file_pattern}%", limit))

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row['id'],
                'timestamp': row['timestamp'],
                'message_count': row['message_count'],
                'files_read': json.loads(row['files_read']) if row['files_read'] else [],
                'files_written': json.loads(row['files_written']) if row['files_written'] else [],
                'files_edited': json.loads(row['files_edited']) if row['files_edited'] else [],
                'tools_used': json.loads(row['tools_used']) if row['tools_used'] else [],
                'topics': json.loads(row['topics']) if row['topics'] else [],
                'first_user_message': row['first_user_message']
            })

        return results

    def search_by_tool(self, tool_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Find conversations using specific tools"""
        self._log(f"Tool search: '{tool_name}'")

        cursor = self.conn.execute("""
            SELECT DISTINCT c.*
            FROM conversations c
            JOIN tool_usage tu ON c.id = tu.conversation_id
            WHERE tu.tool_name LIKE ?
            ORDER BY c.timestamp DESC
            LIMIT ?
        """, (f"%{tool_name}%", limit))

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row['id'],
                'timestamp': row['timestamp'],
                'message_count': row['message_count'],
                'tools_used': json.loads(row['tools_used']) if row['tools_used'] else [],
                'topics': json.loads(row['topics']) if row['topics'] else [],
                'first_user_message': row['first_user_message']
            })

        return results

    def format_results(self, results: List[Dict[str, Any]], format: str = 'text') -> str:
        """Format search results"""
        if format == 'json':
            return json.dumps(results, indent=2)

        elif format == 'markdown':
            output = [f"# Search Results ({len(results)} found)\n"]

            for i, result in enumerate(results, 1):
                timestamp = datetime.fromisoformat(result['timestamp']).strftime('%b %d, %Y %H:%M')
                similarity = f"[Similarity: {result['similarity']:.3f}] " if 'similarity' in result else ""

                output.append(f"## {i}. {similarity}{result['id']}")
                output.append(f"**Date:** {timestamp}")
                output.append(f"**Messages:** {result.get('message_count', 'N/A')}")

                if result.get('topics'):
                    output.append(f"**Topics:** {', '.join(result['topics'])}")

                all_files = (result.get('files_read', []) +
                           result.get('files_written', []) +
                           result.get('files_edited', []))
                if all_files:
                    output.append(f"**Files:** {', '.join(all_files[:5])}")
                    if len(all_files) > 5:
                        output.append(f"  _(and {len(all_files) - 5} more)_")

                if result.get('tools_used'):
                    output.append(f"**Tools:** {', '.join(result['tools_used'][:5])}")

                if result.get('first_user_message'):
                    msg = result['first_user_message'][:200]
                    output.append(f"\n**Snippet:** {msg}...")

                output.append("")

            return "\n".join(output)

        else:  # text format
            output = [f"\nFound {len(results)} conversations:\n"]

            for i, result in enumerate(results, 1):
                timestamp = datetime.fromisoformat(result['timestamp']).strftime('%b %d, %Y %H:%M')
                similarity = f"[Similarity: {result['similarity']:.3f}] " if 'similarity' in result else ""

                output.append(f"{i}. {similarity}{result['id']}")
                output.append(f"   Date: {timestamp}")
                output.append(f"   Messages: {result.get('message_count', 'N/A')}")

                if result.get('topics'):
                    output.append(f"   Topics: {', '.join(result['topics'][:3])}")

                all_files = (result.get('files_read', []) +
                           result.get('files_written', []) +
                           result.get('files_edited', []))
                if all_files:
                    output.append(f"   Files: {', '.join(all_files[:3])}")

                if result.get('first_user_message'):
                    msg = result['first_user_message'][:150].replace('\n', ' ')
                    output.append(f"   Preview: {msg}...")

                output.append("")

            return "\n".join(output)

    def close(self):
        """Close connections"""
        self.indexer.close()
        if self.conn:
            self.conn.close()


@click.command()
@click.argument('query', required=False)
@click.option('--db-path', type=click.Path(), default='.claude/skills/cc-insights/.processed/conversations.db',
              help='SQLite database path')
@click.option('--embeddings-dir', type=click.Path(), default='.claude/skills/cc-insights/.processed/embeddings',
              help='ChromaDB embeddings directory')
@click.option('--semantic/--keyword', default=True, help='Use semantic (RAG) or keyword search')
@click.option('--file', type=str, help='Filter by file pattern')
@click.option('--tool', type=str, help='Search by tool name')
@click.option('--date-from', type=str, help='Start date (ISO format)')
@click.option('--date-to', type=str, help='End date (ISO format)')
@click.option('--limit', default=10, help='Maximum results')
@click.option('--format', type=click.Choice(['text', 'json', 'markdown']), default='text', help='Output format')
@click.option('--verbose', is_flag=True, help='Show detailed logs')
def main(query: Optional[str], db_path: str, embeddings_dir: str, semantic: bool, file: Optional[str],
         tool: Optional[str], date_from: Optional[str], date_to: Optional[str], limit: int, format: str, verbose: bool):
    """Search Claude Code conversations

    Examples:

      # Semantic search
      python search-conversations.py "authentication bugs"

      # Keyword search
      python search-conversations.py "React optimization" --keyword

      # Filter by file
      python search-conversations.py "testing" --file "src/components"

      # Search by tool
      python search-conversations.py --tool "Write"

      # Date range
      python search-conversations.py "refactoring" --date-from 2025-10-01

      # JSON output
      python search-conversations.py "deployment" --format json
    """
    db_path = Path(db_path)
    embeddings_dir = Path(embeddings_dir)

    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        print("Run conversation-processor.py first")
        exit(1)

    searcher = ConversationSearch(db_path, embeddings_dir, verbose=verbose)

    try:
        results = []

        if tool:
            # Search by tool
            results = searcher.search_by_tool(tool, limit=limit)

        elif file:
            # Search by file
            results = searcher.search_by_file(file, limit=limit)

        elif query:
            # Text search
            if semantic:
                results = searcher.semantic_search(
                    query,
                    limit=limit,
                    date_from=date_from,
                    date_to=date_to,
                    file_pattern=file
                )
            else:
                results = searcher.keyword_search(
                    query,
                    limit=limit,
                    date_from=date_from,
                    date_to=date_to,
                    file_pattern=file
                )
        else:
            print("Error: Provide a query, --file, or --tool option")
            exit(1)

        # Format and output
        output = searcher.format_results(results, format=format)
        print(output)

    finally:
        searcher.close()


if __name__ == '__main__':
    main()
