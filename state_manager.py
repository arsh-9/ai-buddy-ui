"""
state_manager.py
================
Conversation state management using Streamlit session state.

Responsibilities:
  - Initialise session state keys.
  - Append messages to chat history.
  - Track the current step, selected role, and user identity.
  - Provide helper accessors so the main app stays clean.

Design:
  - In future, this can be backed by a database for persistence.
"""

import streamlit as st

# Message roles
AI = "ai"
USER = "user"


def init_state() -> None:
    """Initialise all session-state keys (idempotent)."""
    defaults = {
        "user_email": None,
        "user_name": None,
        "chat_history": [],        # list[dict]  {"role": AI|USER, "content": str}
        "current_step": "step_1",
        "selected_role": None,
        "awaiting_selection": True,
        "flow_finished": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_user(email: str) -> None:
    """Store user email and derive display name."""
    st.session_state.user_email = email
    # Derive a friendly name from the email local part
    local = email.split("@")[0]
    # Capitalise parts separated by . or _
    parts = local.replace("_", ".").split(".")
    st.session_state.user_name = " ".join(p.capitalize() for p in parts)


def get_user_name() -> str:
    return st.session_state.get("user_name", "there")


def add_message(role: str, content: str) -> None:
    """Append a message to the chat history."""
    st.session_state.chat_history.append({"role": role, "content": content})


def get_history() -> list[dict]:
    return st.session_state.chat_history


def set_current_step(step_id: str) -> None:
    st.session_state.current_step = step_id


def get_current_step() -> str:
    return st.session_state.current_step


def set_selected_role(role: str) -> None:
    st.session_state.selected_role = role


def get_selected_role() -> str | None:
    return st.session_state.selected_role


def mark_flow_finished() -> None:
    st.session_state.flow_finished = True


def is_flow_finished() -> bool:
    return st.session_state.flow_finished
