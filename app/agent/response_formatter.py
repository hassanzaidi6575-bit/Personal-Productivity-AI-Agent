def format_tool_response(tool_result):

    print("FORMATTER CALLED")

    if not tool_result:
        return "❌ No result received."

    # -------------------------
    # Outer Tool Failure
    # -------------------------

    if not tool_result.get("success"):

        error = (
            tool_result.get("error")
            or tool_result.get("message")
            or "Unknown error"
        )

        return (
            "❌ Action failed\n\n"
            f"{error}"
        )

    result = tool_result.get("result", {})

    if not result:
        return "No data returned."

    # -------------------------
    # Nested Tool Failure
    # -------------------------

    if isinstance(result, dict) and result.get("success") is False:

        return (
            "❌ Action failed\n\n"
            f"{result.get('message', 'Unknown error')}"
        )

    # -------------------------
    # Delete Task
    # -------------------------

    if isinstance(result, dict) and result.get("message") == "Task deleted successfully":

        task = result.get("task", {})

        return (
            "🗑️ Task deleted successfully\n\n"
            f"Title: {task.get('title','Unknown Task')}\n"
            f"Priority: {task.get('priority','')}\n"
            f"Status: {task.get('status','')}"
        )

    # -------------------------
    # Task List Response
    # -------------------------

    if "tasks" in result:

        tasks = result.get("tasks", [])

        if not tasks:
            return "📋 No tasks found."

        output = "📋 Your Tasks\n\n"

        for i, task in enumerate(tasks):

            output += (
                f"{i+1}. {task.get('title','Untitled Task')}\n"
                f"   Status: {task.get('status','Pending')}\n"
                f"   Priority: {task.get('priority','Medium')}\n\n"
            )

        return output

    # -------------------------
    # Note Saved Response
    # -------------------------

    if "note_id" in result:

        return (
            "✅ Note saved successfully\n\n"
            f"Note ID: {result.get('note_id','')}\n"
            f"Title: {result.get('title','')}"
        )

    # -------------------------
    # Task Created / Updated / Completed
    # -------------------------

    if "confirmation" in result:

        response = (
            f"✅ {result.get('confirmation')}\n\n"
            f"Task ID: {result.get('task_id','')}"
        )

        if result.get("status"):

            response += (
                f"\nStatus: {result.get('status')}"
            )

        return response

    # -------------------------
    # Meeting Analysis
    # -------------------------

    if "meeting_analysis" in result:

        return (
            "✅ Meeting analysis completed:\n\n"
            f"{result.get('meeting_analysis')}"
        )

    # -------------------------
    # Semantic Search
    # -------------------------

    if "results" in result:

        return (
            "🔎 Search Results:\n\n"
            f"{result.get('results')}"
        )

    # -------------------------
    # Work Plan
    # -------------------------

    if "work_plan" in result:

        return (
            "📅 Daily Work Plan\n\n"
            f"Date: {result.get('date','')}\n"
            f"Available Hours: {result.get('available_hours','')}\n\n"
            f"{result.get('work_plan')}"
        )

    # -------------------------
    # Generic Success Response
    # -------------------------

    return str(result)