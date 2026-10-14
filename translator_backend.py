"""
translator_backend.py
---------------------
LCEL-based translation backend extracted from simplellmLCEL.ipynb.
Works both locally (reads .env) and on Streamlit Cloud (reads st.secrets).
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ── Load API keys: Streamlit Cloud Secrets OR local .env ─────────────────────
def _load_env():
    """
    Priority:
      1. Streamlit Cloud st.secrets (when deployed on cloud)
      2. .env file (when running locally)
    """
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets:
            os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
            return "streamlit_secrets"
    except Exception:
        pass

    # Fallback: search for .env in current dir and all parents
    current_dir = Path(__file__).resolve().parent
    for parent in [current_dir, *current_dir.parents]:
        candidate = parent / ".env"
        if candidate.exists():
            load_dotenv(dotenv_path=candidate, override=True)
            return f"dotenv:{candidate}"

    return None


_load_env()


# ── Available Groq models ─────────────────────────────────────────────────────
AVAILABLE_MODELS = {
    "GPT OSS 120B  (Default)": "openai/gpt-oss-120b",
    "Llama 3.3 70B": "llama-3.3-70b-versatile",
    "Llama 3.1 8B": "llama-3.1-8b-instant",
    "Gemma 2 9B": "gemma2-9b-it",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
}

# ── Supported target languages ────────────────────────────────────────────────
LANGUAGES = [
    "French", "Spanish", "German", "Italian", "Portuguese",
    "Hindi", "Gujarati", "Arabic", "Chinese (Simplified)",
    "Japanese", "Korean", "Russian", "Dutch", "Turkish",
    "Bengali", "Marathi", "Tamil", "Telugu", "Urdu",
    "Swedish", "Polish", "Greek", "Vietnamese", "Thai",
]


# ── LCEL Chain builder ────────────────────────────────────────────────────────
def build_chain(model_name: str = "openai/gpt-oss-120b"):
    """Build and return a translation LCEL chain for the given Groq model."""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError(
            "GROQ_API_KEY not found. "
            "Locally: add it to your .env file. "
            "On Streamlit Cloud: add it in App Settings > Secrets."
        )

    model = ChatGroq(model=model_name, groq_api_key=groq_api_key)

    generic_template = (
        "Translate the following into {language}. "
        "Return only the translated text, nothing else."
    )
    prompt = ChatPromptTemplate.from_messages(
        [("system", generic_template), ("user", "{text}")]
    )

    parser = StrOutputParser()

    # LCEL chain: prompt | model | parser  (exactly as in the notebook)
    chain = prompt | model | parser
    return chain


def translate(text: str, language: str, model_name: str = "openai/gpt-oss-120b") -> str:
    """
    Translate text to language using the LCEL chain.

    Args:
        text: Source text (any language).
        language: Target language name (e.g. "French").
        model_name: Groq model ID string.

    Returns:
        Translated string.
    """
    chain = build_chain(model_name)
    return chain.invoke({"language": language, "text": text})
