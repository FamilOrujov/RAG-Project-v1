import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from implementation.ingest import KNOWLEDGE_BASE, create_chunks, fetch_documents


class TestFetchDocuments:
    def test_returns_list_of_documents(self):
        documents = fetch_documents()

        assert isinstance(documents, list)
        assert len(documents) > 0

    def test_documents_have_content(self):
        documents = fetch_documents()

        for doc in documents:
            assert hasattr(doc, "page_content")
            assert len(doc.page_content) > 0

    def test_documents_have_source_metadata(self):
        documents = fetch_documents()

        for doc in documents:
            assert "source" in doc.metadata
            assert doc.metadata["source"].endswith(".md")

    def test_documents_have_doc_type_metadata(self):
        documents = fetch_documents()

        valid_doc_types = {"company", "products", "employees", "contracts"}

        for doc in documents:
            assert "doc_type" in doc.metadata
            assert doc.metadata["doc_type"] in valid_doc_types

    def test_loads_all_knowledge_base_categories(self):
        documents = fetch_documents()

        doc_types = {doc.metadata["doc_type"] for doc in documents}
        expected_types = {"company", "products", "employees", "contracts"}

        assert doc_types == expected_types


class TestCreateChunks:
    def test_returns_list_of_chunks(self, sample_documents):
        chunks = create_chunks(sample_documents)

        assert isinstance(chunks, list)
        assert len(chunks) >= len(sample_documents)

    def test_chunks_preserve_metadata(self, sample_documents):
        chunks = create_chunks(sample_documents)

        for chunk in chunks:
            assert "source" in chunk.metadata
            assert "doc_type" in chunk.metadata

    def test_chunk_size_within_limits(self, sample_documents):
        chunks = create_chunks(sample_documents)

        max_chunk_size = 600

        for chunk in chunks:
            assert len(chunk.page_content) <= max_chunk_size

    def test_chunks_have_content(self, sample_documents):
        chunks = create_chunks(sample_documents)

        for chunk in chunks:
            assert len(chunk.page_content) > 0

    def test_real_documents_chunking(self):
        documents = fetch_documents()
        chunks = create_chunks(documents)

        assert len(chunks) > len(documents)

        doc_types_in_chunks = {chunk.metadata["doc_type"] for chunk in chunks}
        assert len(doc_types_in_chunks) == 4


class TestKnowledgeBaseStructure:
    def test_knowledge_base_directory_exists(self):
        assert os.path.exists(KNOWLEDGE_BASE)
        assert os.path.isdir(KNOWLEDGE_BASE)

    def test_knowledge_base_has_required_subdirectories(self):
        required_dirs = ["company", "products", "employees", "contracts"]

        for dir_name in required_dirs:
            dir_path = os.path.join(KNOWLEDGE_BASE, dir_name)
            assert os.path.exists(dir_path), f"Missing directory: {dir_name}"
            assert os.path.isdir(dir_path)

    def test_each_subdirectory_has_markdown_files(self):
        subdirs = ["company", "products", "employees", "contracts"]

        for subdir in subdirs:
            dir_path = os.path.join(KNOWLEDGE_BASE, subdir)
            md_files = list(Path(dir_path).glob("*.md"))
            assert len(md_files) > 0, f"No markdown files in {subdir}"
