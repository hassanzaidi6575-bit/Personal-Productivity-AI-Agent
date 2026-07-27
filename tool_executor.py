from app.agent.tools import ALL_TOOLS
from app.agent.approval import requires_approval, approval_message
import traceback



TOOLS_MAP = {
    tool.__name__: tool
    for tool in ALL_TOOLS
}




def execute_tool(tool_name, arguments=None, skip_approval=False):


    # Check tool exists

    if tool_name not in TOOLS_MAP:

        return {

            "success": False,

            "error": f"Tool '{tool_name}' not found"

        }



    if arguments is None:

        arguments = {}



    # -----------------------------
    # Human Approval Check
    # -----------------------------
    # skip_approval=True means the user has already approved this
    # exact action (e.g. via the "yes" flow in AgentController), so
    # we must not re-trigger the approval gate here.

    if requires_approval(tool_name) and not skip_approval:

        return {

            "success": False,

            "approval_required": True,

            "tool": tool_name,

            "arguments": arguments,

            "message": approval_message(tool_name)

        }




    tool = TOOLS_MAP[tool_name]



    try:

        result = tool(**arguments)


        return {

            "success": True,

            "tool": tool_name,

            "result": result

        }



    except TypeError as e:


        return {

            "success": False,

            "tool": tool_name,

            "error": "Invalid tool arguments",

            "details": str(e)

        }



    except Exception as e:


        return {

            "success": False,

            "tool": tool_name,

            "error": str(e),

            "details": traceback.format_exc()

        }