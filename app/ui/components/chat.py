"""
chat.py
-------
Conversational interface to the LangGraph agent.

Features:
- Chat with productivity agent
- Display user and agent messages
- Display agent execution trace
- Professional task response cards
"""

import streamlit as st

from app.ui import data_adapter



def render_chat_page():

    st.markdown(
        """
        <div class="section-title">
            🤖 AI Assistant
        </div>

        <div class="section-subtitle">
            Chat with your LangGraph-powered productivity agent.
            It can create tasks, save notes, search, and plan your day.
        </div>
        """,
        unsafe_allow_html=True,
    )


    # -------------------------
    # Memory
    # -------------------------

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []


    if "activity_log" not in st.session_state:

        st.session_state.activity_log = []




    # -------------------------
    # Display Messages
    # -------------------------

    for msg in st.session_state.chat_history:

        _render_bubble(
            msg["role"],
            msg["content"]
        )




    st.markdown("---")




    # -------------------------
    # Input
    # -------------------------

    with st.form(
        "chat_form",
        clear_on_submit=True
    ):


        user_input = st.text_input(
            "Message",
            placeholder="Ask your agent anything...",
            label_visibility="collapsed"
        )


        send = st.form_submit_button(
            "Send ➤",
            use_container_width=True
        )





    if send and user_input.strip():


        st.session_state.chat_history.append(

            {
                "role": "user",
                "content": user_input.strip()
            }

        )


        with st.spinner(
            "Agent is thinking..."
        ):


            response = data_adapter.run_agent(
                user_input.strip()
            )



            controller = data_adapter.get_controller()


            st.session_state.activity_log = (
                controller.get_activity_log()
            )



        st.session_state.chat_history.append(

            {
                "role": "assistant",
                "content": response
            }

        )


        st.rerun()






    # -------------------------
    # Agent Trace
    # -------------------------

    if st.session_state.activity_log:


        st.subheader(
            "🤖 Agent Execution Trace"
        )


        with st.expander(
            "View Agent Processing Steps",
            expanded=False
        ):


            for step in st.session_state.activity_log:


                st.success(
                    step
                )







    # -------------------------
    # Clear
    # -------------------------

    if st.session_state.chat_history:


        if st.button(
            "🧹 Clear Conversation"
        ):


            st.session_state.chat_history = []

            st.session_state.activity_log = []

            st.rerun()







# -------------------------
# Message Renderer
# -------------------------

def _render_bubble(
    role: str,
    content: str
):


    if role == "user":


        with st.chat_message("user"):

            st.write(content)



    else:


        with st.chat_message("assistant"):


            # -------------------------
            # Task Card Detection
            # -------------------------

            if (
                "Completed" in content
                or "Pending" in content
                or "In Progress" in content
            ):


                st.subheader(
                    "📋 Your Tasks"
                )


                tasks = content.split("\n")



                for task in tasks:


                    task = task.strip()


                    if task:


                        with st.container(border=True):


                            if "Completed" in task:


                                st.success(
                                    task
                                )


                            elif "In Progress" in task:


                                st.info(
                                    task
                                )


                            elif "Pending" in task:


                                st.warning(
                                    task
                                )


                            else:


                                st.write(
                                    task
                                )



            else:


                st.write(content)