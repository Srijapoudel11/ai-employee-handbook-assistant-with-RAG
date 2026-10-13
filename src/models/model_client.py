from typing import Optional
import ollama
from src.config import config
from src.models.handbook_prompt import build_handbook_prompt


class ModelClientError(Exception):
    """Base exception for model client failures."""
    pass


class OllamaConnectionError(ModelClientError):
    """Exception raised when Ollama service is unreachable."""
    pass


class ModelNotFoundError(ModelClientError):
    """Exception raised when the requested model is not found on local Ollama."""
    pass


class OllamaModelClient:
    """Encapsulates interaction with local Ollama inference server."""

    def __init__(self, base_url: Optional[str] = None, model_name: Optional[str] = None):
        self.base_url = base_url or config.ollama_base_url
        self.model_name = model_name or config.model_name
        self._client = ollama.Client(host=self.base_url)
    def generate_handbook_answer(
        self, question: str, handbook_context: str
    ) -> str:
        """
        Generates an answer using handbook information retrieved by RAG.
        """
        if not handbook_context or not handbook_context.strip():
            return "I could not find this information in the handbook."

        prompt = build_handbook_prompt(question, handbook_context)
        return self.generate(prompt)
    def generate(self, prompt: str) -> str:
        """
        Sends a user prompt to local Ollama model and returns generated response text.
        
        Raises ModelClientError subclass if connection or execution fails.
        """
        try:
            response = self._client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            
            # Standardize extraction from dict or chat response object
            if isinstance(response, dict):
                return response.get("message", {}).get("content", "")
            elif hasattr(response, "message") and hasattr(response.message, "content"):
                return response.message.content
            return str(response)

        except Exception as err:
            err_str = str(err).lower()
            if "connection" in err_str or "connect" in err_str or "refused" in err_str:
                raise OllamaConnectionError(
                    f"Failed to connect to Ollama service at {self.base_url}."
                ) from err
            elif "not found" in err_str or "404" in err_str:
                raise ModelNotFoundError(
                    f"Model '{self.model_name}' is not installed in local Ollama."
                ) from err
            else:
                raise ModelClientError(f"Error communicating with Ollama: {err}") from err
