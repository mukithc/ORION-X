"""
ORION-X - Private AI Agent
Local AI with Grok/Manus/Claude/Emergent style, powered by Ollama.
"""

import gradio as gr

from agent import chat_simple, get_available_models
from config import DEFAULT_MODEL


def chat_fn(message, history, model):
    """Stream response for Gradio."""
    history = history or []
    for chunk in chat_simple(message, history, model=model):
        yield chunk


def build_ui():
    """Build the Gradio interface."""
    models = get_available_models()
    default = DEFAULT_MODEL if DEFAULT_MODEL in models else (models[0] if models else "llama2:latest")

    css = """
    .orion-header { text-align: center; padding: 1.5rem 0; }
    .orion-logo {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .orion-tagline { color: #64748b; font-size: 0.9rem; margin-top: 0.25rem; }
    .orion-footer { text-align: center; padding: 0.75rem; color: #64748b; font-size: 0.8rem; }
    """

    with gr.Blocks(
        title="ORION-X | Private AI",
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate"),
        css=css,
    ) as demo:
        gr.HTML(
            '<div class="orion-header">'
            '<div class="orion-logo">ORION-X</div>'
            '<p class="orion-tagline">Private AI · Powered by Ollama</p>'
            '</div>'
        )

        with gr.Row():
            model_dropdown = gr.Dropdown(
                choices=models,
                value=default,
                label="Model",
                scale=1,
            )

        chatbot = gr.Chatbot(
            height=500,
            show_copy_button=True,
        )

        with gr.Row():
            msg = gr.Textbox(
                placeholder="Throw me a hard one. I'm ready.",
                show_label=False,
                scale=9,
                container=False,
            )
            submit_btn = gr.Button("Send", variant="primary", scale=1)

        gr.Examples(
            examples=[
                "Plan a 3-day trip to Tokyo",
                "Calculate 123 * 456",
                "Search for latest AI news",
            ],
            inputs=msg,
            label="Try",
        )

        def respond(message, history, model):
            history = history or []
            for chunk in chat_fn(message, history, model):
                yield history + [(message, chunk)]

        msg.submit(
            respond,
            inputs=[msg, chatbot, model_dropdown],
            outputs=chatbot,
        ).then(lambda: "", outputs=msg)
        submit_btn.click(
            respond,
            inputs=[msg, chatbot, model_dropdown],
            outputs=chatbot,
        ).then(lambda: "", outputs=msg)

        gr.HTML('<div class="orion-footer">Calculator & web search · Local Ollama</div>')

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
