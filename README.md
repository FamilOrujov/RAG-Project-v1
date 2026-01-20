#  RAG Project v1: Innovatech Solutions AI Assistant

<div align="center">

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-1.0-green.svg)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.3-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**My Retrieval-Augmented Generation (RAG) system v1 for intelligent enterprise knowledge management**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage)

</div>

---

## Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [Knowledge Base](#-knowledge-base)
- [Configuration](#-configuration)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## Overview

**RAG Project v1** is a production-ready Retrieval-Augmented Generation system built for **Innovatech Solutions**, demonstrating how AI can transform enterprise knowledge management. The system enables natural language queries over organizational data including company information, products, employees, and contracts.


## Features

!-+!

---

## Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.13 | Main programming language |
| **LLM Framework** | LangChain v1.0 | Orchestration and RAG pipeline |
| **Vector Database** | ChromaDB | Embeddings storage and retrieval |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) | Document and query embeddings |
| **LLM** | OpenAI / Ollama (Gemma3 4B) | Response generation |
| **UI Framework** | Gradio | Web interface |
| **Text Processing** | LangChain Text Splitters | Document chunking |




## Project Structure

```
RAG-Project-v1/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── pyproject.toml                     # Project configuration (uv)
├── uv.lock                            # Dependency lock file
├── .gitignore                         # Git ignore rules
├── .env                               # Environment variables (create this)
│
└── src/                               # Main application folder
    ├── app.py                         # Main Gradio web application (START HERE)
    │
    ├── implementation/                # Core RAG implementation
    │   ├── ingest.py                  # Document ingestion & embedding creation
    │   └── answer.py                  # RAG pipeline & question answering
    │
    ├── knowledge_base/                # Source documents (31 .md files)
    │   ├── company/                   # Company information (4 docs)
    │   │   ├── about.md
    │   │   ├── careers.md
    │   │   ├── culture.md
    │   │   └── overview.md
    │   │
    │   ├── products/                  # Product documentation (5 docs)
    │   │   ├── ClarityLens.md
    │   │   ├── Continuum.md
    │   │   ├── EchoSphere.md
    │   │   ├── Guardian.md
    │   │   └── SynapseEngine.md
    │   │
    │   ├── employees/                 # Employee profiles (10 docs)
    │   │   ├── Gideon Cross.md
    │   │   ├── Isolde Beaumont.md
    │   │   ├── Jia Li.md
    │   │   ├── Kaelen Vance.md
    │   │   ├── Linnea Vega.md
    │   │   ├── Orion Fletcher.md
    │   │   ├── Ronan Dexter.md
    │   │   ├── Seraphina Jones.md
    │   │   ├── Silas Thorne.md
    │   │   └── Tessa McRae.md
    │   │
    │   └── contracts/                 # Business contracts (12 docs)
    │       ├── API Data License with Veridian Datafeeds for InsightIQ.md
    │       ├── Cloud Services Agreement with Stratus Infrastructure for Hosting.md
    │       ├── Co-Marketing Agreement with Orion CRM for SynapseChat Integration.md
    │       ├── Consulting Agreement with Navigator Strategy for APAC GTM.md
    │       ├── Data Processing Addendum with Zenith Financial Group for InsightIQ.md
    │       ├── Hybrid MSA with Fusion Robotics for NexusFlow and CoreLLM.md
    │       ├── Master Service Agreement with Momentum Machines for NexusFlow.md
    │       ├── Master Service Agreement with Silverline Logistics for NexusFlow.md
    │       ├── OEM Partnership Agreement with Quantum Leap AI for CoreLLM API.md
    │       ├── Office Lease Agreement with Cityscape Realty for SF Headquarters.md
    │       ├── Reseller Agreement with Catalyst Partners for EMEA Region.md
    │       └── Statement of Work with Cygnus Security for Penetration Test.md
    │
    ├── experiments/                   # Jupyter notebooks for testing
    │   └── experiment.ipynb           # RAG experimentation notebook
    │
    └── vector_db/                     # ⚠️ Auto-generated (gitignored)
        └── [Created locally when you run ingest.py]

Note: vector_db/ folders are auto-generated and not tracked in Git
```

---

## Installation

### Prerequisites

- **Git** (for cloning the repository)
- **OpenAI API Key** OR **Ollama** installed locally (for local LLMs)

### Step 1: Clone the Repository

```bash
git clone https://github.com/FamilOrujov/RAG-Project-v1.git
cd RAG-Project-v1
```

### Step 2: Create Virtual Environment

#### Using venv (Standard Python)
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

#### Using uv (Faster Alternative)
```bash
uv venv
uv sync
```

### Step 3: Install Dependencies (if you're not using uv package manager)

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# For OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Other API keys
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```

### Step 5: Download Ollama (Optional - For Local LLMs)

If you want to use local models instead of OpenAI:

1. Download and install [Ollama](https://ollama.ai/)
2. Pull a model:
```bash
ollama pull gemma3:3b
# or
ollama pull llama3.1:8b
```

---

## Usage

### Quick Start

#### 1. Ingest Documents (First Time Setup)

This step processes all documents in the `knowledge_base/` folder, creates embeddings, and stores them in ChromaDB.

```bash
cd src
python implementation/ingest.py
```

**Expected Output:**
```
There are 156 vectors with 384 dimensions in the vector store
Ingestion complete
```

#### 2. Launch the Web Interface

```bash
python app.py
```

The Gradio interface will open in your browser at `http://localhost:7860`

### Using the Application

1. **Ask Questions**: Type your question in the text box
2. **View Responses**: The AI assistant will provide an answer
3. **Check Sources**: The right panel shows which documents were used
4. **Continue Conversation**: Ask follow-up questions for context-aware responses

