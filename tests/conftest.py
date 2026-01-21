import shutil
import tempfile
from pathlib import Path

import pytest
from langchain_core.documents import Document


@pytest.fixture
def temp_knowledge_base():
    temp_dir = tempfile.mkdtemp()

    company_dir = Path(temp_dir) / "company"
    company_dir.mkdir()

    (company_dir / "overview.md").write_text(
        "# Company Overview\n\n"
        "Innovatech Solutions is a leading technology company "
        "specializing in enterprise software solutions. "
        "Founded in 2015, we have grown to serve over 500 clients worldwide."
    )

    (company_dir / "mission.md").write_text(
        "# Our Mission\n\n"
        "To empower businesses through innovative technology solutions "
        "that drive efficiency, growth, and digital transformation."
    )

    products_dir = Path(temp_dir) / "products"
    products_dir.mkdir()

    (products_dir / "synapse.md").write_text(
        "# SynapseEngine\n\n"
        "SynapseEngine is our flagship AI-powered analytics platform. "
        "It processes millions of data points in real-time, "
        "providing actionable insights for business intelligence. "
        "Key features include predictive analytics, natural language queries, "
        "and automated reporting dashboards."
    )

    yield temp_dir

    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_documents():
    return [
        Document(
            page_content="Innovatech Solutions was founded in 2015 by Dr. Elena Martinez.",
            metadata={"source": "/knowledge_base/company/about.md", "doc_type": "company"},
        ),
        Document(
            page_content="SynapseEngine is our flagship AI analytics platform with real-time processing.",
            metadata={"source": "/knowledge_base/products/synapse.md", "doc_type": "products"},
        ),
        Document(
            page_content="John Smith is the Chief Technology Officer at Innovatech Solutions.",
            metadata={"source": "/knowledge_base/employees/john_smith.md", "doc_type": "employees"},
        ),
    ]


@pytest.fixture
def sample_chunks(sample_documents):
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    return text_splitter.split_documents(sample_documents)
