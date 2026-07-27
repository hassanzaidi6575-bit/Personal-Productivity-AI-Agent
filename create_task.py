from app.agent.database import Database


database = Database()



def create_task(
    title,
    description="",
    priority="Medium",
    due_date=None,
    tags=None
):

    if tags is None:
        tags = []


    task = {

        "title": title,

        "description": description,

        "priority": priority,

        "due_date": due_date,

        "tags": tags,

        "source": "user",

        "notes": ""

    }


    created_task = database.add(task)


    return {

        "task_id": created_task["id"],

        "title": created_task["title"],

        "status": created_task["status"],

        "confirmation": "Task created successfully"

    }