### Example Queries

```
❓ What products does Innovatech Solutions offer?
❓ Tell me about the company's mission and vision
❓ Who is Seraphina Jones and what does she do?
❓ What is the NexusFlow platform?
❓ Tell me about the contract with Momentum Machines
❓ What are the key features of the Synapse Engine?
```

---

## Architecture

### RAG Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         RAG PIPELINE                            │
└─────────────────────────────────────────────────────────────────┘

1. INGESTION PHASE (One-time / When knowledge base updates)
   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │  Load Docs   │ ───> │ Split Chunks │ ───> │   Embed &    │
   │  from KB     │      │  (500 chars) │      │   Store in   │
   └──────────────┘      └──────────────┘      │   ChromaDB   │
                                               └──────────────┘

2. QUERY PHASE (Real-time)
   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │ User Query   │ ───> │   Embed &    │ ───> │   Retrieve   │
   │              │      │ Vector Search│      │  Top K Docs  │
   └──────────────┘      └──────────────┘      └──────────────┘
                                                       │
                                                       v
   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │   Return     │ <─── │     LLM      │ <─── │   Format     │
   │   Answer     │      │   Generate   │      │   Prompt     │
   └──────────────┘      └──────────────┘      └──────────────┘
```

### Component Details

#### 1. Document Ingestion (`ingest.py`)

**Purpose**: Process raw documents and create searchable embeddings

**Steps**:
1. **Load Documents**: Scans `knowledge_base/` for all `.md` files
2. **Add Metadata**: Tags documents with type (company, products, employees, contracts)
3. **Text Splitting**: 
   - Chunk size: 500 characters
   - Overlap: 200 characters (preserves context)
4. **Embedding Creation**: Uses `all-MiniLM-L6-v2` (384 dimensions)
5. **Vector Storage**: Stores in ChromaDB at `src/vector_db/`

**Key Functions**:
- `fetch_documents()`: Loads all markdown files with metadata
- `create_chunks()`: Splits documents into overlapping chunks
- `create_embeddings()`: Creates and stores vector embeddings

#### 2. Question Answering (`answer.py`)

**Purpose**: Handle user queries and generate responses using RAG

**Steps**:
1. **Query Processing**: Combines current question with conversation history
2. **Retrieval**: Fetches top K=10 most relevant document chunks
3. **Context Formatting**: Assembles retrieved documents into context
4. **Prompt Construction**: Injects context into system prompt
5. **LLM Generation**: Generates response using chat history
6. **Response Return**: Returns answer + source documents

**Key Functions**:
- `fetch_context()`: Retrieves relevant documents via semantic search
- `combined_question()`: Merges conversation history for better retrieval
- `answer_question()`: Main RAG pipeline orchestration

#### 3. Web Interface (`app.py`)

**Purpose**: User-friendly Gradio interface for interaction

**Features**:
- Two-column layout: Chat on left, sources on right
- Real-time streaming responses
- Copy button for answers
- Formatted source attribution with highlighting
- Conversation history management

---

## Knowledge Base

### Structure

Inside the knowledge_base folder, you'll see 4 folders: company, contracts, employees, and products. All the .md files inside are **synthetic data**, which I created using Frontier LLMs (ChatGPT 5 and Gemini 2.5 pro).

The knowledge base contains **31 markdown documents** across 4 categories:

| Category | Count | Description |
|----------|-------|-------------|
| **Company** | 4 docs | Mission, culture, history, careers |
| **Products** | 5 docs | SynapseEngine, ClarityLens, Continuum, EchoSphere, Guardian |
| **Employees** | 10 docs | Employee profiles with roles and responsibilities |
| **Contracts** | 12 docs | Business agreements, MSAs, partnerships |



## Configuration

### Key Parameters

Edit these in `answer.py` and `ingest.py`:

#### Retrieval Settings (`answer.py`)

```python
RETRIEVAL_K = 10  # Number of document chunks to retrieve
                  # Higher = more context, slower responses
                  # Lower = faster, potentially less comprehensive
```

#### Chunking Settings (`ingest.py`)

```python
chunk_size = 500       # Characters per chunk
chunk_overlap = 200    # Overlap between chunks (preserves context)
```

#### Model Selection (`answer.py`)

**Option 1: OpenAI API**
```python
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
```

**Option 2: Local LLM (Ollama)**
```python
llm = ChatOpenAI(
    temperature=0.7, 
    model_name='gemma2:2b',  # or llama3.1:8b
    base_url='http://localhost:11434/v1', 
    api_key='ollama'
)
```

#### Embedding Model (`ingest.py` and `answer.py`)

```python
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# Alternatives:
# - all-mpnet-base-v2 (higher quality, slower)
# - all-MiniLM-L12-v2 (balanced)
```

---

## Development

### Project Structure for Developers

- **`implementation/ingest.py`**: Modify document loading, chunking strategy, embedding model
- **`implementation/answer.py`**: Customize RAG pipeline, prompts, retrieval strategy
- **`app.py`**: Change UI, add features, modify chat interface
- **`experiments/`**: Jupyter notebooks for testing and experimentation

### Running Experiments

The `experiments/` folder contains Jupyter notebooks for testing:

```bash
cd src/experiments
jupyter notebook experiment.ipynb
```

### Testing Different Configurations

1. **Test Chunk Sizes**: Modify `chunk_size` in `ingest.py` and re-ingest
2. **Test Retrieval K**: Adjust `RETRIEVAL_K` in `answer.py` and restart app
3. **Test Different LLMs**: Change model in `answer.py`
4. **Test Different Embeddings**: Change embedding model and re-ingest

### Debugging

Enable verbose output by adding to `answer.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)



