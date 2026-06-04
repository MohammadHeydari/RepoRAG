# GitHub Repository RAG Assistant

A Retrieval-Augmented Generation (RAG) system that allows you to **chat with your own GitHub repository** using semantic search and a local LLM (Ollama).

This project indexes a codebase, builds vector embeddings, and enables natural language questions about the repository.

---

## Features

- Automatic GitHub repository loader
- File filtering by extension (`.py`, `.md`, `.yml`, etc.)
- Intelligent code chunking with overlap
- Vector embeddings using SentenceTransformers
- FAISS-based similarity search (cosine similarity)
- Metadata tagging (file path + extension)
- LLM-powered Q&A using Ollama (local models)
- Interactive CLI chat interface

---

## Architecture

```text
GitHub Repo - > load.py - > chunker.py > vectorstore.py > search.py - > chat.py
```
## Project Structure
```
.
├── repo/                 # Cloned GitHub repository
├── load.py              # File loader with metadata extraction
├── chunker.py           # Text chunking logic
├── vectorstore.py       # Embedding + FAISS index builder
├── search.py            # Semantic search engine
├── chat_ollama.py       # RAG chat with Ollama LLM
├── ingest.py            # Debug & ingestion pipeline
├── vector.index         # FAISS index (generated)
└── metadata.npy         # Stored chunks (generated)
```

## Installation

1. Clone this repo

```
git clone https://github.com/MohammadHeydari/RepoRAG.git
cd reporag
```

2. Install dependencies

```
pip install gitpython faiss-cpu numpy sentence-transformers langchain
```
3. Install and run Ollama

Install from: https://ollama.com

Then pull a model:
```
ollama run gemma3:4b
```

## Usage

### Replace this with your own repository URL

Go to ```clone.py``` 

then,

look for this line 

```
REPO_URL = "https://github.com/your-username/your-repo.git"
```
and replace this with your own repository URL. 

#### Step 1: Clone target repository
```
python clone.py
```

#### Step 2: Ingesting

```
python ingest.py
```

#### Step 3: Build vector database
```
python vectorstore.py
```
#### Step 4: Test retrieval (optional)
```
python search.py
```
#### Step 4: Start RAG chat
```
python chat.py
```

## sample ```Q``` and ```R``` of example Queries and corresponding Responses on the current repo:

```
python .\chat.py
```
ignore it: 
```
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.  
Loading weights: 100%|████████████████████████████████████████████████████████████████████████████████| 103/103 [00:00<00:00, 5864.33it/s] 
```

#### Query: What does this repository do?

--- ANSWER ---

```
This repository implements a real-time telecom streaming pipeline using Kafka, Spark Streaming, and Python, currently in development (PoC / experimental). It includes a Kafka producer, a Kafka cluster, a Spark cluster, and a simple dashboard. Future work is planned to include PostgreSQL storage and Grafana dashboards.
```

#### Query: Which services are defined in docker-compose?

--- ANSWER ---

```
Here's a list of the services defined in the `docker-compose.yml` files:

*   minio
*   fastapi
*   clickhouse
*   zookeeper
*   kafka
*   spark
*   spark-worker

```

#### Query: How does Spark streaming work?


`
Spark Streaming reads from Kafka topic `telecom_events`, parses JSON, performs window aggregation (1 minute) by operator, and calculates metrics like `total_data_mb` and `total_call_duration`.
`

#### Query: what is kafka ip?

`
192.168.224.128
`

#### Query: How many files are in the repo?

`
There are 5 files in the repo.
`
#### Query: do we have any images in the repo

`
Yes, the repository contains the following images: minio, nginx, clickhouse, bitnami/zookeeper, bitnami/kafka, and bitnami/spark.
`

#### Query: compose file version?

`
"3.9"
`

#### Query: encoding in kafka producer?

`
The Kafka producer uses `value_serializer=lambda v: json.dumps(v).encode("utf-8")` to encode the event data as UTF-8 bytes before sending it to Kafka.
`
#### Query: what are the kafka events fields?

