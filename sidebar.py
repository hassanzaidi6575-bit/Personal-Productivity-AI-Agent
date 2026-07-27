"""
sidebar.py
----------
Left navigation for the dashboard. Purely presentational + routing;
no backend calls happen here.
"""

import streamlit as st

NAV_ITEMS = [
    ("Dashboard", "🏠"),
    ("Tasks", "✅"),
    ("Notes", "📝"),
    ("Semantic Search", "🔎"),
    ("Work Planner", "📅"),
    ("AI Assistant", "🤖"),
    ("Settings", "⚙"),
]


def render_sidebar() -> str:
    """Renders the sidebar and returns the currently selected page name."""
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Dashboard"

    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 6px 4px 18px 4px;">
                <div style="font-size:20px; font-weight:700;">🧠 Productivity Agent</div>
                <div style="font-size:12.5px; color:#9198A8;">AI-powered workspace</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for label, icon in NAV_ITEMS:
            is_active = st.session_state.active_page == label
            button_label = f"{icon}  {label}"
            if st.button(
                button_label,
                key=f"nav_{label}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.active_page = label
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size:12px; color:#9198A8; padding: 0 4px;">
                Connected backend<br>
                <span style="color:#2ECC71;">● </span> AgentController (LangGraph)
            </div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state.active_page
