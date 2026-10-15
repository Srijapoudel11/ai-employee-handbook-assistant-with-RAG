from typing import Optional

from src.models.model_client import (
    OllamaModelClient,
    ModelClientError,
    OllamaConnectionError,
    ModelNotFoundError,
)
from src.schemas.responses import UserRequest, AIResponse
from src.rag_retriever import build_rag_prompt, retrieve_context


class AIService:
    """
    Application service layer responsible for validating user input,
    orchestrating model client requests, and catching exceptions gracefully.
    """

    def __init__(self, model_client: Optional[OllamaModelClient] = None):
        # Allow injecting custom/mock model_client for simple testing
        self.model_client = model_client

    def _get_client(self) -> OllamaModelClient:
        """Returns active model client, initializing default client if none provided."""
        if self.model_client is None:
            self.model_client = OllamaModelClient()
        return self.model_client

    def process_message(self, user_message: str) -> AIResponse:
        """
        Processes a raw user message string and returns a structured AIResponse.
        Catches technical failures and converts them to friendly user-facing messages.
        """

        # 1. Validate empty input
        if not user_message or not user_message.strip():
            return AIResponse(
                content="Please enter a message before sending.",
                success=False,
                error_message="User message was empty.",
            )

        try:
            # 2. Schema validation
            request = UserRequest(message=user_message.strip())

            # 3. Retrieve handbook context and build RAG prompt
            rag_prompt = build_rag_prompt(request.message)

            # 4. Send the RAG prompt to the model
            client = self._get_client()
            response_text = client.generate(rag_prompt)

            return AIResponse(
                content=response_text,
                success=True,
            )

        except OllamaConnectionError as err:
            return AIResponse(
                content=(
                    "[Error] Could not connect to Ollama.\n\n"
                    "Please verify that Ollama is installed and running locally "
                    "on your machine."
                ),
                success=False,
                error_message=str(err),
            )

        except ModelNotFoundError as err:
            return AIResponse(
                content=(
                    "[Error] The configured AI model is unavailable in Ollama.\n\n"
                    "Please verify your MODEL_NAME setting or run "
                    "'ollama run <model_name>'."
                ),
                success=False,
                error_message=str(err),
            )

        except ModelClientError as err:
            return AIResponse(
                content=(
                    "[Error] An unexpected communication error occurred "
                    "with the AI model."
                ),
                success=False,
                error_message=str(err),
            )

        except Exception as err:
            return AIResponse(
                content="[Error] An unexpected application error occurred.",
                success=False,
                error_message=str(err),
            )


def generate_response(
    user_message: str,
    service: Optional[AIService] = None
) -> str:
    """
    Main reusable service entry point used by the UI layer.

    Accepts user input message, passes it to the AI service,
    and returns the generated text response.
    """

    active_service = service or AIService()
    response = active_service.process_message(user_message)

    return response.content

    
def generate_demo_handbook_response(user_message: str) -> tuple[str, str]:
    """
    Temporarily connects the handbook AI model to Gradio.
    Uses fictional sample policies until RAG is ready.
    """

    if not user_message or not user_message.strip():
        return "Please enter a message before sending.", ""

    demo_context = (
        "Working Hours: Employees work Monday to Friday, "
        "9 AM to 5 PM.\n"
        "Remote Work: Employees can work remotely up to "
        "two days per week with supervisor approval."
    )

    try:
        client = OllamaModelClient()

        answer = client.generate_handbook_answer(
            user_message.strip(),
            demo_context
        )

        source = (
            "DEMO ONLY - Fictional sample handbook information. "
            "RAG retrieval is not connected yet."
        )

        return answer, source

    except OllamaConnectionError:
        return "Could not connect to Ollama. Check that Ollama is running.", ""

    except ModelNotFoundError:
        return "The configured AI model is not available in Ollama.", ""

    except ModelClientError:
        return "An error occurred while communicating with the AI model.", ""

    except Exception:
        return "An unexpected application error occurred.", ""

def generate_rag_handbook_response(user_message: str) -> tuple[str, str]:
    """Return an AI answer and its real handbook source."""

    if not user_message or not user_message.strip():
        return "Please enter a message before sending.", ""

    try:
        question = user_message.strip()
        result = retrieve_context(question)

        if not result["found"]:
            return "I could not find this information in the handbook.", ""

        response = AIService().process_message(question)

        if not response.success:
            return response.content, ""

        source = f"{result['section']} — employee_handbook.docx"
        return response.content, source

    except Exception:
        return "An error occurred while reading the employee handbook.", ""