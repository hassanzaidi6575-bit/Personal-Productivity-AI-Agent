"""
planner.py
----------
Work Planner page: daily plan generation + meeting note analysis.
Both routed through the LangGraph agent via data_adapter.
"""

import streamlit as st

from app.ui import data_adapter



def clean_output(text):
    """
    Clean AI response formatting.
    Removes excessive empty lines.
    """

    if not text:
        return ""

    lines = text.splitlines()

    cleaned = []

    empty_found = False

    for line in lines:

        line = line.rstrip()

        if line.strip() == "":

            if not empty_found:
                cleaned.append("")

            empty_found = True

        else:

            cleaned.append(line)

            empty_found = False


    return "\n".join(cleaned).strip()





def render_planner_page():

    st.markdown(
        """
        <div class="section-title">📅 Work Planner</div>

        <div class="section-subtitle">
        Let your agent plan your day or analyze meeting notes for action items.
        </div>
        """,
        unsafe_allow_html=True,
    )



    tab1, tab2 = st.tabs(
        [
            "🗓 Daily Plan",
            "📋 Meeting Note Analysis"
        ]
    )



    # -----------------------------
    # Daily Planner
    # -----------------------------

    with tab1:


        st.markdown(
            '<div class="section-title" style="font-size:18px;">Generate today\'s plan</div>',
            unsafe_allow_html=True,
        )


        context = st.text_area(
            "Anything specific to factor in? (optional)",
            placeholder="Prepare AI evaluation demo, revise LangGraph, complete documentation...",
            height=90,
        )



        if st.button(
            "✨ Generate Daily Plan",
            use_container_width=True
        ):


            with st.spinner(
                "Agent is analyzing your tasks and priorities..."
            ):

                plan = data_adapter.generate_daily_plan(
                    context.strip()
                )



            plan = clean_output(plan)



            st.markdown(
                """
                <div class="app-card">

                <div class="task-title">
                📅 Today's Plan
                </div>

                </div>
                """,
                unsafe_allow_html=True,
            )



            # Display markdown normally
            st.markdown(plan)





    # -----------------------------
    # Meeting Analysis
    # -----------------------------

    with tab2:


        st.markdown(
            '<div class="section-title" style="font-size:18px;">Analyze meeting notes</div>',
            unsafe_allow_html=True,
        )



        meeting_text = st.text_area(
            "Paste your raw meeting notes",
            height=200,
            placeholder="Paste meeting transcript or notes here...",
        )



        if st.button(
            "🔍 Analyze & Extract Action Items",
            use_container_width=True
        ):


            if not meeting_text.strip():

                st.warning(
                    "Please paste some meeting notes first."
                )


            else:


                with st.spinner(
                    "Agent is analyzing meeting notes..."
                ):


                    analysis = data_adapter.analyze_meeting_notes(
                        meeting_text.strip()
                    )



                analysis = clean_output(analysis)



                st.markdown(
                    """
                    <div class="app-card">

                    <div class="task-title">
                    📋 Action Items & Summary
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )



                st.markdown(analysis)