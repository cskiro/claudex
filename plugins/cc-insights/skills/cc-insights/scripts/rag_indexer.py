#!/usr/bin/env python3
"""
RAG Indexer for Claude Code Insights

Builds vector embeddings for semantic search using sentence-transformers
and ChromaDB. Supports incremental indexing and efficient similarity search.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import click

try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    from chromadb.config import Settings
except ImportError as e:
    print(f"Error: Required packages not installed. Run: pip install sentence-transformers chromadb")
    print(f"Missing: {e}")
    exit(1)


class RAGIndexer:
    """Builds and manages vector embeddings for conversations"""

    def __init__(self, db_path: Path, embeddings_dir: Path, model_name: str = "all-MiniLM-L6-v2", verbose: bool = False):
        self.db_path = db_path
        self.embeddings_dir = embeddings_dir
        self.model_name = model_name
        self.verbose = verbose

        # Initialize sentence transformer model
        self._log("Loading embedding model...")
        self.model = SentenceTransformer(model_name)
        self._log(f"✓ Loaded {model_name}")

        # Initialize ChromaDB
        self.embeddings_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.embeddings_dir),
            settings=Settings(anonymized_telemetry=False)
        )

        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="conversations",
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )

        # Connect to SQLite
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

    def _log(self, message: str):
        """Log if verbose mode is enabled"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def _get_indexed_conversation_ids(self) -> set:
        """Get set of conversation IDs already indexed"""
        try:
            results = self.collection.get(include=[])
            return set(results['ids'])
        except Exception:
            return set()

    def _fetch_conversations_to_index(self, rebuild: bool = False) -> List[Dict[str, Any]]:
        """Fetch conversations that need indexing"""
        if rebuild:
            # Rebuild: get all conversations
            cursor = self.conn.execute("""
                SELECT id, first_user_message, last_assistant_message, topics,
                       files_read, files_written, files_edited, timestamp
                FROM conversations
                ORDER BY timestamp DESC
            """)
        else:
            # Incremental: only get conversations not yet indexed
            indexed_ids = self._get_indexed_conversation_ids()
            if not indexed_ids:
                # Nothing indexed yet, get all
                cursor = self.conn.execute("""
                    SELECT id, first_user_message, last_assistant_message, topics,
                           files_read, files_written, files_edited, timestamp
                    FROM conversations
                    ORDER BY timestamp DESC
                """)
            else:
                # Get conversations not in indexed set
                placeholders = ','.join('?' * len(indexed_ids))
                cursor = self.conn.execute(f"""
                    SELECT id, first_user_message, last_assistant_message, topics,
                           files_read, files_written, files_edited, timestamp
                    FROM conversations
                    WHERE id NOT IN ({placeholders})
                    ORDER BY timestamp DESC
                """, tuple(indexed_ids))

        conversations = []
        for row in cursor.fetchall():
            conversations.append({
                'id': row['id'],
                'first_user_message': row['first_user_message'] or "",
                'last_assistant_message': row['last_assistant_message'] or "",
                'topics': json.loads(row['topics']) if row['topics'] else [],
                'files_read': json.loads(row['files_read']) if row['files_read'] else [],
                'files_written': json.loads(row['files_written']) if row['files_written'] else [],
                'files_edited': json.loads(row['files_edited']) if row['files_edited'] else [],
                'timestamp': row['timestamp']
            })

        return conversations

    def _create_document_text(self, conversation: Dict[str, Any]) -> str:
        """Create text document for embedding"""
        # Combine relevant fields into searchable text
        parts = []

        if conversation['first_user_message']:
            parts.append(f"User: {conversation['first_user_message']}")

        if conversation['last_assistant_message']:
            parts.append(f"Assistant: {conversation['last_assistant_message']}")

        if conversation['topics']:
            parts.append(f"Topics: {', '.join(conversation['topics'])}")

        all_files = conversation['files_read'] + conversation['files_written'] + conversation['files_edited']
        if all_files:
            parts.append(f"Files: {', '.join(all_files)}")

        return "\n\n".join(parts)

    def _create_metadata(self, conversation: Dict[str, Any]) -> Dict[str, Any]:
        """Create metadata for ChromaDB"""
        return {
            'timestamp': conversation['timestamp'],
            'topics': json.dumps(conversation['topics']),
            'files_read': json.dumps(conversation['files_read']),
            'files_written': json.dumps(conversation['files_written']),
            'files_edited': json.dumps(conversation['files_edited']),
        }

    def index_conversations(self, rebuild: bool = False, batch_size: int = 32) -> int:
        """Index conversations for semantic search"""
        if rebuild:
            self._log("Rebuilding entire index...")
            # Clear existing collection
            self.chroma_client.delete_collection("conversations")
            self.collection = self.chroma_client.create_collection(
                name="conversations",
                metadata={"hnsw:space": "cosine"}
            )
        else:
            self._log("Incremental indexing...")

        # Fetch conversations to index
        conversations = self._fetch_conversations_to_index(rebuild)

        if not conversations:
            self._log("No conversations to index")
            return 0

        self._log(f"Indexing {len(conversations)} conversations...")

        # Process in batches
        indexed_count = 0
        for i in range(0, len(conversations), batch_size):
            batch = conversations[i:i + batch_size]

            # Prepare batch data
            ids = []
            documents = []
            metadatas = []

            for conv in batch:
                ids.append(conv['id'])
                documents.append(self._create_document_text(conv))
                metadatas.append(self._create_metadata(conv))

            # Generate embeddings
            embeddings = self.model.encode(documents, show_progress_bar=self.verbose)

            # Add to ChromaDB
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings.tolist(),
                metadatas=metadatas
            )

            indexed_count += len(batch)
            self._log(f"Indexed {indexed_count}/{len(conversations)} conversations")

        self._log(f"✓ Indexing complete: {indexed_count} conversations")
        return indexed_count

    def search(self, query: str, n_results: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search conversations by semantic similarity"""
        # Generate query embedding
        query_embedding = self.model.encode([query])[0]

        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results,
            where=filters if filters else None
        )

        # Format results
        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                'id': results['ids'][0][i],
                'distance': results['distances'][0][i],
                'similarity': 1 - results['distances'][0][i],  # Convert distance to similarity
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
            })

        return formatted_results

    def get_stats(self) -> Dict[str, Any]:
        """Get indexing statistics"""
        try:
            count = self.collection.count()
            return {
                'total_indexed': count,
                'model': self.model_name,
                'collection_name': self.collection.name,
                'embedding_dimension': self.model.get_sentence_embedding_dimension()
            }
        except Exception as e:
            return {
                'error': str(e)
            }

    def close(self):
        """Close connections"""
        if self.conn:
            self.conn.close()


@click.command()
@click.option('--db-path', type=click.Path(), default='.claude/skills/cc-insights/.processed/conversations.db',
              help='SQLite database path')
@click.option('--embeddings-dir', type=click.Path(), default='.claude/skills/cc-insights/.processed/embeddings',
              help='ChromaDB embeddings directory')
@click.option('--model', default='all-MiniLM-L6-v2', help='Sentence transformer model name')
@click.option('--rebuild', is_flag=True, help='Rebuild entire index (delete and recreate)')
@click.option('--batch-size', default=32, help='Batch size for embedding generation')
@click.option('--verbose', is_flag=True, help='Show detailed logs')
@click.option('--stats', is_flag=True, help='Show statistics after indexing')
@click.option('--test-search', type=str, help='Test search with query')
def main(db_path: str, embeddings_dir: str, model: str, rebuild: bool, batch_size: int, verbose: bool, stats: bool, test_search: Optional[str]):
    """Build vector embeddings for semantic search"""
    db_path = Path(db_path)
    embeddings_dir = Path(embeddings_dir)

    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        print("Run conversation-processor.py first to process conversations")
        exit(1)

    indexer = RAGIndexer(db_path, embeddings_dir, model, verbose=verbose)

    try:
        # Index conversations
        count = indexer.index_conversations(rebuild=rebuild, batch_size=batch_size)

        print(f"\n✓ Indexed {count} conversations")

        if stats:
            print("\n=== Indexing Statistics ===")
            stats_data = indexer.get_stats()
            for key, value in stats_data.items():
                print(f"{key}: {value}")

        if test_search:
            print(f"\n=== Test Search: '{test_search}' ===")
            results = indexer.search(test_search, n_results=5)

            if not results:
                print("No results found")
            else:
                for i, result in enumerate(results, 1):
                    print(f"\n{i}. [Similarity: {result['similarity']:.3f}] {result['id']}")
                    print(f"   {result['document'][:200]}...")

    finally:
        indexer.close()


if __name__ == '__main__':
    main()
