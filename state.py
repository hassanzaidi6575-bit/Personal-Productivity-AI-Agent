from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):

    messages: List[Dict[str, str]]

    next: str

    result: str

    selected_tool: str

    tool_arguments: Dict[str, Any]

    tool_result: Any

    approval_required: bool

    approved: bool

    pending_action: Dict[str, Any]

    error: str