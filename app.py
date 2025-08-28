import gradio as gr
from backend.transcriber import transcribe_audio

def process(audio_file):
    if audio_file is None:
        return "⚠️ Please upload an audio file."
    return transcribe_audio(audio_file)

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🎙️ Audio → English Text Converter")
    gr.Markdown("Upload audio (mp3, wav, m4a, opus, ogg, etc.) and get **English transcription** for free!")

    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="Upload your audio")
        output_text = gr.Textbox(label="Transcribed Text", lines=10)

    transcribe_btn = gr.Button("🚀 Transcribe")
    transcribe_btn.click(fn=process, inputs=audio_input, outputs=output_text)

    # Add ability to auto-run on upload
    audio_input.change(fn=process, inputs=audio_input, outputs=output_text)

if __name__ == "__main__":
    demo.launch()
