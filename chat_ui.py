"""
chat_ui.py
==========
UI rendering functions for the AI Buddy chatbot.

Responsibilities:
  - render_message()   – display a single chat bubble (AI or User)
  - render_options()   – display clickable option buttons
  - handle_selection() – process a user's button click
  - get_next_step()    – resolve the next conversation step
  - inject_custom_css()– inject the modern chat styling

All heavy styling is done via injected CSS; the Python code
focuses on structure and semantics.
"""

import streamlit as st

from state_manager import AI, USER, add_message, get_user_name, set_current_step, set_selected_role, get_selected_role, mark_flow_finished
from flow_data import get_step, build_step3_message, FLOW_STEPS


# ── CSS Injection ────────────────────────────────────────────────────────────

def inject_custom_css() -> None:
    """Inject the complete custom CSS for the chatbot UI."""
    st.markdown("""
    <style>
    /* ── Import Google Fonts ─────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global Resets ───────────────────────────────────────── */
    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(160deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
    }

    /* Hide default Streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        max-width: 820px !important;
        padding-top: 1rem !important;
        padding-bottom: 6rem !important;
    }

    /* ── Brand Header ────────────────────────────────────────── */
    .brand-header {
        text-align: center;
        padding: 1.5rem 0 1rem;
    }
    .brand-header .logo {
        width: 56px; height: 56px;
        background: linear-gradient(135deg, #6C63FF 0%, #48c6ef 100%);
        border-radius: 16px;
        display: inline-flex; align-items: center; justify-content: center;
        font-size: 28px;
        box-shadow: 0 8px 32px rgba(108, 99, 255, .35);
        margin-bottom: .6rem;
    }
    .brand-header h1 {
        font-size: 1.55rem; font-weight: 700;
        background: linear-gradient(90deg, #6C63FF, #48c6ef);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .brand-header p {
        color: rgba(255,255,255,.5); font-size: .82rem; margin: .25rem 0 0;
    }

    /* ── Chat Container ──────────────────────────────────────── */
    .chat-container {
        display: flex; flex-direction: column; gap: 0;
        padding: .5rem 0;
    }

    /* ── Message Rows ────────────────────────────────────────── */
    .msg-row {
        display: flex; gap: .65rem; animation: fadeSlide .4s ease;
        margin-bottom: 1.2rem;
    }
    .msg-row.ai  { justify-content: flex-start; }
    .msg-row.user { justify-content: flex-end; }

    @keyframes fadeSlide {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Avatars ──────────────────────────────────────────────── */
    .avatar {
        width: 36px; height: 36px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px; flex-shrink: 0; margin-top: 2px;
    }
    .avatar.ai {
        background: linear-gradient(135deg, #6C63FF, #48c6ef);
        box-shadow: 0 4px 14px rgba(108,99,255,.3);
    }
    .avatar.user {
        background: linear-gradient(135deg, #f857a6, #ff5858);
        box-shadow: 0 4px 14px rgba(248,87,166,.3);
    }

    /* ── Bubbles ──────────────────────────────────────────────── */
    .bubble {
        padding: .85rem 1.15rem;
        border-radius: 18px;
        font-size: .92rem;
        line-height: 1.55;
        max-width: 78%;
        word-wrap: break-word;
    }
    .bubble.ai {
        background: rgba(255,255,255,.07);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,.10);
        color: rgba(255,255,255,.92);
        border-top-left-radius: 4px;
    }
    .bubble.user {
        background: linear-gradient(135deg, #6C63FF 0%, #8B5CF6 100%);
        color: #fff;
        border-top-right-radius: 4px;
        box-shadow: 0 4px 20px rgba(108,99,255,.30);
    }
    .bubble p { margin: 0 0 .45rem; }
    .bubble p:last-child { margin-bottom: 0; }
    .bubble strong { color: #a78bfa; }
    .bubble.user strong { color: #e0d4ff; }

    /* ── Option Buttons ──────────────────────────────────────── */
    .options-wrapper {
        display: flex; flex-wrap: wrap; gap: .5rem;
        padding: .5rem 0 .25rem 2.8rem;
        margin-top: .5rem;
        animation: fadeSlide .45s ease;
    }

    /* Add spacing above Streamlit button containers */
    .stButton {
        margin-top: .35rem !important;
        margin-bottom: .35rem !important;
    }

    /* Style Streamlit buttons inside option containers */
    div[data-testid="stHorizontalBlock"] .stButton > button,
    .stButton > button {
        background: rgba(108, 99, 255, .12) !important;
        border: 1px solid rgba(108, 99, 255, .35) !important;
        color: #c4b5fd !important;
        border-radius: 24px !important;
        padding: .55rem 1.3rem !important;
        font-size: .85rem !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        transition: all .25s ease !important;
        white-space: normal !important;
        text-align: left !important;
        line-height: 1.4 !important;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button:hover,
    .stButton > button:hover {
        background: rgba(108, 99, 255, .28) !important;
        border-color: #6C63FF !important;
        color: #fff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 18px rgba(108, 99, 255, .25) !important;
    }

    /* ── Email Input Styling ─────────────────────────────────── */
    .email-card {
        background: rgba(255,255,255,.05);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        text-align: center;
        max-width: 480px;
        margin: 4rem auto 0;
        box-shadow: 0 20px 60px rgba(0,0,0,.3);
    }
    .email-card .icon {
        font-size: 3rem; margin-bottom: 1rem;
    }
    .email-card h2 {
        color: #fff; font-weight: 700; font-size: 1.4rem; margin: 0 0 .3rem;
    }
    .email-card p {
        color: rgba(255,255,255,.55); font-size: .88rem; margin: 0 0 1.5rem;
    }

    /* Text input styling */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,.06) !important;
        border: 1px solid rgba(108,99,255,.35) !important;
        border-radius: 14px !important;

        padding: .75rem 1rem !important;
        font-size: .95rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6C63FF !important;
        box-shadow: 0 0 0 2px rgba(108,99,255,.25) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,.35) !important;
    }
    /* Hide text input label */
    .stTextInput > label { display: none !important; }

    /* Primary submit button */
    button[kind="primary"], .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6C63FF 0%, #48c6ef 100%) !important;
        border: none !important;
        color: #fff !important;
        border-radius: 14px !important;
        padding: .7rem 2rem !important;
        font-weight: 600 !important;
        font-size: .95rem !important;
        width: 100% !important;
        transition: all .25s ease !important;
        box-shadow: 0 6px 24px rgba(108,99,255,.3) !important;
    }
    button[kind="primary"]:hover, .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(108,99,255,.45) !important;
    }

    /* ── Typing Indicator ────────────────────────────────────── */
    .typing-indicator {
        display: flex; gap: 5px; padding: .5rem 0 .5rem 3rem;
        animation: fadeSlide .3s ease;
    }
    .typing-indicator .dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: rgba(108,99,255,.5);
        animation: typingBounce 1.4s infinite ease-in-out;
    }
    .typing-indicator .dot:nth-child(2) { animation-delay: .2s; }
    .typing-indicator .dot:nth-child(3) { animation-delay: .4s; }

    @keyframes typingBounce {
        0%, 80%, 100% { transform: scale(0.7); opacity: .4; }
        40% { transform: scale(1); opacity: 1; }
    }

    /* ── Scrollbar ───────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(108,99,255,.3); border-radius: 3px;
    }

    /* ── Divider ─────────────────────────────────────────────── */
    .chat-divider {
        text-align: center; color: rgba(255,255,255,.25);
        font-size: .75rem; padding: .5rem 0 1rem;
    }

    /* ── Reduce Streamlit default element gaps ────────────────── */
    .stMarkdown {
        margin-bottom: 0 !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0 !important;
    }

    /* ── Responsive ──────────────────────────────────────────── */
    @media (max-width: 640px) {
        .bubble { max-width: 90%; font-size: .87rem; }
        .email-card { margin: 2rem 1rem 0; padding: 2rem 1.5rem; }
    }
    </style>
    """, unsafe_allow_html=True)


