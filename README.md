<div align="center">

# LangChain RAG Project

### Retrieval Augmented Generation System for Enterprise Knowledge Management

<a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
<a href="https://python.langchain.com/"><img src="https://img.shields.io/badge/LangChain-1.0+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain"></a>
<a href="https://www.trychroma.com/"><img src="https://img.shields.io/badge/ChromaDB-1.3+-FF6F61?style=for-the-badge&logo=chroma&logoColor=white" alt="ChromaDB"></a>
<a href="https://huggingface.co/"><img src="https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="HuggingFace"></a>
<a href="https://ollama.ai/"><img src="https://img.shields.io/badge/Ollama-Local_LLM-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama"></a>
<a href="https://www.gradio.app/"><img src="https://img.shields.io/badge/Gradio-UI-F97316?style=for-the-badge&logo=gradio&logoColor=white" alt="Gradio"></a>
<a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"></a>

<img src="assets/innovatech_m.gif" alt="Demo" width="800">

*Document question answering Knowledge Base RAG application built to demonstrate how retrieval augmented generation works in practice. The system ingests markdown documents about a fictional company called Innovatech Solutions, chunks them into semantic pieces, creates vector embeddings using HuggingFace transformers, stores them in ChromaDB, and retrieves relevant context at query time to augment LLM responses. The focus was on building something production ready with clean architecture and proper separation between ingestion, retrieval, and generation components.*

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
4. [Installation](#installation)
   - 4.1 [Choose Your Path](#choose-your-path)
   - 4.2 [Installation with uv (Recommended)](#installation-with-uv-recommended)
   - 4.3 [Installation with pip](#installation-with-pip)
   - 4.4 [Docker Installation](#docker-installation)
5. [Configuration](#configuration)
   - 5.1 [LLM Selection](#llm-selection)
   - 5.2 [Retrieval Parameters](#retrieval-parameters)
   - 5.3 [Chunking Strategy](#chunking-strategy)
6. [Testing](#testing)
   - 6.1 [Test Architecture](#test-architecture)
   - 6.2 [Running Tests](#running-tests)
   - 6.3 [Continuous Integration](#continuous-integration)
7. [Knowledge Base](#knowledge-base)


## Overview

### The Problem

Large Language Models are incredibly powerful, but they have a fundamental limitation: they only know what they were trained on. When you need an AI assistant that understands your specific company documents, product specifications, employee information, or business contracts, a vanilla LLM simply cannot help. It will either hallucinate information or admit it does not know.

### The Solution

Retrieval Augmented Generation solves this by giving the LLM access to external knowledge at inference time. Instead of trying to fine tune the model on your data, which is expensive and requires retraining whenever documents change, RAG retrieves relevant document chunks based on semantic similarity to the user query and injects them into the prompt as context. The LLM then generates responses grounded in your actual documents.

### Why I Built This

I built this project because most RAG implementations I encountered were either too simplistic or too abstracted. Real systems need to handle document ingestion pipelines, vector database management, prompt engineering, conversation history, and user interfaces. I built each component from scratch using LangChain as the orchestration layer, giving me full control over retrieval parameters, chunking strategies, and prompt construction.

The fictional company Innovatech Solutions serves as a realistic test case with 31 markdown documents covering company information, product specifications, employee profiles, and business contracts. This synthetic dataset provides enough variety to validate the system across different document types and query patterns.

## Project Structure

### Directory Layout

```
langchain-rag-project/
├── README.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-docker.txt
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .env
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── lint.yml
│
├── tests/
│   ├── conftest.py
│   ├── test_ingest.py
│   ├── test_answer.py
│   └── test_integration.py
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

<img src="assets/system_architecture.png" alt="System Architecture" width="800">

### Data Flow

When a user submits a question, the system first combines it with the conversation history to improve retrieval quality. Multi turn conversations often have questions that reference previous context, so including prior user messages helps the retriever find relevant documents even when the current question is vague or refers to earlier topics.

The combined query is embedded using the same HuggingFace model used during ingestion, ensuring vector space alignment. ChromaDB performs approximate nearest neighbor search to find the 10 most semantically similar document chunks.

These chunks are concatenated into a context string and injected into a system prompt that instructs the LLM to act as a knowledgeable assistant for Innovatech Solutions. The conversation history is preserved so the LLM can reference earlier exchanges, and the user question is appended as the final message.

The response streams back to the Gradio interface along with the source documents, which are displayed in the right panel so users can verify where the information came from.

### Design Decisions

**Why ChromaDB over other vector databases?** I considered Pinecone, Weaviate, and Qdrant, but ChromaDB won for this project because it runs entirely locally with no external dependencies, stores data persistently by default, and has excellent LangChain integration. This eliminates the need for API keys, usage limits, or cloud infrastructure, making the system fully self contained and easy to deploy anywhere.

**Why HuggingFace embeddings over OpenAI?** The all-MiniLM-L6-v2 model produces high quality 384 dimensional embeddings while running entirely on CPU. This eliminates API costs and latency, making the system completely self contained. For production with GPU acceleration, I would consider all-mpnet-base-v2 which has higher quality at the cost of speed.

**Why Ollama for local inference?** Running Gemma3 4B locally through Ollama gives me full control over the inference stack with no per token costs. The OpenAI compatible API means I can switch between local and cloud models by changing one line of code. For users who prefer OpenAI, the code includes a commented alternative.

**Why 500 character chunks with 200 character overlap?** After experimenting with various chunk sizes, I found 500 characters provides enough context for coherent retrieval without overwhelming the context window. The 40% overlap ensures important information at chunk boundaries is not lost during splitting.

**Why force CPU for embeddings?** I discovered that PyTorch CUDA support requires specific GPU architectures. Older GPUs like the GTX 1060 have CUDA capability 6.1, but modern PyTorch builds require 7.0 or higher. Rather than creating installation friction, I configured embeddings to run on CPU by default, which is fast enough for this workload.

## Installation

### Choose Your Path

I provide three installation methods depending on your preferences and setup. Each has its trade offs, and I want to be transparent about what you are getting into with each approach.

| Method | Build Time | Best For | Prerequisites |
|--------|------------|----------|---------------|
| **uv (Recommended)** | ~3 min | Development, full CUDA support | Python 3.13+, Ollama |
| **pip** | ~5 min | Traditional Python workflow | Python 3.13+, Ollama |
| **Docker** | ~12 min | Isolated environment, quick demo | Docker Desktop |

**A note on Docker and CUDA:** The Docker image uses CPU only PyTorch to keep the image size manageable (~3GB instead of ~12GB) and build times reasonable (~12 minutes instead of ~50 minutes). If you need GPU acceleration for embeddings, I recommend the local installation with uv where you can install the full CUDA enabled PyTorch. For most use cases, CPU embeddings are fast enough since embedding generation is not the bottleneck, the LLM inference is.

### Installation with uv (Recommended)

This is my recommended approach for most users. uv is a fast Python package manager written in Rust that handles virtual environments automatically and installs dependencies 10 to 100 times faster than pip. I use it for all my projects now, and once you try it you probably will too.

**Prerequisites:**
- Python 3.13 or higher
- Ollama installed with Gemma3 model pulled
- NVIDIA GPU with CUDA 11.8+ (optional, for GPU acceleration)

**Step 1: Install uv**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Step 2: Clone and install dependencies**

```bash
git clone https://github.com/FamilOrujov/langchain-rag-project.git
cd langchain-rag-project
uv venv
uv sync
```

This installs the full dependency set including CUDA enabled PyTorch if your system supports it. The `uv.lock` file ensures reproducible installs across different machines.

**Step 3: Pull the Ollama model**

```bash
ollama pull gemma3:4b
```

**Step 4: Ingest the knowledge base**

```bash
uv run python src/implementation/ingest.py
```

You should see output confirming 199 vectors were created.

**Step 5: Launch the application**

```bash
uv run python src/app.py
```

The Gradio interface opens at http://localhost:7860.

**Why uv over pip?** uv is a Rust implementation of pip that is 10 to 100 times faster for dependency resolution and installation. It also handles virtual environments transparently, so you never have to remember to activate anything. Just prefix commands with `uv run` and it handles the rest.

### Installation with pip

If you prefer the traditional Python workflow or cannot install uv for some reason, pip works fine. The only downside is slower installation and manual virtual environment management.

**Prerequisites:**
- Python 3.13 or higher
- Ollama installed with Gemma3 model pulled

**Step 1: Clone and set up environment**

```bash
git clone https://github.com/FamilOrujov/langchain-rag-project.git
cd langchain-rag-project
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Step 2: Pull the Ollama model**

```bash
ollama pull gemma3:4b
```

**Step 3: Ingest and run**

```bash
cd src
python implementation/ingest.py
python app.py
```

**Remember:** You need to activate the virtual environment every time you open a new terminal session before running commands. With uv, this is handled automatically.

### Docker Installation

If you prefer containerized environments or want a quick demo without installing Python dependencies on your system, Docker is available. I optimized the Docker build to use CPU only PyTorch, which dramatically reduces the image size and build time. The trade off is that embedding generation runs on CPU instead of GPU, but for a knowledge base of this size the difference is negligible.

**Prerequisites:**
- Docker Desktop installed and running
- Ollama running on your host machine with Gemma3 pulled

**Step 1: Clone and build**

```bash
git clone https://github.com/FamilOrujov/langchain-rag-project.git
cd langchain-rag-project
docker compose build
```

The first build takes around 12 minutes as it downloads Python dependencies and pre ingests the knowledge base. Subsequent builds are cached and take seconds.

**Step 2: Start the container**

```bash
docker compose up
```

**Step 3: Access the application**

Open http://localhost:7860 in your browser. The knowledge base is already ingested during the build process, so you can start asking questions immediately.

**Note about Ollama:** The Docker container needs to communicate with Ollama running on your host. On Linux, this works automatically. On macOS and Windows, you may need to update `src/implementation/answer.py` to use `host.docker.internal` instead of `localhost` for the Ollama base URL, or configure your network settings appropriately.

**Stopping the container:**

```bash
docker compose down
```

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

## Testing

I believe production ready code needs proper test coverage, not as an afterthought but as a core part of the development process. The test suite validates both individual components and the full RAG pipeline, ensuring that changes to one part of the system do not break others.

### Test Architecture

The test suite is organized into three layers that mirror the testing pyramid. Unit tests cover individual functions in isolation, integration tests verify that components work together correctly, and the full pipeline tests ensure end to end functionality.

| Test File | Tests | Coverage |
|-----------|-------|----------|
| test_ingest.py | 11 | Document loading, chunking, knowledge base structure |
| test_answer.py | 13 | Context retrieval, question combination, prompt configuration |
| test_integration.py | 9 | Full ingestion pipeline, vectorstore operations, retrieval quality |

The test suite runs against the actual knowledge base and real ChromaDB instances rather than mocked dependencies. I made this choice deliberately because mocked tests can pass while the real system fails, which defeats the purpose of testing. The trade off is slightly longer test execution times, but 33 tests completing in under 45 seconds is acceptable for the confidence it provides.

Fixtures in `conftest.py` handle common setup like creating temporary knowledge bases and sample documents. Each test class groups related tests together, making it easy to run specific subsets when debugging a particular component.

### Running Tests

To run the full test suite with pytest:

```bash
uv run pytest tests/ -v
```

For coverage reporting that shows which lines of code are exercised:

```bash
uv run pytest tests/ --cov=src --cov-report=html
```

This generates an HTML report in `htmlcov/` that you can open in a browser to see exactly which code paths your tests cover. I aim for high coverage on the core modules while accepting that some UI code in `app.py` is better tested manually.

To run a specific test file or test class:

```bash
uv run pytest tests/test_ingest.py -v
uv run pytest tests/test_answer.py::TestFetchContext -v
```

### Continuous Integration

The project includes GitHub Actions workflows that run automatically on every push and pull request. The CI pipeline ensures that code changes do not introduce regressions before they reach the main branch.

**CI Workflow** runs the full test suite with coverage reporting. It sets up Python 3.13, installs dependencies using uv, runs the ingestion script to populate the vector database, and executes all tests. Failed tests block the pull request from merging.

**Lint Workflow** runs ruff for code quality checks. It catches common Python issues like unused imports, undefined variables, and formatting inconsistencies. I configured ruff to be strict enough to catch real problems without being annoying about stylistic preferences.

Both workflows use caching to speed up subsequent runs. The first run takes a few minutes to install dependencies, but subsequent runs reuse the cached environment and complete much faster.

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
