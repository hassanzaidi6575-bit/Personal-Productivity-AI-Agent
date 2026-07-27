from app.tools.create_task import create_task
from app.tools.list_tasks import list_tasks
from app.tools.update_task import update_task
from app.tools.complete_task import complete_task
from app.tools.delete_task import delete_task

from app.tools.save_note import save_note
from app.tools.search_notes import search_notes

from app.tools.meeting_actions import extract_meeting_actions
from app.tools.work_plan import generate_work_plan



ALL_TOOLS = [

    create_task,

    list_tasks,

    update_task,

    complete_task,

    delete_task,

    save_note,

    search_notes,

    extract_meeting_actions,

    generate_work_plan,

]