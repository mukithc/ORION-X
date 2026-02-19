"""
Private AI Agent - GUI
A local agent with Grok/Manus/Claude/Emergent style, powered by Ollama.
"""

import gradio as gr

from agent import chat_simple, get_available_models
from config import DEFAULT_MODEL


def chat_fn(message, history, model):
    """Stream response for Gradio ChatInterface."""
    history = history or []
    for chunk in chat_simple(message, history, model=model):
        yield chunk


def build_ui():
    """Build the Gradio interface."""
    models = get_available_models()
    default = DEFAULT_MODEL if DEFAULT_MODEL in models else (models[0] if models else "llama2:latest")

    with gr.Blocks(
        title="Private AI Agent",
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate"),
    ) as demo:
        gr.Markdown(
            """
            # 🤖 Private AI Agent
            **Grok + Manus + Claude + Emergent** — Your local autonomous agent.  
            Plan tasks, get results, no cloud. Powered by Ollama.
            """
        )

        model_dropdown = gr.Dropdown(
            choices=models,
            value=default,
            label="Model",
        )

        def chat_with_model(message, history, model):
            yield from chat_fn(message, history, model)

        gr.ChatInterface(
            fn=chat_with_model,
            additional_inputs=[model_dropdown],
            chatbot=gr.Chatbot(height=450, show_copy_button=True),
            textbox=gr.Textbox(
                placeholder="Ask me anything. Give me a task. I'll plan and execute...",
                container=False,
                scale=7,
            ),
            title=None,
            description=None,
            examples=[
                "Plan a 3-day trip to Tokyo",
                "Write a Python script to sort a list",
                "Explain quantum computing in simple terms",
            ],
        )

        gr.Markdown(
            """
            ---
            *Uses your local Ollama models. No API keys. Data stays on your machine.*
            """
        )

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
    )
