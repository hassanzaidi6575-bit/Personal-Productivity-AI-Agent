"""
main.py
-------
Entry point for the Personal Productivity AI Agent dashboard.

Run with:
    python -m streamlit run app/ui/main.py

This file only handles page routing + global setup. It does not contain
any business logic — every action is delegated to `app.ui.data_adapter`,
which calls your real `app.agent.controller.AgentController`.
"""

import sys
from pathlib import Path

import streamlit as st

# Ensure the project root (containing the `app` package) is on sys.path
# so `from app.agent.controller import AgentController` resolves correctly
# regardless of the working directory Streamlit is launched from.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ui.styles import inject_global_styles
from app.ui.components.sidebar import render_sidebar
from app.ui.components.dashboard import render_dashboard
from app.ui.components.tasks_page import render_tasks_page
from app.ui.components.notes import render_notes_page, render_semantic_search_page
from app.ui.components.planner import render_planner_page
from app.ui.components.chat import render_chat_page
from app.ui.components.settings import render_settings_page


st.set_page_config(
    page_title="Personal Productivity AI Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()

active_page = render_sidebar()

PAGE_RENDERERS = {
    "Dashboard": render_dashboard,
    "Tasks": render_tasks_page,
    "Notes": render_notes_page,
    "Semantic Search": render_semantic_search_page,
    "Work Planner": render_planner_page,
    "AI Assistant": render_chat_page,
    "Settings": render_settings_page,
}

renderer = PAGE_RENDERERS.get(active_page, render_dashboard)
renderer()
