import os
from pydub import AudioSegment

def convert_audio(input_file, target_format):
    if not input_file:
        return None, None
    try:
        audio = AudioSegment.from_file(input_file)
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}_converted.{target_format}"
        audio.export(output_file, format=target_format)
        return output_file, output_file  # one for download, one for playback
    except Exception as e:
        return None, f"❌ Conversion failed: {e}"
