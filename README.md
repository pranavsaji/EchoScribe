# 🎙️ EchoScribe – WhatsApp Audio → Text + Groq LLMs  

I always felt the need to quickly turn a **WhatsApp voice note** into **text**, and then *do something useful with it*.  
So I built **EchoScribe** 🚀 – a fun little project that transcribes WhatsApp audios and lets you **summarize, analyze sentiment, extract tasks, and even chat with the transcript** using Groq’s ultra-fast LLMs.  

---

## ✨ Features  

- 📥 **Upload WhatsApp audio** (supports `.opus`, `.mp3`, `.wav`, `.m4a`, `.ogg`, etc.)  
- 📝 **Transcription** – speech → English text (via Whisper)  
- 📌 **Summarization** – condense long audios into key points (Groq LLM)  
- 💡 **Sentiment Analysis** – detect positive / negative / neutral tone  
- ✅ **Task Extraction** – auto-detect action items & reminders  
- 💬 **Conversation Agent** – chat with your transcript, ask follow-ups, or draft replies  
- ⭐ **Rating System** – rate assistant responses (1–5) to track quality  

---

## 🛠️ Setup  

### 1. Clone the repo  
```bash
git clone git@github.com:pranavsaji/whatsapp-audio-to-text.git
cd whatsapp-audio-to-text
````

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

* **Transcription & Insights Tab** – Upload audio, see transcript, summary, sentiment, and tasks
* **Conversation Agent Tab** – Ask questions, request replies, or chat with your transcript
* **Ratings** – Quickly rate each assistant response from 1–5

---

## 🤝 Why I Built This

Voice notes are everywhere, especially on WhatsApp. But sometimes:

* They’re too long ⏳
* You only want the key points 📌
* You’d rather see action items or draft replies ✅

**EchoScribe** makes that **1-click easy**.

---

## 📜 License

MIT — free to use, modify, and share.

---

## 🚀 Future Ideas

* Save ratings & transcripts to a database for analytics
* Multi-language support (transcribe & keep original language)
* Export replies as ready-to-send WhatsApp messages
