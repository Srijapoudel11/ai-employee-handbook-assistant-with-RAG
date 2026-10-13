import gradio as gr
from src.services.ai_service import generate_demo_handbook_response


def build_ui() -> gr.Blocks:
    """
    Constructs the Gradio web interface.
    
    Architectural Principle: The UI communicates strictly with `generate_response()`
    in the AI service layer and never directly with Ollama or the model client.
    """
    with gr.Blocks(title="AI Employee Handbook Assistant") as demo:
        gr.Markdown(
            """
            # AI Employee Handbook Assistant
            
            Welcome to the AI Employee Handbook Assistant!

            Ask questions about workplace policies, working hours, annual leave, sick leave, remote work, and company procedures.
            """
        )
        gr.Markdown(
            """
            ### How to Use
            1. Enter your question about company policies.
            2. Click **Ask AI** to receive an answer.
            3. Check the **Handbook Source** for the relevant policy section.
            4. Click **Clear** to ask a new question.
            """
        
        )

        with gr.Row():
            user_input = gr.Textbox(
                lines=3,
                placeholder="Example: How many days of annual leave do I get?",
                label="Ask a Question About Your Employee Handbook",
            )
        gr.Examples(
            examples=[
                ["What are the normal working hours?"],
                ["How many days of annual leave do employees receive?"],
                ["What should I do if I am sick?"],
                ["Can employees work remotely?"],
                ["How can I claim travel expenses?"],
            ],
            inputs=user_input,
        )
        submit_btn = gr.Button("Ask AI", variant="primary")

        with gr.Row():
            output_box = gr.Textbox(
                lines=8,
                label="Answer from Employee Handbook Assistant",
                interactive=False,
            )
        source_box = gr.Textbox(
            lines=2,
            label="Handbook Source",
            interactive=False,
        )
        gr.ClearButton(components=[user_input, output_box, source_box], value="Clear")
        # Connect UI actions exclusively to the service layer function
        
        submit_btn.click(
            fn=generate_demo_handbook_response,
            inputs=user_input,
            outputs=[output_box, source_box],
        )

        user_input.submit(
            fn=generate_demo_handbook_response,
            inputs=user_input,
            outputs=[output_box, source_box],
        )
    return demo
