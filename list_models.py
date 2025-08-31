from TTS.api import TTS

tts = TTS()
manager = tts.list_models()

models = manager.list_models()   # 🔑 second call returns the actual list

print("Available models:")
for i, m in enumerate(models, 1):
    print(f"{i}. {m}")
    if i >= 20:  # just print first 20
        break
