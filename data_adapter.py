from __future__ import annotations

from typing import List, Dict

import streamlit as st


from app.agent.database import Database
from app.agent.notes_database import NotesDatabase
from app.agent.controller import AgentController



# -----------------------------
# Persistent Controller
# -----------------------------

def get_controller():

    if "agent_controller" not in st.session_state:

        st.session_state.agent_controller = AgentController()


    return st.session_state.agent_controller




# -----------------------------
# Agent Runner
# -----------------------------

def run_agent(message):


    controller = get_controller()


    response = controller.run(message)



    # Save approval state

    if controller.pending_action:


        st.session_state.pending_action = (
            controller.pending_action
        )


    else:


        st.session_state.pending_action = None



    return str(response)





# -----------------------------
# TASK FUNCTIONS
# -----------------------------


def fetch_tasks() -> List[Dict]:

    database = Database()

    return database.get_all()



def create_task(
    title,
    description="",
    priority="Medium",
    due_date=None
):

    return run_agent(

        f"""
Create a task.

Title:
{title}

Description:
{description}

Priority:
{priority}

Due Date:
{due_date}

"""

    )




def update_task_status(task_id, status):

    return run_agent(
        f"Update task {task_id} status to {status}"
    )




def delete_task(task_id):

    return run_agent(
        f"Delete task {task_id}"
    )





# -----------------------------
# NOTES
# -----------------------------


def fetch_notes() -> List[Dict]:

    database = NotesDatabase()

    return database.get_all()



def create_note(title, content):

    return run_agent(

        f"""
Save a note.

Title:
{title}

Content:
{content}

"""

    )




def semantic_search_notes(query):

    return run_agent(
        f"Search my notes semantically for: {query}"
    )





# -----------------------------
# PLANNER
# -----------------------------


def generate_daily_plan(context=""):


    prompt = """
Create a productivity work plan for today.
"""


    if context:

        prompt += f"""

Additional Context:
{context}

"""


    return run_agent(prompt)





# -----------------------------
# MEETING ANALYSIS
# -----------------------------


def analyze_meeting_notes(notes_text):

    return run_agent(

        f"""
Extract action items from these meeting notes:

{notes_text}

"""

    )