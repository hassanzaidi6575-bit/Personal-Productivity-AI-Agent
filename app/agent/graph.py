from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os
import json

from app.agent.state import AgentState
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.decision import build_decision_prompt

from app.agent.tool_executor import execute_tool
from app.agent.approval import requires_approval, approval_message
from app.agent.response_formatter import format_tool_response


load_dotenv()


llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)



# --------------------------------
# Decision Node
# --------------------------------

def decision_node(state: AgentState):

    user_message = state["messages"][-1]["content"]

    text = user_message.lower().strip()



    # ----------------------------
    # Approval YES
    # ----------------------------

    if text in ["yes", "y"]:

        pending = state.get(
            "pending_action",
            {}
        )


        if pending:

            return {

                "selected_tool": pending["tool"],

                "tool_arguments": pending["arguments"],

                "approved": True,

                "approval_required": False,

                "pending_action": pending,

                "next": "tool"

            }



        return {

            "next": "chat"

        }




    # ----------------------------
    # Approval NO
    # ----------------------------

    if text in ["no", "n"]:

        return {

            "messages": state["messages"] + [

                {
                    "role": "assistant",
                    "content": "Action cancelled."
                }

            ],

            "pending_action": {},

            "approved": False,

            "approval_required": False,

            "next": "chat"

        }





    # ----------------------------
    # Build LLM decision
    # ----------------------------

    prompt = build_decision_prompt(
        user_message
    )


    try:

        result = llm.invoke(prompt)


        decision = json.loads(
            result.content
        )



        # ---------------------------------
        # SAFETY TOOL ROUTING FIX
        # ---------------------------------

        if "delete task" in text or "remove task" in text:

            task_id = int(
                text.split()[-1]
            )


            decision = {

                "action": "tool",

                "tool": "delete_task",

                "arguments": {

                    "task_id": task_id

                },

                "approval_required": True

            }



        elif "complete task" in text:

            task_id = int(
                text.split()[-1]
            )


            decision = {

                "action": "tool",

                "tool": "complete_task",

                "arguments": {

                    "task_id": task_id

                },

                "approval_required": True

            }





        return {

            "selected_tool": decision.get(
                "tool"
            ),


            "tool_arguments": decision.get(
                "arguments",
                {}
            ),


            "approval_required": decision.get(
                "approval_required",
                False
            ),


            "approved": False,


            "next": (

                "tool"

                if decision.get("action") == "tool"

                else "chat"

            )

        }





    except Exception as e:


        return {

            "error": str(e),

            "next": "chat"

        }





# --------------------------------
# Chat Node
# --------------------------------

def chat_node(state: AgentState):


    result = llm.invoke(

        [

            ("system", SYSTEM_PROMPT),

            (
                "user",
                state["messages"][-1]["content"]
            )

        ]

    )


    return {


        "messages": state["messages"] + [

            {

                "role": "assistant",

                "content": result.content

            }

        ],


        "next": "end"

    }







# --------------------------------
# Tool Node
# --------------------------------

def tool_node(state: AgentState):


    tool_name = state.get(
        "selected_tool"
    )


    arguments = state.get(
        "tool_arguments",
        {}
    )



    # Approval required first time

    if requires_approval(tool_name) and not state.get("approved"):


        return {


            "messages": state["messages"] + [

                {

                    "role": "assistant",

                    "content": approval_message(tool_name)

                }

            ],


            "pending_action": {


                "tool": tool_name,

                "arguments": arguments

            },


            "approval_required": True,


            "approved": False,


            "next": "end"

        }






    # Execute approved tool

    result = execute_tool(

        tool_name,

        arguments,

        skip_approval=True

    )



    return {


        "messages": state["messages"] + [

            {

                "role": "assistant",

                "content": format_tool_response(result)

            }

        ],


        "tool_result": result,


        "pending_action": {},


        "approved": False,


        "approval_required": False,


        "next": "end"

    }







# --------------------------------
# Create Graph
# --------------------------------

def create_agent_graph():


    workflow = StateGraph(
        AgentState
    )



    workflow.add_node(
        "decision",
        decision_node
    )


    workflow.add_node(
        "chat",
        chat_node
    )


    workflow.add_node(
        "tool",
        tool_node
    )



    workflow.set_entry_point(
        "decision"
    )



    workflow.add_conditional_edges(

        "decision",

        lambda state: state["next"],

        {

            "tool": "tool",

            "chat": "chat"

        }

    )



    workflow.add_edge(
        "tool",
        END
    )


    workflow.add_edge(
        "chat",
        END
    )



    return workflow.compile()