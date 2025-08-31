import os
from groq import Groq
from dotenv import load_dotenv

# Load env vars
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("⚠️ GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)

def ask_groq(messages, model: str = "llama-3.3-70b-versatile") -> str:
    """
    Send conversation history (OpenAI-style dicts) to Groq and return latest response.
    """
    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

def conversation_agent(transcript: str, history: list, user_input: str, target_lang: str = "English") -> tuple:
    """
    Continue a conversation about the transcript or generate replies.
    Maintains history and includes transcript context at the start.
    Translates replies if target_lang is not English.
    """
    if not transcript:
        return history, "⚠️ Please transcribe an audio first."

    if not history:
        history = [
            {"role": "system", "content": "You are an assistant that helps interpret and respond to audio transcripts."},
            {"role": "system", "content": f"Transcript context:\n\n{transcript}"}
        ]

    history.append({"role": "user", "content": user_input})
    reply = ask_groq(history)

    if target_lang.lower() != "english":
        reply = translate_text(reply, target_lang)

    history.append({"role": "assistant", "content": reply})
    return history, reply

def summarize_text(text: str, target_lang: str = "English") -> str:
    summary = ask_groq([
        {"role": "user", "content": f"Summarize the following text in 3-4 sentences:\n\n{text}"}
    ])
    return translate_text(summary, target_lang) if target_lang.lower() != "english" else summary

def sentiment_analysis(text: str, target_lang: str = "English") -> str:
    sentiment = ask_groq([
        {"role": "user", "content": f"Perform sentiment analysis (positive, negative, neutral) on this text:\n\n{text}"}
    ])
    return translate_text(sentiment, target_lang) if target_lang.lower() != "english" else sentiment

def extract_tasks(text: str, target_lang: str = "English") -> str:
    tasks = ask_groq([
        {"role": "user", "content": f"Extract any tasks, action items, or reminders from this text. Format as a bullet list:\n\n{text}"}
    ])
    return translate_text(tasks, target_lang) if target_lang.lower() != "english" else tasks

def translate_text(text: str, target_lang: str) -> str:
    """
    Translate text into the target language using Groq.
    """
    if not text.strip():
        return ""
    return ask_groq([
        {"role": "user", "content": f"Translate the following into {target_lang}:\n\n{text}"}
    ])
