# 🎙️ WhatsApp Audio → Text Converter

I always felt the need to quickly turn a **WhatsApp voice note** into **text** — so I built this project for fun 🚀.

This small app takes audio (including **`.opus` WhatsApp recordings**) and converts it to **English text** using [Whisper](https://github.com/openai/whisper). The UI is powered by **Gradio** for a smooth upload-and-go experience.

---

## ✨ Features

* Upload **audio in any format** (opus, mp3, wav, m4a, ogg, etc.)
* Automatically converts and transcribes to **English text**
* Clean and simple **web UI** with Gradio
* Runs **locally for free** — no API costs

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone git@github.com:pranavsaji/whatsapp-audio-to-text.git
cd whatsapp-audio-to-text
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate.bat  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Also install **ffmpeg** (required by Pydub):

```bash
brew install ffmpeg      # macOS
sudo apt-get install ffmpeg   # Ubuntu/Debian
```

### 4. Run the app

```bash
python app.py
```

Then open the local link in your browser 🌐.


## 🤝 Why I Built This

Sometimes you just don’t want to listen to a long voice note.
I hacked this together quickly to make **voice → text transcription** super easy, especially for WhatsApp audios.

---

## 📜 License

MIT — free to use, modify, and share.


