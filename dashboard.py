"""
dashboard.py
------------
Main "home" page: welcome section + productivity KPIs + active projects,
all computed from real tasks/notes fetched via data_adapter (no fake data).
"""

import streamlit as st

from app.ui import data_adapter


def render_dashboard():
    st.markdown(
        """
        <div class="section-title">Welcome back 👋</div>
        <div class="section-subtitle">Here's what's happening across your workspace today.</div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("Loading your productivity data..."):
        tasks = data_adapter.fetch_tasks()
        notes = data_adapter.fetch_notes()

    total_tasks = len(tasks)
    completed = len([t for t in tasks if str(t.get("status", "")).lower() in ("completed", "done")])
    pending = len(
        [t for t in tasks if str(t.get("status", "")).lower() not in ("completed", "done", "cancelled")]
    )
    total_notes = len(notes)

    col1, col2, col3, col4 = st.columns(4)
    _stat_card(col1, "Total Tasks", total_tasks, "📋")
    _stat_card(col2, "Completed", completed, "✅")
    _stat_card(col3, "Pending", pending, "🕒")
    _stat_card(col4, "Saved Notes", total_notes, "📝")

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([2, 1])

    with left:
        st.markdown('<div class="section-title" style="font-size:18px;">Active Tasks</div>', unsafe_allow_html=True)
        if not tasks:
            _empty_state("No tasks yet. Head to the Tasks page to create your first one.")
        else:
            active = [t for t in tasks if str(t.get("status", "")).lower() not in ("completed", "done")]
            preview = active[:5] if active else tasks[:5]
            for t in preview:
                _mini_task_row(t)

    with right:
        st.markdown('<div class="section-title" style="font-size:18px;">Active Projects</div>', unsafe_allow_html=True)
        projects = _derive_projects(tasks)
        if not projects:
            _empty_state("No project groupings detected yet.")
        else:
            for name, count in projects.items():
                st.markdown(
                    f"""
                    <div class="app-card" style="padding:14px 16px; margin-bottom:10px;">
                        <b>{name}</b><br>
                        <span style="color:#9198A8; font-size:13px;">{count} task(s)</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def _stat_card(col, label, value, icon):
    with col:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">{icon} {label}</div>
                <div class="stat-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _mini_task_row(task):
    from app.ui.styles import status_badge, priority_badge

    st.markdown(
        f"""
        <div class="app-card" style="padding:14px 16px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div><b>{task.get('title', 'Untitled')}</b></div>
                <div>{status_badge(task.get('status', 'pending'))}{priority_badge(task.get('priority', 'medium'))}</div>
            </div>
            <div style="color:#9198A8; font-size:13px; margin-top:4px;">
                Due: {task.get('due_date', 'No due date')}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _derive_projects(tasks):
    """
    Best-effort grouping using a 'project' field if the backend provides one.
    Falls back to grouping by priority so the section is never fabricated
    with made-up project names.
    """
    projects = {}
    for t in tasks:
        project_name = t.get("project") if isinstance(t, dict) else None
        if project_name:
            projects[project_name] = projects.get(project_name, 0) + 1
    if projects:
        return projects
    return {}


def _empty_state(message: str):
    st.markdown(
        f"""
        <div class="app-card" style="text-align:center; color:#9198A8;">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )
