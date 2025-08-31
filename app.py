import os
import gradio as gr
from backend.transcriber import transcribe_audio
from backend.processor import (
    summarize_text,
    sentiment_analysis,
    extract_tasks,
    conversation_agent,
    translate_text,
)
from backend.voice_cloner import save_cloned_voice, list_saved_voices, generate_voice_reply
from backend.audio_converter import convert_audio
from backend.translator import translate_custom_text   # 👈 NEW

# -----------------------------
# State containers
# -----------------------------
transcript_state = {"text": ""}
conversation_history = []
ratings_log = []

# -----------------------------
# Supported languages
# -----------------------------
LANGUAGES = [
    "English", "Hindi", "Malayalam", "Tamil", "Telugu", "Kannada",
    "Bengali", "Marathi", "Gujarati", "Punjabi", "Urdu", "Odia",
    "Assamese", "Konkani", "Sanskrit", "Sindhi", "Kashmiri", "Manipuri",
    "Spanish", "French", "German", "Arabic", "Chinese", "Japanese"
]

# Map UI names → processor translate codes
LANG_CODE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Malayalam": "ml",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Odia": "or",
    "Assamese": "as",
    "Konkani": "kok",
    "Sanskrit": "sa",
    "Sindhi": "sd",
    "Kashmiri": "ks",
    "Manipuri": "mni",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Arabic": "ar",
    "Chinese": "zh",
    "Japanese": "ja",
}

# TTS supported langs
SUPPORTED_TTS_LANGS = [
    "English", "Hindi", "Spanish", "French", "German", "Italian",
    "Portuguese", "Polish", "Turkish", "Russian", "Dutch",
    "Czech", "Arabic", "Chinese", "Hungarian", "Korean", "Japanese"
]

TTS_LANG_CODE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Polish": "pl",
    "Turkish": "tr",
    "Russian": "ru",
    "Dutch": "nl",
    "Czech": "cs",
    "Arabic": "ar",
    "Chinese": "zh-cn",
    "Hungarian": "hu",
    "Korean": "ko",
    "Japanese": "ja",
}

# -----------------------------
# Core functions
# -----------------------------
def process(audio_file, target_lang):
    if audio_file is None:
        return "⚠️ Please upload an audio file.", "", "", ""

    transcript = transcribe_audio(audio_file)

    transcript_state["text"] = transcript
    transcript_output = transcript if target_lang.lower() == "english" else translate_text(transcript, target_lang)

    summary = summarize_text(transcript, target_lang)
    sentiment = sentiment_analysis(transcript, target_lang)
    tasks = extract_tasks(transcript, target_lang)

    return transcript_output, summary, sentiment, tasks


def handle_conversation(user_input, target_lang):
    global conversation_history
    conversation_history, _ = conversation_agent(
        transcript_state["text"], conversation_history, user_input, target_lang
    )
    return conversation_history


def rate_response(rating):
    if rating:
        ratings_log.append(int(rating))
        return f"⭐ Thanks! You rated the last response: {rating}/5"
    return "⚠️ Please select a rating."


# Save + refresh voices
def save_and_refresh(reference_audio, voice_name):
    status = save_cloned_voice(reference_audio, voice_name)
    voices = list_saved_voices()
    return status, gr.update(choices=voices, value=voice_name if voice_name in voices else None)


def handle_generate_voice(text, voice_name, target_lang):
    lang_code = TTS_LANG_CODE_MAP.get(target_lang, "en")
    return generate_voice_reply(text, voice_name, lang_code)

