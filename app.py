"""
app.py  -  LinguaLCEL: LangChain LCEL Language Translator
A premium Streamlit web app showcasing LangChain Expression Language (LCEL)
for real-time multi-language text translation powered by Groq AI models.
"""

import streamlit as st
import time
from translator_backend import translate, AVAILABLE_MODELS, LANGUAGES

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LinguaLCEL | AI Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 35%, #112240 70%, #0a0a1a 100%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }

.hero-header { text-align: center; padding: 2.5rem 1rem 1.5rem; margin-bottom: 1.5rem; }
.hero-badge {
    display: inline-block;
    background: rgba(99,179,237,0.15); border: 1px solid rgba(99,179,237,0.4);
    color: #63b3ed; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.15em;
    text-transform: uppercase; padding: 0.35rem 1rem; border-radius: 20px; margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.5rem); font-weight: 800; line-height: 1.1;
    background: linear-gradient(135deg, #e2e8f0 0%, #63b3ed 40%, #9f7aea 80%, #f687b3 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin: 0.5rem 0;
}
.hero-subtitle { color: #94a3b8; font-size: 1.05rem; max-width: 540px; margin: 0 auto; line-height: 1.6; }

.glass-card {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; padding: 1.8rem; backdrop-filter: blur(12px);
    margin-bottom: 1rem;
}

.section-label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #63b3ed; margin-bottom: 0.5rem;
}

.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important; color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important; font-size: 1rem !important; resize: vertical !important;
}
.stTextArea textarea:focus { border-color: rgba(99,179,237,0.6) !important; box-shadow: 0 0 0 3px rgba(99,179,237,0.08) !important; }

.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #6366f1, #8b5cf6) !important;
    color: white !important; border: none !important; border-radius: 14px !important;
    font-size: 1rem !important; font-weight: 600 !important; width: 100% !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 30px rgba(99,102,241,0.5) !important; }
.stButton > button:active { transform: translateY(0px) !important; }

