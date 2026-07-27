TOOLS_SCHEMA = [

    {
        "name": "create_task",
        "description": "Create a new productivity task.",
        "parameters": {
            "title": "string",
            "description": "string",
            "priority": "string",
            "due_date": "string",
            "tags": "list"
        }
    },


    {
        "name": "list_tasks",
        "description": "Retrieve tasks with optional filters.",
        "parameters": {
            "status": "string",
            "priority": "string",
            "due_date": "string",
            "tag": "string"
        }
    },


    {
        "name": "update_task",
        "description": "Update an existing task. Requires approval before execution.",
        "parameters": {
            "task_id": "integer",
            "updates": "dictionary"
        }
    },


    {
        "name": "complete_task",
        "description": "Mark a task as completed. Requires approval before execution.",
        "parameters": {
            "task_id": "integer"
        }
    },


    {
        "name": "delete_task",
        "description": "Delete an existing task permanently. Requires approval before execution.",
        "parameters": {
            "task_id": "integer"
        }
    },


    {
        "name": "save_note",
        "description": "Save a new note.",
        "parameters": {
            "title": "string",
            "content": "string",
            "category": "string",
            "tags": "list"
        }
    },


    {
        "name": "search_notes",
        "description": "Search notes using semantic similarity.",
        "parameters": {
            "query": "string",
            "category": "string",
            "date_range": "string"
        }
    },


    {
        "name": "extract_meeting_actions",
        "description": "Extract summary, decisions, action items, owners, deadlines, and questions from meeting notes.",
        "parameters": {
            "meeting_notes": "string"
        }
    },


    {
        "name": "generate_work_plan",
        "description": "Generate a daily work plan based on tasks and priorities.",
        "parameters": {
            "available_hours": "string",
            "date": "string",
            "user_priorities": "list"
        }
    }

]