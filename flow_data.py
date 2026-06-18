"""
flow_data.py
============
Hardcoded onboarding conversation flow definitions.

Design:
  - Each step is a dict with an "id", "message" (AI message text),
    and "options" (list of clickable choices).
  - Each option maps to a "next_step" id.
  - Special placeholders like {user_name} and {selected_role} are
    resolved at runtime by the flow engine.
  - In future, this entire structure can be fetched from a FastAPI backend.
"""

# ---------------------------------------------------------------------------
# Role-specific welcome messages (Step 3)
# ---------------------------------------------------------------------------
ROLE_DETAILS: dict[str, dict[str, str]] = {
    "BizOps – Front-End Developer": {
        "focus": "building intuitive UI and enhancing user experience across our platforms",
        "team_info": (
            "The BizOps team works on key areas like release & initiative management, "
            "branding, referral & programs management, user support, and minor enhancements, "
            "giving you strong exposure to both business and technology."
        ),
    },
    "Application Development – .NET / Full Stack Developer": {
        "focus": "designing and developing full-stack applications using .NET technologies",
        "team_info": (
            "The Application Development team builds and maintains enterprise-grade solutions, "
            "working across front-end and back-end layers to deliver robust, scalable software."
        ),
    },
    "Quality Assurance – QA Engineer / Senior QA": {
        "focus": "ensuring product quality through comprehensive testing strategies",
        "team_info": (
            "The QA team is responsible for test planning, automation, regression testing, "
            "and continuous quality improvement across all deliverables."
        ),
    },
    "L2 Support – Support Engineer": {
        "focus": "providing advanced technical support and troubleshooting for our platforms",
        "team_info": (
            "The L2 Support team handles escalated issues, root-cause analysis, and works "
            "closely with development teams to ensure rapid resolution."
        ),
    },
    "Reporting & Analytics – MSTR / Power BI Developer": {
        "focus": "creating data-driven reports and dashboards for business insights",
        "team_info": (
            "The Reporting & Analytics team leverages MicroStrategy, Power BI, and other tools "
            "to transform raw data into actionable intelligence for stakeholders."
        ),
    },
    "DataOps – Data Engineer / Analyst": {
        "focus": "building and optimizing data pipelines and analytical frameworks",
        "team_info": (
            "The DataOps team manages data infrastructure, ETL processes, and ensures data "
            "quality and availability for downstream consumers."
        ),
    },
    "Project Management – Scrum Master / Project Coordinator": {
        "focus": "facilitating agile ceremonies and coordinating cross-functional project delivery",
        "team_info": (
            "The Project Management team drives delivery excellence through agile methodologies, "
            "stakeholder management, and continuous process improvement."
        ),
    },
}


# ---------------------------------------------------------------------------
# Conversation steps
# ---------------------------------------------------------------------------
FLOW_STEPS: dict[str, dict] = {
    "step_1": {
        "id": "step_1",
        "message": "Hi {user_name}! 👋 Welcome to **AI Buddy**",
        "options": [
            {"label": "Are you a new member of the team?", "next_step": "step_2"},
            {"label": "No, looking for something else.", "next_step": "step_other"},
        ],
    },
    "step_2": {
        "id": "step_2",
        "message": (
            "I'm **AI Buddy**, and I'm here to help you get started on your onboarding journey.\n\n"
            "A very warm welcome to the team — we're excited to have you with us! 🎉\n\n"
            "To create your personalized onboarding roadmap, I just need to know where you're joining.\n\n"
            "Please select your **Team & Role** from the options below."
        ),
        "options": [
            {"label": "BizOps – Front-End Developer", "next_step": "step_3"},
            {"label": "Application Development – .NET / Full Stack Developer", "next_step": "step_3"},
            {"label": "Quality Assurance – QA Engineer / Senior QA", "next_step": "step_3"},
            {"label": "L2 Support – Support Engineer", "next_step": "step_3"},
            {"label": "Reporting & Analytics – MSTR / Power BI Developer", "next_step": "step_3"},
            {"label": "DataOps – Data Engineer / Analyst", "next_step": "step_3"},
            {"label": "Project Management – Scrum Master / Project Coordinator", "next_step": "step_3"},
        ],
    },
    "step_3": {
        "id": "step_3",
        # Message is dynamically generated – see build_step3_message() below
        "message": None,
        "options": [
            {"label": "Let's get started!", "next_step": "step_4"},
        ],
    },
    "step_4": {
        "id": "step_4",
        "message": (
            "Before we move on to the **Client & Business Overview**, **Business Process Understanding**, "
            "and **Team Introduction**, let's first initiate your LHH ID request and software setup.\n\n"
            "This will enable you to get your **LHH email ID** for client communications and ensure all "
            "required tools and software are installed so you're fully ready to begin your development "
            "journey without blockers.\n\n"
            "Let's start with:"
        ),
        "options": [
            {"label": "LHH ID Request and NDA Signature", "next_step": "step_end"},
        ],
    },
    "step_end": {
        "id": "step_end",
        "message": (
            "Great! 🚀 I've initiated the **LHH ID Request and NDA Signature** process for you.\n\n"
            "You'll receive further instructions via email shortly. In the meantime, feel free to "
            "explore and reach out if you need any help!\n\n"
            "Welcome aboard! 🎊"
        ),
        "options": [],
    },
    "step_other": {
        "id": "step_other",
        "message": (
            "No worries! I'm here whenever you need help. 😊\n\n"
            "If you change your mind or need onboarding assistance later, just come back and say hi!"
        ),
        "options": [],
    },
}


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
