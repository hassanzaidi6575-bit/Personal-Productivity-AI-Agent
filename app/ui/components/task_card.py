"""
task_card.py
------------
Renders a single professional task card, plus action buttons that route
back through the AgentController (complete / delete) via data_adapter.
"""

import streamlit as st

from app.ui.styles import status_badge, priority_badge
from app.ui import data_adapter


def render_task_card(task: dict):
    task_id = task.get("id", "")
    title = task.get("title", "Untitled Task")
    description = task.get("description", "")
    status = task.get("status", "pending")
    priority = task.get("priority", "medium")
    due_date = task.get("due_date", "No due date")

    with st.container():
        st.markdown('<div class="app-card">', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="task-title">{title}</div>
            <div>{status_badge(status)}{priority_badge(priority)}</div>
            <div class="task-desc">{description or "No description provided."}</div>
            <div class="task-meta">📅 Due: {due_date} &nbsp;&nbsp;|&nbsp;&nbsp; 🆔 {task_id}</div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Mark Complete", key=f"complete_{task_id}", use_container_width=True):
                with st.spinner("Updating task via agent..."):
                    result = data_adapter.update_task_status(task_id, "completed")
                st.success(result)
                st.rerun()
        with col2:
            if st.button("🔄 In Progress", key=f"progress_{task_id}", use_container_width=True):
                with st.spinner("Updating task via agent..."):
                    result = data_adapter.update_task_status(task_id, "in_progress")
                st.success(result)
                st.rerun()
        with col3:
            if st.button("🗑 Delete", key=f"delete_{task_id}", use_container_width=True):
                with st.spinner("Deleting task via agent..."):
                    result = data_adapter.delete_task(task_id)
                st.warning(result)
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
