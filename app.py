import gradio as gr
from backend.transcriber import transcribe_audio
from backend.processor import (
    summarize_text,
    sentiment_analysis,
    extract_tasks,
    conversation_agent,
)

# State containers
transcript_state = {"text": ""}
conversation_history = []
ratings_log = []  # store ratings per reply


def process(audio_file):
    if audio_file is None:
        return "⚠️ Please upload an audio file.", "", "", ""

    transcript = transcribe_audio(audio_file)
    transcript_state["text"] = transcript

    summary = summarize_text(transcript)
    sentiment = sentiment_analysis(transcript)
    tasks = extract_tasks(transcript)

    return transcript, summary, sentiment, tasks


def handle_conversation(user_input):
    global conversation_history
    conversation_history, _ = conversation_agent(
        transcript_state["text"], conversation_history, user_input
    )
    return conversation_history


def rate_response(rating):
    if rating:
        ratings_log.append(int(rating))
        return f"⭐ Thanks! You rated the last response: {rating}/5"
    return "⚠️ Please select a rating."


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🎙️ WhatsApp Audio → Text + Groq LLMs")
    gr.Markdown(
        "Upload audio → get transcript, insights, and then converse with the assistant about it."
    )

    with gr.Tab("Transcription & Insights"):
        with gr.Row():
            audio_input = gr.Audio(type="filepath", label="Upload your audio")
        with gr.Row():
            transcript_box = gr.Textbox(label="📝 Transcribed Text", lines=10)
            summary_box = gr.Textbox(label="📌 Summary", lines=5)
            sentiment_box = gr.Textbox(label="💡 Sentiment", lines=2)
            tasks_box = gr.Textbox(label="✅ Extracted Tasks", lines=5)
        transcribe_btn = gr.Button("🚀 Transcribe & Process")
        transcribe_btn.click(
            fn=process,
            inputs=audio_input,
            outputs=[transcript_box, summary_box, sentiment_box, tasks_box],
        )

    with gr.Tab("Conversation Agent"):
        chat_box = gr.Chatbot(type="messages", label="💬 Conversation with Transcript")
        user_input = gr.Textbox(
            label="Type your message or ask for a reply",
            placeholder="e.g., 'Draft a polite reply to this audio'",
        )
        send_btn = gr.Button("Send")

        rating_dropdown = gr.Dropdown(
            choices=["1", "2", "3", "4", "5"],
            label="Rate the last response (1=bad, 5=great)",
        )
        rating_btn = gr.Button("Submit Rating")
        rating_output = gr.Textbox(label="Rating Status")

        send_btn.click(fn=handle_conversation, inputs=user_input, outputs=chat_box)
        rating_btn.click(fn=rate_response, inputs=rating_dropdown, outputs=rating_output)

if __name__ == "__main__":
    demo.launch()
