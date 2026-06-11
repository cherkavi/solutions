#!/bin/bash
# setup.sh - Setup and ingestion script

# Install Python dependencies
pip install sentence-transformers argparse

# Install specific DB client based on choice
# Uncomment the one you want:
# pip install chromadb
# pip install qdrant-client
# pip install weaviate-client
# pip install lancedb

# Start your chosen Vector DB
# docker-compose up -d chromadb    # for ChromaDB
# docker-compose up -d qdrant      # for Qdrant
# docker-compose up -d weaviate    # for Weaviate

# Run ingestion
python ingest_documents.py \
    --db-type chromadb \
    --db-host localhost \
    --db-port 8000 \
    --collection video_lectures \
    --input-dir ./lectures \
    --chunk-size 500 \
    --embedding-model all-MiniLM-L6-v2 \
    --file-pattern "*.txt,*.md,*.transcript"