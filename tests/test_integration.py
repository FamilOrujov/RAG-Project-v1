import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from implementation.ingest import create_chunks, fetch_documents


class TestIngestionPipeline:
    def test_full_ingestion_pipeline(self, temp_knowledge_base):
        from langchain_community.document_loaders import DirectoryLoader, TextLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        loader = DirectoryLoader(
            temp_knowledge_base,
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )
        documents = loader.load()

        assert len(documents) == 3

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        assert len(chunks) >= 3

        for chunk in chunks:
            assert len(chunk.page_content) > 0

    def test_vectorstore_creation_and_retrieval(self):
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
        )

        temp_db = tempfile.mkdtemp()

        try:
            documents = fetch_documents()
            chunks = create_chunks(documents)

            vectorstore = Chroma.from_documents(
                documents=chunks[:10], embedding=embeddings, persist_directory=temp_db
            )

            results = vectorstore.similarity_search("Innovatech Solutions", k=3)

            assert len(results) > 0
            assert all(hasattr(doc, "page_content") for doc in results)

        finally:
            shutil.rmtree(temp_db)

    def test_embedding_dimensions(self):
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
        )

        test_text = "This is a test sentence for embedding."
        embedding_vector = embeddings.embed_query(test_text)

        assert len(embedding_vector) == 384
        assert all(isinstance(x, float) for x in embedding_vector)


class TestRetrievalQuality:
    def test_company_query_retrieves_company_docs(self):
        from implementation.answer import fetch_context

        context = fetch_context("Tell me about Innovatech Solutions company")

        doc_types = [doc.metadata.get("doc_type", "") for doc in context]
        assert "company" in doc_types or any(
            "company" in str(doc.metadata.get("source", "")).lower() for doc in context
        )

    def test_product_query_retrieves_product_docs(self):
        from implementation.answer import fetch_context

        context = fetch_context("What products does Innovatech offer?")

        all_content = " ".join(doc.page_content.lower() for doc in context)
        assert any(
            keyword in all_content
            for keyword in ["product", "synapse", "clarity", "continuum", "echo", "guardian"]
        )

    def test_employee_query_retrieves_employee_docs(self):
        from implementation.answer import fetch_context

        context = fetch_context("Who are the employees at Innovatech?")

        doc_types = [doc.metadata.get("doc_type", "") for doc in context]
        has_employee_docs = "employees" in doc_types

        all_content = " ".join(doc.page_content.lower() for doc in context)
        has_employee_content = any(
            keyword in all_content
            for keyword in ["employee", "team", "staff", "manager", "director", "officer"]
        )

        assert has_employee_docs or has_employee_content


class TestEndToEndRAG:
    def test_rag_pipeline_returns_valid_response_structure(self):
        from implementation.answer import combined_question, fetch_context

        question = "What is the company mission?"
        history = []

        combined = combined_question(question, history)
        assert isinstance(combined, str)
        assert len(combined) > 0

        context = fetch_context(combined)
        assert isinstance(context, list)
        assert len(context) > 0

        context_text = "\n\n".join(doc.page_content for doc in context)
        assert len(context_text) > 0
