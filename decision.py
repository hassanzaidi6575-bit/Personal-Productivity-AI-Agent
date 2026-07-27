import json

from app.agent.agent_tools_schema import TOOLS_SCHEMA


def build_decision_prompt(user_message):

    return f"""

You are a tool selection engine for a Personal Productivity AI Agent.

You MUST select a tool whenever the user request matches a tool.

Never return:
- tool: none
- tool: null

Available tools:

{json.dumps(TOOLS_SCHEMA, indent=4)}


STRICT COMMAND MAPPING:


If user says:

"show tasks"
"list tasks"
"view tasks"

Return:

{{
"action":"tool",
"tool":"list_tasks",
"arguments":{{}},
"approval_required":false
}}


If user says:

"complete task X"
"finish task X"
"mark task X complete"

Return:

{{
"action":"tool",
"tool":"complete_task",
"arguments":{{"task_id":X}},
"approval_required":true
}}


If user says:

"delete task X"
"remove task X"
"erase task X"

Return:

{{
"action":"tool",
"tool":"delete_task",
"arguments":{{"task_id":X}},
"approval_required":true
}}


If user says:

"update task X"

Return:

{{
"action":"tool",
"tool":"update_task",
"arguments":{{"task_id":X}},
"approval_required":true
}}


For all other requests choose chat.


Return ONLY JSON.

User request:

{user_message}

"""