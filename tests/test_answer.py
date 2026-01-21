import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from implementation.answer import (
    RETRIEVAL_K,
    SYSTEM_PROMPT,
    combined_question,
    fetch_context,
)


class TestCombinedQuestion:
    def test_single_question_without_history(self):
        question = "What is Innovatech Solutions?"
        result = combined_question(question, [])

        assert question in result

    def test_combines_history_with_current_question(self):
        question = "Tell me more about the CEO"
        history = [
            {"role": "user", "content": "Who founded the company?"},
            {"role": "assistant", "content": "Dr. Elena Martinez founded the company."},
        ]

        result = combined_question(question, history)

        assert "Who founded the company?" in result
        assert "Tell me more about the CEO" in result

    def test_filters_out_assistant_messages(self):
        question = "Current question"
        history = [
            {"role": "user", "content": "User message 1"},
            {"role": "assistant", "content": "Assistant response"},
            {"role": "user", "content": "User message 2"},
        ]

        result = combined_question(question, history)

        assert "User message 1" in result
        assert "User message 2" in result
        assert "Assistant response" not in result

    def test_empty_history_returns_question(self):
        question = "What products do you offer?"
        result = combined_question(question, [])

        assert question in result

    def test_multiple_user_messages_concatenated(self):
        question = "Final question"
        history = [
            {"role": "user", "content": "First question"},
            {"role": "user", "content": "Second question"},
            {"role": "user", "content": "Third question"},
        ]

        result = combined_question(question, history)

        assert "First question" in result
        assert "Second question" in result
        assert "Third question" in result
        assert "Final question" in result


class TestFetchContext:
    def test_returns_list_of_documents(self):
        question = "What is Innovatech Solutions?"
        context = fetch_context(question)

        assert isinstance(context, list)

    def test_documents_have_page_content(self):
        question = "Tell me about the company"
        context = fetch_context(question)

        for doc in context:
            assert hasattr(doc, "page_content")
            assert len(doc.page_content) > 0

    def test_documents_have_metadata(self):
        question = "What products are available?"
        context = fetch_context(question)

        for doc in context:
            assert hasattr(doc, "metadata")
            assert "source" in doc.metadata

    def test_retrieves_relevant_context_for_company_query(self):
        question = "Tell me about Innovatech Solutions company history"
        context = fetch_context(question)

        all_content = " ".join(doc.page_content.lower() for doc in context)

        assert any(
            keyword in all_content for keyword in ["innovatech", "company", "founded", "mission"]
        )

    def test_retrieves_relevant_context_for_product_query(self):
        question = "What is SynapseEngine?"
        context = fetch_context(question)

        all_content = " ".join(doc.page_content.lower() for doc in context)

        assert "synapse" in all_content or "product" in all_content


class TestSystemPrompt:
    def test_system_prompt_contains_context_placeholder(self):
        assert "{context}" in SYSTEM_PROMPT

    def test_system_prompt_mentions_innovatech(self):
        assert "Innovatech" in SYSTEM_PROMPT

    def test_retrieval_k_is_reasonable(self):
        assert RETRIEVAL_K > 0
        assert RETRIEVAL_K <= 20
