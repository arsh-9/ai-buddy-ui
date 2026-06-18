"""
AI Buddy – Employee Onboarding Assistant
=========================================
Main Streamlit application entry point.

Architecture:
  ├── app.py            ← this file (entry point & page orchestration)
  ├── chat_ui.py        ← UI rendering functions
  ├── state_manager.py  ← session state management
  └── flow_data.py      ← conversation flow definitions

Run:
  streamlit run app.py
"""

import streamlit as st

# ── Page Configuration (must be FIRST Streamlit call) ────────────────────────
st.set_page_config(
    page_title="AI Buddy – Onboarding Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from state_manager import init_state, set_user, get_history, add_message, AI, get_user_name
from chat_ui import inject_custom_css, render_brand_header, render_message, render_options, get_next_step, auto_scroll
from flow_data import get_step


# ── Initialise ───────────────────────────────────────────────────────────────
init_state()
inject_custom_css()


# ── Email Gate ───────────────────────────────────────────────────────────────

def show_email_screen() -> bool:
    """
    Display the email entry card.
    Returns True if user has submitted an email.
    """
    render_brand_header()

    st.markdown("""
    <div class="email-card">
        <div class="icon">✉️</div>
        <h2>Welcome to AI Buddy</h2>
        <p>Enter your work email to get started with your personalized onboarding journey.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

    # Centre the form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("email_form", clear_on_submit=False):
            email = st.text_input(
                "Email Address",
                placeholder="yourname@company.com",
                key="email_input",
            )
            submitted = st.form_submit_button("🚀  Start Onboarding", type="primary")

        if submitted and email and "@" in email:
            set_user(email)
            # Kick off the conversation with Step 1
            step1 = get_step("step_1")
            if step1:
                msg = step1["message"].replace("{user_name}", get_user_name())
                add_message(AI, msg)
            return True
        elif submitted:
            st.markdown(
                "<p style='text-align:center; color:#f87171; font-size:.85rem; margin-top:.5rem;'>"
                "Please enter a valid email address.</p>",
                unsafe_allow_html=True,
            )

    return False


# ── Chat Screen ──────────────────────────────────────────────────────────────

def show_chat_screen() -> None:
    """Render the full chat interface."""
    render_brand_header()

    st.markdown(
        "<div class='chat-divider'>── Onboarding Conversation ──</div>",
        unsafe_allow_html=True,
    )

    # Render chat history
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in get_history():
        render_message(msg["role"], msg["content"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Render options for the current step (if any remain)
    if not st.session_state.flow_finished:
        current_step_data = get_step(st.session_state.current_step)
        if current_step_data and current_step_data.get("options"):
            render_options(current_step_data["options"], current_step_data["id"])

    # Auto-scroll to latest
    auto_scroll()


# ── Main Router ──────────────────────────────────────────────────────────────

def main() -> None:
    if st.session_state.user_email is None:
        already_submitted = show_email_screen()
        if already_submitted:
            st.rerun()
    else:
        show_chat_screen()


if __name__ == "__main__":
    main()
