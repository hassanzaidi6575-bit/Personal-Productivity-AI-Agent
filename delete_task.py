from app.agent.database import Database


def delete_task(task_id):

    database = Database()

    try:

        task_id = int(task_id)

        result = database.delete(task_id)

        if result:

            return {

                "success": True,

                "confirmation": "Task deleted successfully",

                "task_id": task_id,

                "deleted_task": result

            }

        return {

            "success": False,

            "message": "Task not found"

        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)

        }