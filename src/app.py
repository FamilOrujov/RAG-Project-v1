import gradio as gr
from dotenv import load_dotenv

from implementation.answer import answer_question

load_dotenv(override=True)


def format_context(context):
    if not context:
        return """
<div style="height: 100%; display: flex; align-items: center; justify-content: center; text-align: center; color: #888;">
    <div>
        <p style="font-size: 1.1em; margin-bottom: 8px;">No context retrieved yet</p>
        <p style="font-size: 0.9em;">Ask a question to see relevant documents</p>
    </div>
</div>
"""

    result = """
<div style="padding: 10px;">
    <h3 style="color: #6366f1; margin-bottom: 20px; border-bottom: 2px solid #6366f1; padding-bottom: 10px;">
        Retrieved Documents
    </h3>
"""

    for i, doc in enumerate(context, 1):
        source = doc.metadata.get("source", "Unknown")
        source_name = source.split("/")[-1] if "/" in source else source
        doc_type = doc.metadata.get("doc_type", "document")

        result += f"""
<div style="background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3d 100%); 
            border-radius: 12px; 
            padding: 16px; 
            margin-bottom: 16px;
            border-left: 4px solid #6366f1;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <span style="color: #6366f1; font-weight: 600; font-size: 0.9em;">
            Source #{i}
        </span>
        <span style="background: #6366f1; color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.75em; text-transform: uppercase;">
            {doc_type}
        </span>
    </div>
    <div style="color: #a5b4fc; font-size: 0.85em; margin-bottom: 8px;">
        {source_name}
    </div>
    <div style="color: #e2e8f0; font-size: 0.9em; line-height: 1.6;">
        {doc.page_content}
    </div>
</div>
"""

    result += "</div>"
    return result


def chat(history):
    if not history:
        return history, format_context([])

    last_message = history[-1]["content"]
    prior = history[:-1]
    answer, context = answer_question(last_message, prior)
    history.append({"role": "assistant", "content": answer})
    return history, format_context(context)


def main():
    def put_message_in_chatbot(message, history):
        if not message.strip():
            return "", history
        return "", history + [{"role": "user", "content": message}]

    custom_css = """
    .gradio-container {
        max-width: 1800px !important;
        padding: 20px !important;
    }
    
    #main-row {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 24px !important;
        align-items: stretch !important;
    }
    
    #chat-column, #context-column {
        min-width: 0 !important;
        display: flex !important;
        flex-direction: column !important;
    }
    
    .header-container {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d3d 100%);
        border-radius: 16px;
        border: 1px solid #3d3d5c;
    }
    
    .header-title {
        font-size: 2em;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    
    .header-subtitle {
        color: #888;
        font-size: 1em;
    }
    
    .context-panel {
        height: 665px !important;
        min-height: 665px !important;
        max-height: 665px !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        background: #1e1e2e;
        border-radius: 12px;
        border: 1px solid #3d3d5c;
        padding: 10px;
        box-sizing: border-box;
    }
    
    .context-panel > div {
        overflow: visible !important;
        max-height: none !important;
    }
    
    .context-panel::-webkit-scrollbar {
        width: 8px;
    }
    
    .context-panel::-webkit-scrollbar-track {
        background: #1e1e2e;
        border-radius: 4px;
    }
    
    .context-panel::-webkit-scrollbar-thumb {
        background: #6366f1;
        border-radius: 4px;
    }
    
    .context-panel::-webkit-scrollbar-thumb:hover {
        background: #4f46e5;
    }
    
    footer {
        display: none !important;
    }
    
    @media (max-width: 900px) {
        #main-row {
            grid-template-columns: 1fr !important;
        }
    }
    """

    theme = gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="purple",
        neutral_hue="slate",
        font=["Inter", "system-ui", "sans-serif"],
    ).set(
        body_background_fill="#0f0f1a",
        body_background_fill_dark="#0f0f1a",
        block_background_fill="#1e1e2e",
        block_background_fill_dark="#1e1e2e",
        block_border_color="#3d3d5c",
        block_border_color_dark="#3d3d5c",
        block_label_text_color="#a5b4fc",
        block_label_text_color_dark="#a5b4fc",
        block_title_text_color="#e2e8f0",
        block_title_text_color_dark="#e2e8f0",
        input_background_fill="#2d2d3d",
        input_background_fill_dark="#2d2d3d",
        input_border_color="#3d3d5c",
        input_border_color_dark="#3d3d5c",
        button_primary_background_fill="#6366f1",
        button_primary_background_fill_dark="#6366f1",
        button_primary_background_fill_hover="#4f46e5",
        button_primary_background_fill_hover_dark="#4f46e5",
    )

    with gr.Blocks(title="Innovatech Solutions Assistant", theme=theme, css=custom_css) as ui:
        gr.HTML("""
        <div class="header-container">
            <div class="header-title">Innovatech Solutions Assistant</div>
            <div class="header-subtitle">AI powered knowledge base for enterprise information</div>
        </div>
        """)

        with gr.Row(elem_id="main-row"):
            with gr.Column(elem_id="chat-column"):
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=600,
                    type="messages",
                    show_copy_button=True,
                    avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=innovatech"),
                    bubble_full_width=False,
                )

                with gr.Row():
                    message = gr.Textbox(
                        placeholder="Ask anything about company",
                        show_label=False,
                        scale=9,
                        container=False,
                    )
                    submit_btn = gr.Button(
                        "Send",
                        variant="primary",
                        scale=1,
                        min_width=80,
                    )

            with gr.Column(elem_id="context-column"):
                context_panel = gr.HTML(
                    value=format_context([]),
                    elem_classes=["context-panel"],
                )

        message.submit(
            put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]
        ).then(chat, inputs=chatbot, outputs=[chatbot, context_panel])

        submit_btn.click(
            put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]
        ).then(chat, inputs=chatbot, outputs=[chatbot, context_panel])

    ui.launch(inbrowser=True)


if __name__ == "__main__":
    main()
