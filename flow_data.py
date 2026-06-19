"""
flow_data.py
============
Onboarding conversation flow definitions loaded from flow_steps.json.

Design:
  - All flow content (steps, options, role details) lives in flow_steps.json.
  - This module loads that JSON at startup and exposes the same API
    (get_step, build_step3_message) to the rest of the app.
  - Special placeholders like {user_name} are resolved at runtime
    by the flow engine in chat_ui.py.
  - In future, the JSON load can be swapped for a FastAPI call.
"""

import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Load flow data from JSON
# ---------------------------------------------------------------------------
_FLOW_FILE = Path(__file__).parent / "flow_steps.json"

with open(_FLOW_FILE, encoding="utf-8") as f:
    _DATA = json.load(f)

ROLE_DETAILS: dict[str, dict[str, str]] = _DATA["role_details"]
FLOW_STEPS: dict[str, dict] = _DATA["flow_steps"]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_step3_message(role: str) -> str:
    """Build the personalised welcome message for step 3."""
    details = ROLE_DETAILS.get(role, {})
    team_name = role.split("–")[0].strip() if "–" in role else role.split("-")[0].strip()
    role_title = role.split("–")[1].strip() if "–" in role else role

    focus = details.get("focus", "contributing to the team's goals")
    team_info = details.get("team_info", "The team works on exciting projects across the organisation.")

    return (
        f"Welcome once again — great to have you onboard! 🙌\n\n"
        f"I see that you've joined the **{team_name}** team as a **{role_title}** — that's fantastic!\n\n"
        f"You'll be focused on {focus}.\n\n"
        f"{team_info}\n\n"
        f"I'll now guide you through your onboarding steps."
    )


def get_step(step_id: str) -> dict | None:
    """
    Retrieve a flow step by its ID.
    In future, this will call the FastAPI backend instead.
    """
    return FLOW_STEPS.get(step_id)
