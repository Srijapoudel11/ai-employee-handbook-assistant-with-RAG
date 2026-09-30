# AI Study Assistant with RAG

Starter template for the **Development of AI Applications** course final group project.

## Team members

- Poudel Srijan (srijan.poudel@student.hamk.fi )
- Luitel Subham (luitelsubham86@gmail.com)(amk1004106@student.hamk.fi)
- Imran Mohammad (amk1002049@student.hamk.fi)

## Problem

### Intended users
The primary users of this application are university students who
study using lecture notes, course materials, and PDF documents.
The application is especially useful for students who want to find
information from their study materials quickly and understand
difficult topics more easily.

### Problem statement
Students often have long lecture notes and PDF documents that contain
a large amount of information. Finding a specific answer from these
materials can take time, and some topics can be difficult to understand.
Our application will help students interact with their study materials
by allowing them to ask questions and receive answers based on the
content of their uploaded documents.

### Why AI is appropriate
Traditional search can find exact words or phrases, but students may
ask questions in many different ways. An AI language model can
understand natural-language questions, use relevant context from study
materials, and generate understandable explanations.
AI is therefore useful because the application needs to understand
questions and produce helpful answers rather than only perform exact
keyword matching.

## Solution

Our solution is an AI Study Assistant that allows students to provide
study materials and ask questions about them.
The application will retrieve relevant information from the student's
material and provide that information as context to an AI model. The
model will then generate an understandable answer.
This will help students find important information faster and make
their study materials easier to understand.

## Main user workflow

1. **Provide Study Material:** The user provides study material through the Gradio user interface.
2. **Ask a Question:** The user enters a question about the study material.
3. **Processing & Guardrails:** The application service layer validates the request and processes the user's question.
4. **Information Retrieval:** The RAG component searches the study material and retrieves relevant information.
5. **Model Response:** The relevant information and question are passed to the local AI model through the service layer.
6. **Answer:** The generated answer is returned to the user through the Gradio interface.

## Architecture

Below is the initial starter architecture. As your project evolves with additional capabilities, replace or extend this diagram in [`docs/architecture.md`](docs/architecture.md).

```text
User
  ↓
Gradio UI (app/ui.py)
  ↓
Application / AI Service (src/services/ai_service.py)
  ↓
Model Client (src/models/model_client.py)
  ↓
Ollama (Local LLM Server)
```

> **Core Architectural Rule:** The user interface must NEVER communicate directly with the model client or Ollama. All interactions must pass through the service layer (`ai_service.py`).

## Model

- **Model used:** `llama3.2` through Ollama
- **Selection rationale:** We plan to start with llama3.2 because it can run locally through Ollama and is suitable for developing and testing our AI study assistant. The final model choice may be adjusted during development after testing.

## Additional AI capability

Select at least one additional capability to implement for your final project:

- [x] RAG (Retrieval-Augmented Generation)
- [ ] Tools / External API integration
- [ ] Model Context Protocol (MCP)
- [ ] Agentic workflow (Model-selected actions based on observations)
- [ ] Memory / Persistent state
- [ ] Multimodal interaction (Text + Images)
- [ ] Other: ______________________

### Capability justification
RAG is useful for our application because students need answers that
are based on their own study materials.
Instead of relying only on the AI model's general knowledge, the
application will retrieve relevant information from the provided study
material and give that information to the model as context.
This should make the answers more relevant to the student's material
and also allows the application to show which source information was
used.

## Setup

### 1. Create the Conda environment

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

```bash
conda activate dev-ai-project
```

### 3. Configure environment variables

Copy `.env.example` to create your local `.env` configuration file:

On Linux / macOS:
```bash
cp .env.example .env
```

On Windows (Command Prompt / PowerShell):
```powershell
copy .env.example .env
```

Ensure `.env` contains valid values for `OLLAMA_BASE_URL` and `MODEL_NAME`:
```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.2
```

### 4. Start Ollama

Make sure Ollama is installed and running locally, then pull your configured model:

```bash
ollama run llama3.2
```

### 5. Run the application

Run the application from the root directory of the project:

```bash
python -m app.main
```

Then open your browser at `http://localhost:7860`.

### 6. Run automated tests

```bash
pytest
```

## Evaluation

The application will be evaluated after implementation using different
test cases to check whether it works correctly and provides useful
answers based on the uploaded study materials.

We plan to test:
- Questions that can be answered from the uploaded document
- Questions where the answer is not available in the document
- Empty or invalid user input
- Whether RAG retrieves relevant information
- Whether the generated answer is related to the retrieved information
- Error and failure scenarios

Detailed evaluation results will be added after the application has
been implemented and tested. Starter test cases can be found in [`evaluation/test_cases.json`](evaluation/test_cases.json).

Refer to [`evaluation/README.md`](evaluation/README.md) for guidelines on defining success, edge cases, and failure scenarios.

## Known limitations

- The project is currently in the proposal and early development stage.
Known limitations will be documented after implementation and testing.
Possible limitations may include model response quality, document
processing limitations, and the performance of the application on
different types of study materials.

## Future improvements

Possible future improvements include:

- Quiz generation from study materials
- Support for additional document formats
- Improved source citation
- Conversation history or memory
- Improvements based on evaluation results
- Automatic flashcard generation
- Improved document retrieval and ranking
- Support for multilingual questions and answers
- Personalized study recommendations