`
The event contains: user_id, timestamp, data_mb, call_duration, and operator.
`

#### Query: what is the name of network of compose file

`
telecom-net
`

#### Query: How does Spark streaming work?


`
Spark Streaming reads from the Kafka topic `telecom_events`, parses the JSON stream, performs a 1-minute window aggregation by operator, and calculates total data MB and total call duration.
`

#### what is sleep time of kafka in generate events?


`
0.5
`

#### Query: do we have me readme file?

`
Yes, there is a README file.
`

#### Query: any volumes in compose file?

`
clickhouse_data:/var/lib/clickhouse
`

#### Query: what is this function KafkaProducer does?

`
The `KafkaProducer` creates a Kafka producer that sends JSON-encoded events to the `telecom_events` Kafka topic on the server `192.168.224.128:9092`. It uses ZooKeeper for coordination.
`

#### Query: what is the role of generate_event function?

`
The `generate_event()` function creates a JSON-like dictionary containing simulated telecom event data, including user ID, timestamp, data usage, call duration, and operator.
`

#### Query: what is StructType in spark?


`
StructType is a Spark SQL data type that defines the schema of a table or DataFrame. It specifies the names and data types of the columns in the data.
`

#### Query: bootstrap_servers?

`192.168.224.128:9092`

## How It Works
- Repository files are loaded and filtered
- Code is split into overlapping chunks
- Each chunk is embedded into vector space
- FAISS indexes embeddings for fast retrieval
- User query is embedded and matched
- Top-k relevant chunks are sent to LLM
- Ollama generates final answer

---


## GrapRAG Layer (Experimental Extension)

In addition to standard Retrieval-Augmented Generation (RAG), this project includes an experimental **Graph-based RAG layer** to improve contextual understanding of the codebase.

### Overview

Traditional vector search retrieves isolated chunks based on semantic similarity.  
This project extends that with a **Graph RAG approach**, where:

- Each code chunk is represented as a **graph node**
- Nodes are connected based on **entity overlap (e.g., Kafka, Spark, functions, imports)**
- Queries trigger both:
  - Semantic retrieval (via Sentence Transformers)
  - Graph traversal (multi-hop context expansion)

---

### How It Works

The Graph RAG pipeline consists of the following steps:

1. **Repository Parsing**
   - Load source files from the repository
   - Filter supported file types (e.g., `.py`, `.md`, `.yml`)

2. **Chunking**
   - Split files into manageable code/text chunks
   - Attach metadata (file source, extension)

3. **Entity Extraction**
   - Extract named entities from each chunk using NLP (spaCy)
   - Entities include tools, frameworks, functions, and keywords

4. **Graph Construction**
   - Each chunk becomes a node
   - Edges are created when nodes share common entities

5. **Graph-based Retrieval**
   - Query is matched to seed nodes using semantic similarity
   - Graph is expanded using multi-hop traversal
   - Nodes are ranked using:
     - Entity overlap
     - Node connectivity (degree)

---

### Query Flow

`
User Query - > Semantic Search (Sentence Transformers) - > Seed Nodes Selection - >
Graph Expansion (Multi-hop neighbors) - > Scoring & Ranking - > 
Top-K Context Chunks - > LLM (Ollama / Gemma) Answer Generation
`
### Key Benefits

- Captures **relationships between files**, not just similarity
- Improves reasoning over **multi-file dependencies**
- Better answers for architecture-level questions
- Works well for:
  - System design questions
  - Code navigation
  - Dependency tracing

### Status

This Graph RAG layer is currently **experimental** and may evolve into:

- Hybrid Graph + Vector Retrieval system
- PageRank-based node scoring
- Cross-encoder reranking layer
- Code-aware AST-based graph construction

### Future Improvements

- Add PageRank scoring for nodes
- Improve entity extraction for code (AST parsing)
- Hybrid FAISS + Graph retrieval
- Add reranking using transformer cross-encoders

## Contribution

Pull requests are welcome. For major changes, please open an issue first.