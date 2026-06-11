#!/usr/bin/env python3
"""
Vendor-agnostic document ingestion system for Vector DBs
Supports: ChromaDB, Qdrant, Weaviate, Milvus, LanceDB, pgvector
"""

import os
import argparse
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

# Optional imports - install only what you need
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False

# Vector DB clients (install as needed)
CHROMA_AVAILABLE = False
QDRANT_AVAILABLE = False
WEAVIATE_AVAILABLE = False
MILVUS_AVAILABLE = False
LANCEDB_AVAILABLE = False
PGVECTOR_AVAILABLE = False

try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    pass

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams
    QDRANT_AVAILABLE = True
except ImportError:
    pass

try:
    import weaviate
    WEAVIATE_AVAILABLE = True
except ImportError:
    pass

try:
    from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType
    MILVUS_AVAILABLE = True
except ImportError:
    pass

try:
    import lancedb
    LANCEDB_AVAILABLE = True
except ImportError:
    pass

try:
    import psycopg2
    import numpy as np
    PGVECTOR_AVAILABLE = True
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Document:
    """Document representation"""
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    doc_id: str = ""


class EmbeddingProvider:
    """Generate embeddings for documents"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        if not EMBEDDINGS_AVAILABLE:
            raise ImportError("Install sentence-transformers: pip install sentence-transformers")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Loaded embedding model: {model_name} (dim={self.dimension})")
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts).tolist()


class DocumentProcessor:
    """Process and chunk documents"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def process_file(self, file_path: Path) -> List[Document]:
        """Process a single file into chunks"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract video lecture metadata from filename
        metadata = self._extract_metadata(file_path)
        
        # Chunk the content
        chunks = self._chunk_text(content)
        
        documents = []
        for i, chunk in enumerate(chunks):
            doc_id = hashlib.md5(f"{file_path}_{i}".encode()).hexdigest()
            chunk_metadata = {
                **metadata,
                "chunk_index": i,
                "chunk_count": len(chunks),
                "file_path": str(file_path),
                "file_type": file_path.suffix
            }
            documents.append(Document(
                content=chunk,
                metadata=chunk_metadata,
                doc_id=doc_id
            ))
        
        return documents
    
    def _extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from filename and path"""
        metadata = {
            "filename": file_path.name,
            "directory": str(file_path.parent),
            "size_bytes": file_path.stat().st_size
        }
        
        # Try to extract video lecture info from filename
        # Example: "Lecture_01_Introduction.md" or "Week2_TopicName.txt"
        name_parts = file_path.stem.split('_')
        if len(name_parts) >= 2:
            # Attempt to identify lecture number
            for part in name_parts:
                if part.isdigit():
                    metadata["lecture_number"] = int(part)
                    break
                if part.lower().startswith('lecture') or part.lower().startswith('lec'):
                    num_part = part.lower().replace('lecture', '').replace('lec', '')
                    if num_part.isdigit():
                        metadata["lecture_number"] = int(num_part)
        
        return metadata
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        if len(words) <= self.chunk_size:
            return [text]
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = ' '.join(words[i:i + self.chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks


class VectorDBAdapter(ABC):
    """Abstract adapter for vector databases"""
    
    @abstractmethod
    def connect(self, **kwargs):
        pass
    
    @abstractmethod
    def create_collection(self, collection_name: str, dimension: int):
        pass
    
    @abstractmethod
    def insert_documents(self, collection_name: str, documents: List[Document]):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass


class ChromaDBAdapter(VectorDBAdapter):
    def connect(self, host: str = "localhost", port: int = 8000, **kwargs):
        self.client = chromadb.HttpClient(host=host, port=port)
        logger.info(f"Connected to ChromaDB at {host}:{port}")
    
    def create_collection(self, collection_name: str, dimension: int):
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def insert_documents(self, collection_name: str, documents: List[Document]):
        collection = self.client.get_collection(collection_name)
        collection.add(
            documents=[doc.content for doc in documents],
            metadatas=[doc.metadata for doc in documents],
            ids=[doc.doc_id for doc in documents],
            embeddings=[doc.embedding for doc in documents]
        )
        logger.info(f"Inserted {len(documents)} documents into ChromaDB")
    
    def disconnect(self):
        pass


class QdrantAdapter(VectorDBAdapter):
    def connect(self, host: str = "localhost", port: int = 6333, **kwargs):
        self.client = QdrantClient(host=host, port=port)
        logger.info(f"Connected to Qdrant at {host}:{port}")
    
    def create_collection(self, collection_name: str, dimension: int):
        self.client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dimension, distance=Distance.COSINE)
        )
    
    def insert_documents(self, collection_name: str, documents: List[Document]):
        from qdrant_client.models import PointStruct
        
        points = [
            PointStruct(
                id=doc.doc_id,
                vector=doc.embedding,
                payload={
                    "content": doc.content,
                    **doc.metadata
                }
            )
            for doc in documents
        ]
        self.client.upsert(collection_name=collection_name, points=points)
        logger.info(f"Inserted {len(documents)} documents into Qdrant")
    
    def disconnect(self):
        self.client.close()


