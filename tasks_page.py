"""
tasks_page.py
-------------
Full Task Management page: create-task form + filterable list of
professional task cards. All data comes from data_adapter (real backend).
"""

import streamlit as st

from app.ui import data_adapter
from app.ui.components.task_card import render_task_card


def render_tasks_page():
    st.markdown(
        """
        <div class="section-title">✅ Task Management</div>
        <div class="section-subtitle">Create, track, and manage tasks through your AI agent.</div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("➕ Create a new task", expanded=False):
        with st.form("create_task_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Task title")
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            with col2:
                due_date = st.date_input("Due date")
                status = st.selectbox("Initial status", ["Pending", "In Progress"])
            description = st.text_area("Description", height=100)

            submitted = st.form_submit_button("Create Task", use_container_width=True)
            if submitted:
                if not title.strip():
                    st.warning("Please provide a task title.")
                else:
                    with st.spinner("Creating task via agent..."):
                        result = data_adapter.create_task(
                            title.strip(), description.strip(), priority.lower(), str(due_date)
                        )
                    st.success(result)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    with st.spinner("Loading tasks..."):
        tasks = data_adapter.fetch_tasks()

    filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 2])
    with filter_col1:
        status_filter = st.selectbox(
            "Filter by status", ["All", "Pending", "In Progress", "Completed"], key="status_filter"
        )
    with filter_col2:
        priority_filter = st.selectbox(
            "Filter by priority", ["All", "High", "Medium", "Low"], key="priority_filter"
        )
    with filter_col3:
        search_text = st.text_input("Search tasks", placeholder="Search by title...", key="task_search")

    filtered = _apply_filters(tasks, status_filter, priority_filter, search_text)

    st.markdown(
        f'<div class="section-subtitle">Showing {len(filtered)} of {len(tasks)} task(s)</div>',
        unsafe_allow_html=True,
    )

    if not filtered:
        st.markdown(
            '<div class="app-card" style="text-align:center; color:#9198A8;">'
            "No tasks match your filters yet."
            "</div>",
            unsafe_allow_html=True,
        )
        return

    cols = st.columns(2)
    for i, task in enumerate(filtered):
        with cols[i % 2]:
            render_task_card(task)


def _apply_filters(tasks, status_filter, priority_filter, search_text):
    result = tasks
    if status_filter != "All":
        target = status_filter.lower().replace(" ", "_")
        result = [t for t in result if str(t.get("status", "")).lower().replace(" ", "_") == target]
    if priority_filter != "All":
        result = [t for t in result if str(t.get("priority", "")).lower() == priority_filter.lower()]
    if search_text.strip():
        q = search_text.lower().strip()
        result = [t for t in result if q in str(t.get("title", "")).lower()]
    return result
