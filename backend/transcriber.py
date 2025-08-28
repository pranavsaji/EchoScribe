import os
import tempfile
from pydub import AudioSegment
import whisper

def convert_to_wav(input_file: str) -> str:
    """
    Converts any audio format (mp3, wav, m4a, opus, ogg, etc.)
    to WAV (16kHz mono) for Whisper.
    """
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_frame_rate(16000).set_channels(1)
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    audio.export(temp_wav.name, format="wav")
    return temp_wav.name

def transcribe_audio(audio_file: str, model_size: str = "small") -> str:
    """
    Transcribes audio into English text using Whisper.
    """
    wav_file = convert_to_wav(audio_file)
    model = whisper.load_model(model_size)
    result = model.transcribe(wav_file, task="translate")  # always output English
    os.remove(wav_file)
    return result["text"]
