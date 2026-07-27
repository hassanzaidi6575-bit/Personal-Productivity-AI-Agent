from app.agent.notes_database import NotesDatabase


notes_database = NotesDatabase()



def save_note(
    title,
    content,
    category="General",
    tags=None
):

    if tags is None:
        tags = []


    note = {

        "title": title,

        "content": content,

        "category": category,

        "tags": tags

    }


    saved_note = notes_database.add(note)


    return {

        "note_id": saved_note["id"],

        "title": saved_note["title"],

        "confirmation": "Note saved successfully"

    }