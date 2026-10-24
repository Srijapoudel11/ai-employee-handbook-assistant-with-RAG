# AI Employee Handbook Assistant with RAG

Starter template for the **Development of AI Applications** course final group project.

## Team members

- Poudel Srijan (srijan.poudel@student.hamk.fi )
- Luitel Subham (luitelsubham86@gmail.com)(amk1004106@student.hamk.fi)
- Imran Mohammad (amk1002049@student.hamk.fi)

## Problem

### Intended users
The primary users of this application are employees who need to find information about workplace policies and company procedures. Employees may need quick information about topics such as working hours, annual leave, sick leave, remote work, expenses, and workplace rules.

### Problem statement
Employee handbooks can contain many policies and procedures, making it time-consuming for employees to find the information they need. Employees may need to search through several sections of a handbook just to answer a simple workplace question.
Our application will help employees find relevant information from an employee handbook by allowing them to ask questions in natural language and receive clear answers based on the handbook content.

### Why AI is appropriate
Employees may ask the same workplace question in many different ways. Traditional keyword search may not always understand the meaning or context of a question.
An AI language model can understand natural-language questions and generate easy-to-understand answers. By combining the language model with RAG, the application can retrieve relevant information from the employee handbook and use that information when generating the answer.

## Solution

Our solution is an AI Employee Handbook Assistant with RAG.
The application will allow employees to ask questions about workplace policies using a simple Gradio interface. The RAG component will search the employee handbook and retrieve information that is relevant to the employee's question.
The retrieved information will be provided to the AI model as context. The model will then generate a clear answer based on the handbook information.
The application will also show the relevant source or handbook section when possible so that employees can see where the information came from.

## Main user workflow

1. **Ask a Question:** The employee enters a question about a workplace policy through the Gradio user interface.
2. **Processing & Guardrails:** The application service layer (`src/services/ai_service.py`) validates and formats the request.
3. **Information Retrieval:** The RAG component searches the employee handbook and retrieves the most relevant information for the user's question.
4. **Model Interaction:** The retrieved handbook information and the user's question are passed to the model through the application service.
5. **Model Response:** The model client calls Ollama locally and generates an answer based on the retrieved handbook information.
6. **Display Answer:** The answer and relevant source information are returned through the service layer and displayed in the Gradio user interface.

## Architecture

Below is the initial starter architecture. As your project evolves with additional capabilities, replace or extend this diagram in [`docs/architecture.md`](docs/architecture.md).

The application extends the starter architecture by adding a RAG component for retrieving relevant information from the employee handbook.

```text
User
  ↓
Gradio UI (app/ui.py)
  ↓
Application / AI Service (src/services/ai_service.py)
  ↓
RAG / Handbook Retrieval
  ↓
Model Client (src/models/model_client.py)
  ↓
Ollama (Local LLM Server)
  ↓
Generated Answer + Source
  ↓
Application Service
  ↓
Gradio UI
```

> **Core Architectural Rule:** The user interface must NEVER communicate directly with the model client or Ollama. All interactions must pass through the service layer (`ai_service.py`).

## Model

- **Model used:** `llama3.2` through Ollama.
- **Selection rationale:** We selected Llama 3.2 because it runs locally through Ollama and can generate natural-language answers using retrieved employee handbook information. The model is connected to our Gradio interface through the AI service layer.

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

We selected RAG because the application needs to answer questions using information from the employee handbook.
When an employee asks a question, the RAG component will search the handbook and retrieve information that is relevant to the question. The retrieved information will then be provided to the AI model as context.
This allows the AI model to generate answers based on the employee handbook instead of relying only on its general knowledge. The application can also show the relevant handbook section or source used to generate the answer.
RAG therefore directly supports the main purpose of our application: helping employees quickly find and understand workplace policies and procedures.

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

The AI Employee Handbook Assistant was evaluated using automated tests and manual testing with the fictional Fun Digital Solutions employee handbook.

### Automated testing

We ran `python -m pytest` after integrating the Gradio UI, Ollama model, and RAG code. All **10 automated tests passed**. The tests cover the AI service, demo integration, and handbook model functions.

### Manual RAG testing

| Test case | Observed result | Status |
|---|---|---|
| Load the Word handbook | Successfully extracted 10 handbook sections | Passed |
| Retrieve annual leave information | Retrieved Section 3. Annual Leave, with a match score of 9 | Passed |
| Ask about annual leave in Gradio | AI correctly answered 25 working days of paid annual leave | Passed |
| Display the handbook source | Displayed `3. Annual Leave — employee_handbook.docx` | Passed |
| Ask about a cafeteria lunch menu | AI stated that the information was not found and displayed no source | Passed |

### Evaluation observations

The application successfully retrieved relevant handbook information and generated a grounded answer for the tested annual leave question. It also handled the tested unsupported question without inventing a policy.

One issue was observed: the AI mentioned an unverified subsection, `3.2`, in its annual leave answer. This shows that source references still require careful verification. Additional question variations and failure scenarios have not yet been fully evaluated.

Further evaluation guidance and test cases are available in [`evaluation/README.md`](evaluation/README.md) and [`evaluation/test_cases.json`](evaluation/test_cases.json).

## Known limitations

The AI Employee Handbook Assistant has the following known limitations:

- **Keyword-based retrieval:** The RAG system uses keyword matching instead of semantic embeddings. Questions using unfamiliar wording may not retrieve the correct handbook section.
- **Single handbook:** The application currently uses one fictional employee handbook in DOCX format.
- **Source accuracy:** The AI may occasionally mention an incorrect subsection. During testing, it referred to Section 3.2, which was not verified.
- **Document formatting:** The handbook loader reads paragraphs under Word heading styles but does not extract information from tables.
- **Limited evaluation:** The application passed 10 automated tests and the documented manual tests, but additional question variations and error scenarios have not been fully evaluated.

## Future improvements

Possible future improvements include:

- Support for multiple employee handbooks and company policy documents
- Support for additional document formats
- Improved source references
- Improved RAG retrieval accuracy
- Conversation history
- Support for different organizations and their own employee handbooks
- Improvements based on evaluation results

  

## Recorded Group Presentation

Our final group presentation demonstrates the AI Employee Handbook Assistant with RAG.

All three group members explain their individual contributions, demonstrate the application, and discuss its architecture, testing, and limitations.

**Group Members:**
- Srijan Poudel — Gradio User Interface and System Integration
- Subham Luitel — Ollama Model Integration and Prompt Engineering
- Imran Mohammad — Employee Handbook Processing and RAG Retrieval

### Watch Our Presentation

[Watch the Final Group Presentation]((https://drive.google.com/file/d/1b_AVv9hV53hwbENUz6Y0jfV2dECQrXKQ/view?usp=sharing))
