from app.agent.database import Database
from datetime import datetime


database = Database()



def complete_task(task_id):


    task = database.complete(task_id)


    if not task:

        return {

            "success": False,

            "message": "Task not found"

        }



    task["completion_timestamp"] = datetime.now().isoformat()


    database.save()



    return {

        "success": True,

        "task_id": task_id,

        "status": "Completed",

        "completion_timestamp": task["completion_timestamp"],

        "confirmation": "Task completed successfully"

    }