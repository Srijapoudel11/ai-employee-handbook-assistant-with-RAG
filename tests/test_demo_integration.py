
from src.services.ai_service import generate_demo_handbook_response


def test_empty_question():
    answer, source = generate_demo_handbook_response("")

    assert answer == "Please enter a message before sending."
    assert source == ""


def test_demo_answer_and_source(monkeypatch):
    class FakeModelClient:
        def generate_handbook_answer(self, question, handbook_context):
            assert question == "What are the normal working hours?"
            assert "9 AM to 5 PM" in handbook_context

            return "Employees work Monday to Friday, 9 AM to 5 PM."

    monkeypatch.setattr(
        "src.services.ai_service.OllamaModelClient",
        FakeModelClient
    )

    answer, source = generate_demo_handbook_response(
        "What are the normal working hours?"
    )

    assert "9 AM to 5 PM" in answer
    assert "DEMO ONLY" in source
    assert "RAG retrieval is not connected yet" in source
