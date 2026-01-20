<div align="center">

# LangChain RAG Project

### Retrieval Augmented Generation System for Enterprise Knowledge Management

<a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
<a href="https://python.langchain.com/"><img src="https://img.shields.io/badge/LangChain-1.0+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain"></a>
<a href="https://www.trychroma.com/"><img src="https://img.shields.io/badge/ChromaDB-1.3+-FF6F61?style=for-the-badge&logo=chroma&logoColor=white" alt="ChromaDB"></a>
<a href="https://huggingface.co/"><img src="https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="HuggingFace"></a>
<a href="https://ollama.ai/"><img src="https://img.shields.io/badge/Ollama-Local_LLM-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama"></a>
<a href="https://www.gradio.app/"><img src="https://img.shields.io/badge/Gradio-UI-F97316?style=for-the-badge&logo=gradio&logoColor=white" alt="Gradio"></a>

*A document question answering application built to demonstrate how retrieval augmented generation works in practice. The system ingests markdown documents about a fictional company called Innovatech Solutions, chunks them into semantic pieces, creates vector embeddings using HuggingFace transformers, stores them in ChromaDB, and retrieves relevant context at query time to augment LLM responses. The focus was on building something production ready with clean architecture and proper separation between ingestion, retrieval, and generation components.*

</div>

## Table of Contents

