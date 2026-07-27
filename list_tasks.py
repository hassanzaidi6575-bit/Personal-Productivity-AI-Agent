from app.agent.database import Database


database = Database()



def list_tasks(
    status=None,
    priority=None,
    due_date=None,
    tag=None
):

    tasks = database.get_all()


    filtered_tasks = []


    for task in tasks:


        if status and task.get("status") != status:
            continue


        if priority and task.get("priority") != priority:
            continue


        if due_date and task.get("due_date") != due_date:
            continue


        if tag and tag not in task.get("tags", []):
            continue


        filtered_tasks.append(task)



    return {

        "total_count": len(filtered_tasks),

        "tasks": filtered_tasks

    }