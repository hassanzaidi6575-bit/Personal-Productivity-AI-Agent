"""
main.py
-------
Main entry point for Personal Productivity AI Agent Streamlit application.
"""

import streamlit as st


from app.ui.styles import inject_global_styles


from app.ui.components.sidebar import render_sidebar


from app.ui.components.dashboard import render_dashboard


from app.ui.components.tasks_page import render_tasks_page


from app.ui.components.notes import (
    render_notes_page,
    render_semantic_search_page
)


from app.ui.components.planner import render_planner_page


from app.ui.components.chat import render_chat_page


from app.ui.components.settings import render_settings_page





def main():

    st.set_page_config(
        page_title="Personal Productivity AI Agent",
        page_icon="🤖",
        layout="wide"
    )


    # Load CSS

    inject_global_styles()



    # Sidebar

    page = render_sidebar()



    # Page Routing


    if page == "Dashboard":

        render_dashboard()



    elif page == "Tasks":

        render_tasks_page()



    elif page == "Notes":

        render_notes_page()



    elif page == "Semantic Search":

        render_semantic_search_page()



    elif page == "Work Planner":

        render_planner_page()



    elif page == "AI Assistant":

        render_chat_page()



    elif page == "Settings":

        render_settings_page()



    else:

        st.info("Select a page from sidebar.")







if __name__ == "__main__":

    main()