1. [Overview](#overview)
   - 1.1 [The Problem](#the-problem)
   - 1.2 [The Solution](#the-solution)
   - 1.3 [Why I Built This](#why-i-built-this)
2. [Project Structure](#project-structure)
   - 2.1 [Directory Layout](#directory-layout)
   - 2.2 [Core Components](#core-components)
3. [System Architecture](#system-architecture)
   - 3.1 [Pipeline Overview](#pipeline-overview)
   - 3.2 [Data Flow](#data-flow)
   - 3.3 [Design Decisions](#design-decisions)
4. [Quick Start](#quick-start)
   - 4.1 [Prerequisites](#prerequisites)
   - 4.2 [Installation with uv](#installation-with-uv)
   - 4.3 [Installation with pip](#installation-with-pip)
   - 4.4 [Running the Application](#running-the-application)
5. [Configuration](#configuration)
   - 5.1 [LLM Selection](#llm-selection)
   - 5.2 [Retrieval Parameters](#retrieval-parameters)
   - 5.3 [Chunking Strategy](#chunking-strategy)
6. [Knowledge Base](#knowledge-base)

## Overview

### The Problem

Large Language Models are incredibly powerful, but they have a fundamental limitation: they only know what they were trained on. When you need an AI assistant that understands your specific company documents, product specifications, employee information, or business contracts, a vanilla LLM simply cannot help. It will either hallucinate information or admit it does not know.

### The Solution

Retrieval Augmented Generation solves this by giving the LLM access to external knowledge at inference time. Instead of trying to fine tune the model on your data, which is expensive and requires retraining whenever documents change, RAG retrieves relevant document chunks based on semantic similarity to the user query and injects them into the prompt as context. The LLM then generates responses grounded in your actual documents.

### Why I Built This

I built this project to move beyond theoretical understanding of RAG into practical implementation. Most tutorials show simplified examples with a few lines of code, but real systems need to handle document ingestion pipelines, vector database management, prompt engineering, conversation history, and user interfaces. I wanted to understand each of these components deeply, so I built them from scratch using LangChain as the orchestration layer rather than relying on high level abstractions that hide the complexity.

The fictional company Innovatech Solutions serves as a realistic test case with 31 markdown documents covering company information, product specifications, employee profiles, and business contracts. This synthetic dataset, which I generated using frontier LLMs, provides enough variety to test the system thoroughly while being small enough to iterate quickly during development.

## Project Structure

### Directory Layout

```
langchain-rag-project/
├── README.md
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .env
│
└── src/
    ├── app.py
    │
    ├── implementation/
    │   ├── ingest.py
    │   └── answer.py
    │
    ├── knowledge_base/
    │   ├── company/
    │   ├── products/
    │   ├── employees/
    │   └── contracts/
    │
    ├── experiments/
    │   └── experiment.ipynb
    │
    └── vector_db/
```

### Core Components

**app.py** is the entry point, a Gradio web application with a two column layout showing the chat interface on the left and retrieved source documents on the right. I chose Gradio over Streamlit because it handles chat interfaces more elegantly out of the box and requires less boilerplate code.

**implementation/ingest.py** handles the document ingestion pipeline. It scans the knowledge base directory, loads all markdown files, splits them into overlapping chunks, generates embeddings using HuggingFace transformers, and stores everything in ChromaDB. The ingestion process is idempotent, meaning you can run it multiple times safely because it clears the existing collection before recreating it.

**implementation/answer.py** implements the RAG pipeline itself. When a user asks a question, it retrieves the top K most relevant document chunks from ChromaDB, formats them into a context string, constructs a system prompt with the context injected, and sends the conversation to the LLM for response generation.

**knowledge_base/** contains 31 markdown documents organized into four categories: company information, product documentation, employee profiles, and business contracts. All documents are synthetic data that I generated to create a realistic enterprise knowledge base.

**vector_db/** is created automatically when you run the ingestion script. It contains the ChromaDB database with all document embeddings. This directory is gitignored because it should be generated locally.

## System Architecture

### Pipeline Overview

The system operates in two distinct phases. The ingestion phase runs once or whenever the knowledge base changes, processing documents into vector embeddings. The query phase runs in real time, handling user questions by retrieving relevant context and generating responses.

```
INGESTION PHASE

Documents  ──>  Text Splitter  ──>  Embedding Model  ──>  ChromaDB
   │                 │                    │                  │
   │            500 chars            all-MiniLM-L6-v2    Persistent
   │            200 overlap          384 dimensions       Storage
   │
   └── 31 markdown files across 4 categories


QUERY PHASE

User Query  ──>  Embedding  ──>  Vector Search  ──>  Top K Chunks
                                                          │
                                                          v
Response  <──  LLM Generation  <──  Prompt Construction
   │                │                      │
   │           Gemma3 4B              Context + History
   │           via Ollama             + System Prompt
```

### Data Flow

When a user submits a question, the system first combines it with the conversation history to improve retrieval quality. Multi turn conversations often have questions that reference previous context, so including prior user messages helps the retriever find relevant documents even when the current question is vague or refers to earlier topics.

The combined query is embedded using the same HuggingFace model used during ingestion, ensuring vector space alignment. ChromaDB performs approximate nearest neighbor search to find the 10 most semantically similar document chunks.

These chunks are concatenated into a context string and injected into a system prompt that instructs the LLM to act as a knowledgeable assistant for Innovatech Solutions. The conversation history is preserved so the LLM can reference earlier exchanges, and the user question is appended as the final message.

The response streams back to the Gradio interface along with the source documents, which are displayed in the right panel so users can verify where the information came from.

### Design Decisions

**Why ChromaDB over other vector databases?** I considered Pinecone, Weaviate, and Qdrant, but ChromaDB won for this project because it runs entirely locally with no external dependencies, stores data persistently by default, and has excellent LangChain integration. For a learning project, I did not want to deal with API keys, usage limits, or cloud infrastructure.

**Why HuggingFace embeddings over OpenAI?** The all-MiniLM-L6-v2 model produces high quality 384 dimensional embeddings while running entirely on CPU. This eliminates API costs and latency, making the system completely self contained. For production with GPU acceleration, I would consider all-mpnet-base-v2 which has higher quality at the cost of speed.

**Why Ollama for local inference?** Running Gemma3 4B locally through Ollama gives me full control over the inference stack with no per token costs. The OpenAI compatible API means I can switch between local and cloud models by changing one line of code. For users who prefer OpenAI, the code includes a commented alternative.

**Why 500 character chunks with 200 character overlap?** After experimenting with various chunk sizes, I found 500 characters provides enough context for coherent retrieval without overwhelming the context window. The 40% overlap ensures important information at chunk boundaries is not lost during splitting.

**Why force CPU for embeddings?** I discovered that PyTorch CUDA support requires specific GPU architectures. Older GPUs like the GTX 1060 have CUDA capability 6.1, but modern PyTorch builds require 7.0 or higher. Rather than creating installation friction, I configured embeddings to run on CPU by default, which is fast enough for this workload.

## Quick Start

### Prerequisites

You need Python 3.13 or higher installed on your system. You also need either an OpenAI API key or Ollama running locally for LLM inference. I recommend Ollama because it gives you a completely free, local setup.

### Installation with uv

uv is a fast Python package manager written in Rust. It handles virtual environments automatically and installs dependencies 10 to 100 times faster than pip. I use it for all my projects now.

Install uv if you do not have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Clone the repository and install dependencies:

```bash
git clone https://github.com/FamilOrujov/langchain-rag-project.git
cd langchain-rag-project
uv venv
uv sync
```

With uv, you do not need to activate the virtual environment manually. Just prefix commands with `uv run`:

```bash
uv run python src/implementation/ingest.py
uv run python src/app.py
```

### Installation with pip

If you prefer the traditional approach:

```bash
git clone https://github.com/FamilOrujov/langchain-rag-project.git
cd langchain-rag-project
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then run the application:

```bash
cd src
python implementation/ingest.py
python app.py
```

### Running the Application

First, ingest the documents to create the vector database:

```bash
uv run python src/implementation/ingest.py
```

You should see output like:

```
There are 199 vectors with 384 dimensions in the vector store
Ingestion complete
```

Then launch the web interface:

```bash
uv run python src/app.py
```

The Gradio interface will open in your browser at http://localhost:7860. Try questions like "What products does Innovatech Solutions offer?" or "Tell me about Seraphina Jones" to see the RAG system in action.

## Configuration

### LLM Selection

The system defaults to Gemma3 4B running through Ollama. To use this, install Ollama and pull the model:

```bash
ollama pull gemma3:4b
```

To switch to OpenAI, edit `src/implementation/answer.py` and uncomment the OpenAI configuration:

```python
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
```

You will also need to create a `.env` file with your API key:

```
OPENAI_API_KEY=your_key_here
```

### Retrieval Parameters

The `RETRIEVAL_K` constant in `answer.py` controls how many document chunks are retrieved for each query. The default of 10 provides good coverage without exceeding context limits. Lower values give faster responses, higher values provide more comprehensive context at the cost of speed and potential noise.

### Chunking Strategy

The chunking parameters in `ingest.py` control how documents are split:

```python
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
```

If you modify these values, you must re run the ingestion script to rebuild the vector database with the new chunk sizes.

## Knowledge Base

The knowledge base contains 31 markdown documents organized into four categories:

| Category | Documents | Description |
|----------|-----------|-------------|
| Company | 4 | Mission statement, culture, history, careers |
| Products | 5 | SynapseEngine, ClarityLens, Continuum, EchoSphere, Guardian |
| Employees | 10 | Profile pages with roles and responsibilities |
| Contracts | 12 | Business agreements, MSAs, partnerships |

All documents are synthetic data generated specifically for this project. They provide a realistic enterprise knowledge base for testing RAG capabilities without any privacy concerns.

To add your own documents, simply place markdown files in the appropriate subdirectory under `src/knowledge_base/` and re run the ingestion script. The system automatically detects document type based on folder name and adds it as metadata for potential filtering.
