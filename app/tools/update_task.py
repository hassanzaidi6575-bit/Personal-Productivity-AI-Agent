from app.agent.database import Database


database = Database()



def update_task(task_id, updates):

    task = database.update(
        task_id,
        updates
    )


    if not task:

        return {
            "success": False,
            "message": "Task not found"
        }


    return {

        "success": True,

        "task_id": task["id"],

        "updated_task": task,

        "confirmation": "Task updated successfully"

    }