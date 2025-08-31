# 🎙️ EchoScribe – WhatsApp Audio → Text + Groq LLMs + Voice Cloning

I always felt the need to quickly turn a **WhatsApp voice note** into **text**, and then *do something useful with it*.
So I built **EchoScribe** 🚀 – a fun project that transcribes WhatsApp audios, generates insights, and now even lets you **clone voices, translate, and convert audio formats**.

---

## ✨ Features

**Upload WhatsApp audio** – supports `.opus`, `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac` and more
**Transcription** – speech → text (via Whisper)
**Summarization** – condense long audios into key points (Groq LLM)
**Sentiment Analysis** – detect positive / negative / neutral tone
**Task Extraction** – auto-detect action items & reminders
**Conversation Agent** – chat with your transcript, ask follow-ups, or draft replies
**Rating System** – rate assistant responses (1–5) to track quality
**Voice Cloning** – upload a reference voice, save it, and generate custom audio replies in that cloned voice
**Multi-Language Voice Reply** – generate replies in supported languages (English, Hindi, Spanish, French, Arabic, Japanese, etc.)
**Database-backed Voices** – all cloned voices are stored persistently in SQLite
**Audio Converter** – convert any audio file to different formats (`wav`, `mp3`, `opus`, `flac`, `ogg`, `m4a`)
**Text Translator** – translate any custom text into multiple languages instantly

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/pranavsaji/EchoScribe.git
cd EchoScribe
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
brew install ffmpeg          # macOS
sudo apt-get install ffmpeg  # Ubuntu/Debian
```

### 4. Add your Groq API Key

Create a `.env` file in the project root:

```ini
GROQ_API_KEY=your_api_key_here
```

### 5. Run the app

```bash
python app.py
```

Then open the local link in your browser 🌐.

---

## 📸 UI Overview

* **Transcription & Insights Tab** – Upload audio → get transcript, summary, sentiment & tasks
* **Conversation Agent Tab** – Chat with your transcript, draft replies, rate outputs
* **Voice Cloning Tab** – Upload & save voices, then generate replies in your chosen cloned voice
* **Audio Converter Tab** – Convert audio between formats (`wav`, `mp3`, `opus`, `flac`, `ogg`, `m4a`)
* **Text Translator Tab** – Translate any free text into multiple languages

---

## 🎤 Example

* Upload a **Malayalam WhatsApp voice note** → get an **English transcript & summary**
* Draft a reply in English → instantly generate a **Hindi voice reply in your cloned voice**
* Convert the reply to `.opus` format for **WhatsApp compatibility**
* Use the Translator tab to translate your draft reply into **Spanish, Arabic, Japanese**, etc.

---

## 🤝 Why I Built This

Voice notes are everywhere, especially on WhatsApp. But sometimes:

* They’re too long ⏳
* You only want the key points 📌
* You’d rather see action items or draft replies ✅
* Or you want to reply **in your own cloned voice** 🎙️

**EchoScribe** makes that **1-click easy**.

---

## 📜 License

MIT — free to use, modify, and share.

---

## 🚀 Future Ideas

* 🌐 Add **real-time streaming transcription**
* 📲 Export replies directly as **ready-to-send WhatsApp messages**
* 📊 Analytics dashboard for **ratings & usage insights**
* 🎛️ Fine-grained **voice controls** (pitch, speed, emotion)

