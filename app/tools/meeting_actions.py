from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


load_dotenv()


llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)



def extract_meeting_actions(meeting_notes):


    prompt = f"""
Extract structured information from these meeting notes.

Meeting Notes:

{meeting_notes}


Return in this format:

Summary:
-

Decisions:
-

Action Items:
-

Owners:
-

Deadlines:
-

Unresolved Questions:
-
"""


    result = llm.invoke(prompt)


    return {

        "meeting_analysis": result.content,

        "status": "completed"

    }