# ── Rendering Helpers ────────────────────────────────────────────────────────

def render_brand_header() -> None:
    """Render the AI Buddy brand header."""
    st.markdown("""
    <div class="brand-header">
        <div class="logo">🤖</div>
        <h1>AI Buddy</h1>
        <p>Your Employee Onboarding Assistant</p>
    </div>
    """, unsafe_allow_html=True)


def render_message(role: str, content: str) -> None:
    """
    Render a single chat message bubble.
    role: 'ai' or 'user'
    """
    if role == AI:
        # Convert markdown bold **text** → <strong>text</strong>
        import re
        html_content = content.replace("\n", "<br>")
        html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)

        st.markdown(f"""
        <div class="msg-row ai">
            <div class="avatar ai">🤖</div>
            <div class="bubble ai">{html_content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-row user">
            <div class="bubble user">{content}</div>
            <div class="avatar user">👤</div>
        </div>
        """, unsafe_allow_html=True)


def render_options(options: list[dict], step_id: str) -> None:
    """
    Render clickable option buttons for the current step.
    Each option is a dict with 'label' and 'next_step'.
    """
    if not options:
        return

    # Determine layout: use columns for ≤3 options, stacked for more
    if len(options) <= 3:
        cols = st.columns(len(options))
        for i, opt in enumerate(options):
            with cols[i]:
                if st.button(
                    f"• {opt['label']}",
                    key=f"opt_{step_id}_{i}",
                    use_container_width=True,
                ):
                    handle_selection(opt["label"], opt["next_step"])
                    st.rerun()
    else:
        for i, opt in enumerate(options):
            if st.button(
                f"• {opt['label']}",
                key=f"opt_{step_id}_{i}",
                use_container_width=True,
            ):
                handle_selection(opt["label"], opt["next_step"])
                st.rerun()


def handle_selection(label: str, next_step: str) -> None:
    """
    Process a user's option selection:
      1. Add the selected label as a user message.
      2. If this is a role selection (step_2), store it.
      3. Resolve and add the next AI message.
      4. Advance the current step.
    """
    # Record user selection
    add_message(USER, label)

    # Track selected role if coming from step 2
    current = st.session_state.current_step
    if current == "step_2":
        set_selected_role(label)

    # Advance step
    set_current_step(next_step)

    # Get the next step data and add its AI message
    next_data = get_step(next_step)
    if next_data:
        ai_msg = get_next_step(next_data)
        if ai_msg:
            add_message(AI, ai_msg)
        if not next_data.get("options"):
            mark_flow_finished()


def get_next_step(step_data: dict) -> str | None:
    """
    Resolve the AI message for a given step.
    Handles dynamic message generation (e.g. step_3).

    In future, this will call the FastAPI backend.
    """
    step_id = step_data["id"]

    if step_id == "step_3":
        role = get_selected_role()
        if role:
            return build_step3_message(role)
        return step_data.get("message")

    msg = step_data.get("message")
    if msg:
        # Resolve placeholders
        msg = msg.replace("{user_name}", get_user_name())
    return msg


# ── Auto-Scroll Helper ──────────────────────────────────────────────────────

def auto_scroll() -> None:
    """Inject JS to scroll to the bottom of the chat."""
    st.markdown("""
    <script>
        const mainContent = window.parent.document.querySelector('section.main');
        if (mainContent) {
            mainContent.scrollTop = mainContent.scrollHeight;
        }
    </script>
    """, unsafe_allow_html=True)