# -----------------------------
# Gradio App UI
# -----------------------------
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🎙️ EchoScribe – Multilingual WhatsApp Audio → Text + Groq LLMs + Voice Cloning")

    # -------- Tab 1: Transcription & Insights --------
    with gr.Tab("Transcription & Insights"):
        with gr.Row():
            audio_input = gr.Audio(type="filepath", label="Upload your audio")
            target_lang = gr.Dropdown(choices=LANGUAGES, value="English", label="Output Language")
        with gr.Row():
            transcript_box = gr.Textbox(label="📝 Transcript", lines=10)
            summary_box = gr.Textbox(label="📌 Summary", lines=5)
            sentiment_box = gr.Textbox(label="💡 Sentiment", lines=2)
            tasks_box = gr.Textbox(label="✅ Extracted Tasks", lines=5)
        transcribe_btn = gr.Button("🚀 Transcribe & Process")
        transcribe_btn.click(
            fn=process,
            inputs=[audio_input, target_lang],
            outputs=[transcript_box, summary_box, sentiment_box, tasks_box],
        )

    # -------- Tab 2: Conversation Agent --------
    with gr.Tab("Conversation Agent"):
        chat_box = gr.Chatbot(type="messages", label="💬 Conversation with Transcript")
        with gr.Row():
            user_input = gr.Textbox(label="Type your message", placeholder="e.g., 'Draft a reply to this audio'")
            target_lang_chat = gr.Dropdown(choices=LANGUAGES, value="English", label="Conversation Language")
        send_btn = gr.Button("Send")
        rating_dropdown = gr.Dropdown(choices=["1", "2", "3", "4", "5"], label="Rate the last response")
        rating_btn = gr.Button("Submit Rating")
        rating_output = gr.Textbox(label="Rating Status")

        send_btn.click(fn=handle_conversation, inputs=[user_input, target_lang_chat], outputs=chat_box)
        rating_btn.click(fn=rate_response, inputs=rating_dropdown, outputs=rating_output)

    # -------- Tab 3: Voice Cloning --------
    with gr.Tab("Voice Cloning"):
        gr.Markdown("### 🎤 Upload a reference voice and generate replies in that cloned voice.")
        with gr.Row():
            reference_audio = gr.Audio(type="filepath", label="Upload Reference Voice")
            voice_name = gr.Textbox(label="Voice Name", placeholder="e.g., Pranav Voice 1")
        save_btn = gr.Button("💾 Save Voice")
        save_status = gr.Textbox(label="Save Status")

        with gr.Row():
            available_voices = gr.Dropdown(choices=list_saved_voices(), label="Select Saved Voice")
            refresh_btn = gr.Button("🔄 Refresh Voices")

        save_btn.click(fn=save_and_refresh, inputs=[reference_audio, voice_name], outputs=[save_status, available_voices])
        refresh_btn.click(fn=list_saved_voices, outputs=available_voices)

        reply_input = gr.Textbox(label="Reply Text", placeholder="Type a reply to generate in cloned voice")
        reply_lang = gr.Dropdown(choices=SUPPORTED_TTS_LANGS, value="English", label="Reply Language")
        generate_btn = gr.Button("🎙️ Generate Voice Reply")
        reply_audio = gr.Audio(label="🔊 Generated Voice Reply")
        reply_file = gr.File(label="⬇️ Download Voice Reply")

        generate_btn.click(
            fn=handle_generate_voice,
            inputs=[reply_input, available_voices, reply_lang],
            outputs=[reply_file, reply_audio],
        )

    # -------- Tab 4: Audio Converter --------
    with gr.Tab("Audio Converter"):
        gr.Markdown("### 🎶 Convert audio files to different formats")
        with gr.Row():
            audio_input = gr.Audio(type="filepath", label="Upload Audio File")
            target_format = gr.Dropdown(choices=["wav", "mp3", "opus", "flac", "ogg", "m4a"], value="mp3", label="Output Format")
        convert_btn = gr.Button("🔄 Convert")
        converted_file = gr.File(label="⬇️ Converted File")
        converted_preview = gr.Audio(label="🎧 Preview Converted Audio")

        convert_btn.click(fn=convert_audio, inputs=[audio_input, target_format], outputs=[converted_file, converted_preview])

    # -------- Tab 5: Text Translator --------
    with gr.Tab("Text Translator"):
        gr.Markdown("### 🌍 Translate any text to your chosen language")
        input_text = gr.Textbox(label="Enter Text", lines=5, placeholder="Type or paste text here")
        target_lang_trans = gr.Dropdown(choices=LANGUAGES, value="Hindi", label="Translate To")
        translate_btn = gr.Button("🌐 Translate")
        output_text = gr.Textbox(label="Translated Text", lines=5)

        translate_btn.click(
            fn=translate_custom_text,
            inputs=[input_text, target_lang_trans],
            outputs=output_text,
        )

if __name__ == "__main__":
    demo.launch()

