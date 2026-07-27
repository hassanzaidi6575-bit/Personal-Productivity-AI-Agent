def requires_approval(tool_name):

    approval_tools = [
        "update_task",
        "complete_task",
    ]

    if tool_name in approval_tools:
        return True

    return False



def approval_message(tool_name):

    return f"""
The action '{tool_name}' requires your approval.

Do you want me to continue?

Reply with:
- yes
- no
"""