from app.agent.database import Database
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from datetime import datetime
import os



load_dotenv()



database = Database()



llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)





def generate_work_plan(
    available_hours,
    date=None,
    user_priorities=None
):


    # Always use the real current date
    date = datetime.now().strftime("%Y-%m-%d")



    tasks = database.get_all()



    if user_priorities is None:

        user_priorities = []





    prompt = f"""

Create a daily work plan.


Date:
{date}



Available Hours:
{available_hours}



User Priorities:
{user_priorities}



Tasks:

{tasks}



Return:

1. Ordered Schedule

2. Recommended Focus Areas

3. Deferred Tasks

4. Risk Warnings



Consider:

- Priority
- Deadline
- Task status
- Estimated effort

"""



    result = llm.invoke(prompt)





    return {

        "date": date,

        "available_hours": available_hours,

        "work_plan": result.content,

        "status": "generated"

    }