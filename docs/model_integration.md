
# AI Model Component

Developer: Subham Luitel

## Model Selection

The application uses Llama 3.2 through local Ollama.

Llama 3.2 was selected for local AI inference because it can run without a paid cloud API and is suitable for our small employee handbook assistant.

## Prompt Engineering

File: `src/models/handbook_prompt.py`

Function: `build_handbook_prompt(question, handbook_context)`

The prompt instructs the model to:
- Answer using the provided handbook information.
- Avoid inventing company policies.
- Explain when the requested information is unavailable.
- Respond clearly and simply.

## Model Interaction

File: `src/models/model_client.py`

Method: `OllamaModelClient.generate_handbook_answer(question, handbook_context)`

The method receives an employee question and retrieved handbook text, creates the prompt, sends it to Llama 3.2, and returns an answer.

## Integration

Imran's RAG component will provide relevant handbook text.

The AI service layer will call `generate_handbook_answer()` and combine the answer with the handbook source.

Srijan's Gradio interface will receive the final result from the AI service layer.

The Gradio interface must not call Ollama directly.

## Testing

Manual tests:
- Question with available handbook information: Passed.
- Question without relevant handbook information: Passed.
- Empty handbook context: Passed.

Automated tests:
- 5 original tests passed.
- 3 new handbook model tests passed.
- Total: 8 tests passed.

The complete integrated application still requires further testing.
