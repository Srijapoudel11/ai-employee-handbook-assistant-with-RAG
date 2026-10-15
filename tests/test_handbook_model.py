
from src.models.handbook_prompt import build_handbook_prompt
from src.models.model_client import OllamaModelClient


def test_handbook_prompt_contains_question_and_context():
    question = "What are the working hours?"
    context = "Employees work Monday to Friday, 9 AM to 5 PM."

    prompt = build_handbook_prompt(question, context)

    assert question in prompt
    assert context in prompt


def test_empty_handbook_context():
    client = OllamaModelClient()

    answer = client.generate_handbook_answer(
        "How many annual leave days do employees receive?",
        ""
    )

    assert answer == "I could not find this information in the handbook."


def test_handbook_answer_uses_model(monkeypatch):
    client = OllamaModelClient()

    def fake_generate(prompt):
        assert "What are the working hours?" in prompt
        assert "9 AM to 5 PM" in prompt
        return "Employees work from 9 AM to 5 PM."

    monkeypatch.setattr(client, "generate", fake_generate)

    answer = client.generate_handbook_answer(
        "What are the working hours?",
        "Employees work Monday to Friday, 9 AM to 5 PM."
    )

    assert answer == "Employees work from 9 AM to 5 PM."