.translation-output {
    background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(139,92,246,0.08));
    border: 1.5px solid rgba(99,179,237,0.25); border-radius: 16px;
    padding: 1.5rem 1.8rem; margin-top: 0.5rem; min-height: 100px;
    position: relative; overflow: hidden;
}
.translation-output::before {
    content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6, #f472b6);
}
.translation-text { color: #f1f5f9; font-size: 1.1rem; line-height: 1.75; word-break: break-word; }
.translation-lang-tag {
    display: inline-block; background: rgba(99,179,237,0.15); border: 1px solid rgba(99,179,237,0.3);
    color: #63b3ed; font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.1em; padding: 0.2rem 0.7rem; border-radius: 10px; margin-bottom: 0.75rem;
}

.stats-bar { display: flex; gap: 1rem; margin-top: 0.5rem; flex-wrap: wrap; }
.stat-chip {
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px; padding: 0.3rem 0.8rem; font-size: 0.75rem; color: #94a3b8;
}
.stat-chip span { color: #63b3ed; font-weight: 600; }

section[data-testid="stSidebar"] {
    background: rgba(10,10,26,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}

.history-item {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem;
    transition: border-color 0.2s;
}
.history-item:hover { border-color: rgba(99,179,237,0.2); }
.history-original { font-size: 0.8rem; color: #64748b; margin-bottom: 0.4rem; }
.history-translated { font-size: 0.92rem; color: #e2e8f0; line-height: 1.5; }
.history-meta { font-size: 0.72rem; color: #475569; margin-top: 0.5rem; }

.info-box {
    background: rgba(99,179,237,0.07); border: 1px solid rgba(99,179,237,0.2);
    border-radius: 12px; padding: 1rem 1.2rem; color: #94a3b8; font-size: 0.85rem; line-height: 1.6;
}
.info-box strong { color: #63b3ed; }

.pipeline { display: flex; align-items: center; justify-content: center; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0; }
.pipe-node {
    background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3);
    border-radius: 8px; padding: 0.4rem 0.9rem; font-size: 0.78rem; font-weight: 600; color: #a5b4fc;
}
.pipe-arrow { color: #475569; font-size: 1rem; font-weight: 700; }

.empty-state { text-align: center; padding: 2rem 1rem; color: #475569; }
.empty-state p { font-size: 0.9rem; line-height: 1.5; }

@keyframes fadein { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
.fadein { animation: fadein 0.45s ease; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "translation_result" not in st.session_state:
    st.session_state.translation_result = None
if "last_lang" not in st.session_state:
    st.session_state.last_lang = None
if "elapsed" not in st.session_state:
    st.session_state.elapsed = None
# Separate variable to hold text area content (avoids WidgetAlreadyInstantiatedError)
if "text_input_val" not in st.session_state:
    st.session_state.text_input_val = ""

# ── Example button callback (runs BEFORE widgets render on next run) ──────────
EXAMPLES = [
    "Hello, how are you?",
    "The future belongs to those who believe in their dreams.",
    "Artificial intelligence is transforming the world.",
]

def use_example(text: str):
    """on_click callback — sets text BEFORE text_area is rendered."""
    st.session_state.text_input_val = text

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem;text-align:center;">
        <div style="font-size:2.2rem;">🌐</div>
        <div style="font-family:'Outfit',sans-serif;font-size:1.25rem;font-weight:700;
                    background:linear-gradient(135deg,#63b3ed,#9f7aea);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;margin:0.3rem 0;">LinguaLCEL</div>
        <div style="font-size:0.75rem;color:#475569;">Powered by LangChain LCEL</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='color:#63b3ed;font-size:0.75rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;'>⚙️ Model Settings</p>", unsafe_allow_html=True)

    selected_model_label = st.selectbox(
        "AI Model (Groq)", options=list(AVAILABLE_MODELS.keys()), index=0, key="model_select"
    )
    selected_model_id = AVAILABLE_MODELS[selected_model_label]

    st.markdown("---")
    st.markdown("<p style='color:#63b3ed;font-size:0.75rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;'>🔗 LCEL Pipeline</p>", unsafe_allow_html=True)
    st.markdown("""
    <div class="pipeline">
        <div class="pipe-node">Prompt</div>
        <div class="pipe-arrow">|</div>
        <div class="pipe-node">ChatGroq</div>
        <div class="pipe-arrow">|</div>
        <div class="pipe-node">StrParser</div>
    </div>
    <div style="font-size:0.75rem;color:#475569;text-align:center;margin-top:0.25rem;">
        chain = prompt | model | parser
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='color:#63b3ed;font-size:0.75rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;'>📖 About</p>", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        Built with <strong>LangChain Expression Language (LCEL)</strong>
        and <strong>Groq</strong> AI inference.<br><br>
        Demonstrates: PromptTemplates · ChatGroq · StrOutputParser · LCEL Chaining
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Clear History", key="clear_hist"):
        st.session_state.history = []
        st.session_state.translation_result = None
        st.session_state.last_lang = None
        st.session_state.elapsed = None
        st.session_state.text_input_val = ""
        st.rerun()

# ── Hero Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-badge">🔗 LangChain · LCEL · Groq AI</div>
    <h1 class="hero-title">AI Language Translator</h1>
    <p class="hero-subtitle">
        Translate text into <strong style="color:#63b3ed;">24+ languages</strong>
        using LangChain Expression Language chains powered by Groq ultra-fast inference.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Main Layout ───────────────────────────────────────────────────────────────
col_input, col_output = st.columns([1, 1], gap="large")

# ── LEFT: Input ───────────────────────────────────────────────────────────────
with col_input:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">✏️ Input Text</div>', unsafe_allow_html=True)

    # text_area bound to session_state key 'text_input_val'
    input_text = st.text_area(
        "Source Text",
        key="text_input_val",
        placeholder="Type or paste text to translate here...\n\nExample: Hello, how are you?",
        height=200,
        label_visibility="collapsed",
    )

    char_count = len(input_text) if input_text else 0

    col_lang, col_btn = st.columns([1.4, 1])
    with col_lang:
        # Default language = Hindi (index 5 in LANGUAGES list)
        hindi_index = LANGUAGES.index("Hindi")
        target_language = st.selectbox(
            "Target Language",
            options=LANGUAGES,
            index=hindi_index,
            key="lang_select",
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        translate_clicked = st.button("🌐 Translate", key="translate_btn")

    st.markdown(
        f'<div style="font-size:0.75rem;color:#475569;margin-top:0.25rem;">{char_count} characters</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Example phrases (using on_click to avoid WidgetAlreadyInstantiatedError) ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">💡 Try an example</div>', unsafe_allow_html=True)
    ex_cols = st.columns(3)
    for i, (ec, ex) in enumerate(zip(ex_cols, EXAMPLES)):
        with ec:
            st.button(
                f'"{ex[:18]}..."',
                key=f"ex_{i}",
                on_click=use_example,   # callback runs BEFORE render — no error!
                args=(ex,),
            )

# ── RIGHT: Output ─────────────────────────────────────────────────────────────
with col_output:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🌍 Translation Output</div>', unsafe_allow_html=True)

    if translate_clicked:
        if not input_text or not input_text.strip():
            st.warning("Please enter some text to translate.")
        else:
            with st.spinner("Translating with LCEL chain..."):
                try:
                    t_start = time.time()
                    result = translate(
                        text=input_text.strip(),
                        language=target_language,
                        model_name=selected_model_id,
                    )
                    elapsed = round(time.time() - t_start, 2)
                    st.session_state.translation_result = result
                    st.session_state.last_lang = target_language
                    st.session_state.elapsed = elapsed
                    st.session_state.history.insert(0, {
                        "original": input_text.strip(),
                        "translated": result,
                        "language": target_language,
                        "model": selected_model_label,
                        "elapsed": elapsed,
                    })
                    st.session_state.history = st.session_state.history[:10]
                except Exception as e:
                    st.error(f"Translation failed: {e}")

    if st.session_state.translation_result:
        lang = st.session_state.last_lang
        elapsed = st.session_state.elapsed
        result_text = st.session_state.translation_result

        st.markdown(
            f'''<div class="translation-output fadein">
            <div class="translation-lang-tag">→ {lang}</div>
            <div class="translation-text">{result_text}</div>
        </div>''',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'''<div class="stats-bar">
            <div class="stat-chip">⏱️ <span>{elapsed}s</span></div>
            <div class="stat-chip">📝 <span>{len(result_text)}</span> chars</div>
            <div class="stat-chip">🤖 <span>{selected_model_label.split("(")[0].strip()}</span></div>
        </div>''',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download Translation",
            data=result_text,
            file_name=f"translation_{lang.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            key="download_btn",
        )
    else:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:2.5rem;margin-bottom:0.75rem;">🌍</div>
            <p>Your translated text will appear here.<br>
            Select a language and click <strong style="color:#63b3ed;">Translate</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── History ───────────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label" style="margin-bottom:0.75rem;">📜 Translation History</div>', unsafe_allow_html=True)
    for item in st.session_state.history:
        orig = item["original"]
        trunc = orig[:120] + ("..." if len(orig) > 120 else "")
        st.markdown(
            f'''<div class="history-item">
            <div class="history-original">📝 {trunc}</div>
            <div class="history-translated">🌍 {item["translated"]}</div>
            <div class="history-meta">→ {item["language"]} &nbsp;·&nbsp; {item["model"].split("(")[0].strip()} &nbsp;·&nbsp; {item["elapsed"]}s</div>
        </div>''',
            unsafe_allow_html=True,
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:3rem;padding:1.5rem;border-top:1px solid rgba(255,255,255,0.06);">
    <div style="font-size:0.8rem;color:#334155;line-height:1.8;">
        Built with <span style="color:#63b3ed;">LangChain LCEL</span> ·
        <span style="color:#9f7aea;">Groq Inference</span> ·
        <span style="color:#f472b6;">Streamlit</span><br>
        <code style="color:#1e293b;background:transparent;">chain = prompt | model | parser</code>
    </div>
</div>
""", unsafe_allow_html=True)