class WeaviateAdapter(VectorDBAdapter):
    def connect(self, host: str = "localhost", port: int = 8080, **kwargs):
        self.client = weaviate.Client(f"http://{host}:{port}")
        logger.info(f"Connected to Weaviate at {host}:{port}")
    
    def create_collection(self, collection_name: str, dimension: int):
        class_name = collection_name.capitalize()
        schema = {
            "class": class_name,
            "vectorizer": "none",
            "properties": [
                {"name": "content", "dataType": ["text"]},
                {"name": "metadata", "dataType": ["object"]}
            ]
        }
        if not self.client.schema.exists(class_name):
            self.client.schema.create_class(schema)
    
    def insert_documents(self, collection_name: str, documents: List[Document]):
        class_name = collection_name.capitalize()
        with self.client.batch as batch:
            for doc in documents:
                properties = {
                    "content": doc.content,
                    "metadata": doc.metadata
                }
                batch.add_data_object(
                    data_object=properties,
                    class_name=class_name,
                    vector=doc.embedding,
                    uuid=doc.doc_id
                )
        logger.info(f"Inserted {len(documents)} documents into Weaviate")
    
    def disconnect(self):
        pass


class LanceDBAdapter(VectorDBAdapter):
    def connect(self, uri: str = "./lancedb_data", **kwargs):
        self.db = lancedb.connect(uri)
        logger.info(f"Connected to LanceDB at {uri}")
    
    def create_collection(self, collection_name: str, dimension: int):
        import pyarrow as pa
        schema = pa.schema([
            pa.field("doc_id", pa.string()),
            pa.field("content", pa.string()),
            pa.field("vector", pa.list_(pa.float32(), dimension)),
            pa.field("metadata", pa.string())  # JSON string
        ])
        self.table = self.db.create_table(collection_name, schema=schema, mode="overwrite")
    
    def insert_documents(self, collection_name: str, documents: List[Document]):
        import json
        import pyarrow as pa
        
        table = self.db.open_table(collection_name)
        data = {
            "doc_id": [doc.doc_id for doc in documents],
            "content": [doc.content for doc in documents],
            "vector": [doc.embedding for doc in documents],
            "metadata": [json.dumps(doc.metadata) for doc in documents]
        }
        table.add(pa.table(data))
        logger.info(f"Inserted {len(documents)} documents into LanceDB")
    
    def disconnect(self):
        pass


def get_adapter(db_type: str) -> VectorDBAdapter:
    """Factory function for vector DB adapters"""
    adapters = {
        "chromadb": (ChromaDBAdapter, CHROMA_AVAILABLE),
        "qdrant": (QdrantAdapter, QDRANT_AVAILABLE),
        "weaviate": (WeaviateAdapter, WEAVIATE_AVAILABLE),
        "lancedb": (LanceDBAdapter, LANCEDB_AVAILABLE),
    }
    
    if db_type not in adapters:
        raise ValueError(f"Unsupported DB type: {db_type}. Choose from {list(adapters.keys())}")
    
    adapter_class, is_available = adapters[db_type]
    if not is_available:
        raise ImportError(f"Install {db_type} client library first")
    
    return adapter_class()


def main():
    parser = argparse.ArgumentParser(description="Ingest documents into Vector DB")
    parser.add_argument("--db-type", required=True, 
                       choices=["chromadb", "qdrant", "weaviate", "lancedb", "milvus", "pgvector"],
                       help="Vector database type")
    parser.add_argument("--db-host", default="localhost", help="Database host")
    parser.add_argument("--db-port", type=int, help="Database port")
    parser.add_argument("--collection", default="video_lectures", help="Collection/table name")
    parser.add_argument("--input-dir", required=True, help="Directory with text files")
    parser.add_argument("--chunk-size", type=int, default=500, help="Text chunk size in words")
    parser.add_argument("--embedding-model", default="all-MiniLM-L6-v2", 
                       help="Sentence transformer model name")
    parser.add_argument("--file-pattern", default="*.txt,*.md,*.transcript", 
                       help="File patterns to process (comma-separated)")
    
    args = parser.parse_args()
    
    # Initialize components
    embedder = EmbeddingProvider(args.embedding_model)
    processor = DocumentProcessor(chunk_size=args.chunk_size)
    adapter = get_adapter(args.db_type)
    
    # Set default ports
    default_ports = {
        "chromadb": 8000,
        "qdrant": 6333,
        "weaviate": 8080,
    }
    port = args.db_port or default_ports.get(args.db_type, 8000)
    
    # Connect to database
    adapter.connect(host=args.db_host, port=port)
    adapter.create_collection(args.collection, embedder.dimension)
    
    # Process files
    input_path = Path(args.input_dir)
    file_patterns = [p.strip() for p in args.file_pattern.split(',')]
    
    all_documents = []
    for pattern in file_patterns:
        for file_path in input_path.rglob(pattern):
            logger.info(f"Processing: {file_path}")
            documents = processor.process_file(file_path)
            all_documents.extend(documents)
    
    # Generate embeddings in batches
    batch_size = 32
    for i in range(0, len(all_documents), batch_size):
        batch = all_documents[i:i + batch_size]
        texts = [doc.content for doc in batch]
        embeddings = embedder.embed(texts)
        for doc, embedding in zip(batch, embeddings):
            doc.embedding = embedding
    
    # Insert into database
    adapter.insert_documents(args.collection, all_documents)
    adapter.disconnect()
    
    logger.info(f"Successfully ingested {len(all_documents)} document chunks")
    logger.info(f"Source files: {len(set(d.metadata['file_path'] for d in all_documents))}")


if __name__ == "__main__":
    main()