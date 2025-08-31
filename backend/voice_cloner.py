import os
from pydub import AudioSegment
from TTS.api import TTS
import torch
from torch.serialization import add_safe_globals
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig
from backend.db import init_db, add_voice, list_voices, get_voice_path

# Init DB
init_db()

# Allowlist for PyTorch >= 2.6
add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])

MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
VOICES_DIR = "voices"
os.makedirs(VOICES_DIR, exist_ok=True)

def _load_tts():
    return TTS(MODEL_NAME)

def save_cloned_voice(reference_audio, voice_name):
    """Save uploaded audio as normalized wav + store in DB"""
    if not reference_audio or not voice_name:
        return "⚠️ Please upload an audio file and enter a name."

    ref_wav = os.path.join(VOICES_DIR, f"{voice_name}.wav")
    audio = AudioSegment.from_file(reference_audio)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(ref_wav, format="wav")

    # Store in DB
    add_voice(voice_name, ref_wav)

    return f"✅ Voice '{voice_name}' saved successfully!"

def list_saved_voices():
    """Return saved voice names from DB"""
    return list_voices()

def generate_voice_reply(text, voice_name, language="en"):
    """Generate reply in cloned voice and chosen language"""
    if not text:
        return None, None
    if not voice_name:
        return None, None

    ref_wav = get_voice_path(voice_name)
    if not ref_wav or not os.path.exists(ref_wav):
        return None, None

    tts = _load_tts()
    output_path = f"reply_{voice_name}.wav"

    tts.tts_to_file(
        text=text,
        speaker_wav=ref_wav,
        language=language,  # 👈 language now passed in
        file_path=output_path
    )
    return output_path, output_path  # file + preview

