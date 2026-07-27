"""
settings.py
-----------
Lightweight settings/about page. No backend-mutating settings are
fabricated here since the backend contract only exposes `controller.run()`;
this page mostly surfaces environment/connection info and lets the user
reset local UI state (chat history, cached controller instance).
"""

import streamlit as st


def render_settings_page():
    st.markdown(
        """
        <div class="section-title">⚙ Settings</div>
        <div class="section-subtitle">Workspace preferences and connection info.</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown("**Backend Connection**")
    st.markdown(
        """
        <div style="color:#9198A8; font-size:14px;">
        Interface: <code>app.agent.controller.AgentController</code><br>
        Entry point: <code>controller.run(user_message)</code><br>
        Vector store: ChromaDB (semantic search)<br>
        Orchestration: LangGraph
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown("**Session Controls**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧹 Clear chat history", use_container_width=True):
            st.session_state.chat_history = []
            st.success("Chat history cleared.")
    with col2:
        if st.button("🔄 Reset agent controller", use_container_width=True):
            st.session_state.pop("agent_controller", None)
            st.success("Controller will be re-initialized on next action.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown("**About**")
    st.markdown(
        """
        <div style="color:#9198A8; font-size:14px;">
        Personal Productivity AI Agent — a LangGraph-based assistant for tasks,
        notes, semantic search, and daily planning. This dashboard is a pure
        frontend layer; all logic and data live in your existing backend.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
