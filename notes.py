"""
notes.py
--------
Notes page (create + browse) and the dedicated Semantic Search page.
Both talk to the backend exclusively through data_adapter, which in
turn only uses AgentController.
"""

import streamlit as st

from app.ui import data_adapter


def render_notes_page():
    st.markdown(
        """
        <div class="section-title">📝 Notes</div>
        <div class="section-subtitle">Capture ideas, meeting notes, and knowledge for your agent to recall later.</div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("➕ Create a new note", expanded=False):
        with st.form("create_note_form", clear_on_submit=True):
            title = st.text_input("Note title")
            content = st.text_area("Note content", height=140)
            submitted = st.form_submit_button("Save Note", use_container_width=True)
            if submitted:
                if not title.strip() or not content.strip():
                    st.warning("Please provide both a title and content.")
                else:
                    with st.spinner("Saving note via agent..."):
                        result = data_adapter.create_note(title.strip(), content.strip())
                    st.success(result)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="font-size:18px;">Your Notes</div>', unsafe_allow_html=True)

    with st.spinner("Loading notes..."):
        notes = data_adapter.fetch_notes()

    if not notes:
        st.markdown(
            '<div class="app-card" style="text-align:center; color:#9198A8;">'
            "No notes yet. Create one above to get started."
            "</div>",
            unsafe_allow_html=True,
        )
        return

    cols = st.columns(2)
    for i, note in enumerate(notes):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="app-card">
                    <div class="task-title">{note.get('title', 'Untitled Note')}</div>
                    <div class="task-desc">{note.get('content', '')}</div>
                    <div class="task-meta">🕒 {note.get('created_at', '')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_semantic_search_page():
    st.markdown(
        """
        <div class="section-title">🔎 Semantic Search</div>
        <div class="section-subtitle">Search your notes by meaning, powered by ChromaDB embeddings.</div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("semantic_search_form"):
        query = st.text_input("Search your notes...", placeholder="e.g. 'ideas about client onboarding'")
        submitted = st.form_submit_button("Search", use_container_width=True)

    if submitted and query.strip():
        with st.spinner("Running semantic search via ChromaDB..."):
            result = data_adapter.semantic_search_notes(query.strip())

        st.markdown('<div class="section-title" style="font-size:16px;">Results</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="app-card">
                <div class="task-desc" style="white-space: pre-wrap;">{result}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif submitted:
        st.warning("Please enter a search query.")
