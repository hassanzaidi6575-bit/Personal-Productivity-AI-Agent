from app.agent.database import Database
from app.agent.notes_database import NotesDatabase

from app.vectorstore.embedding import create_embedding
from app.vectorstore.chroma_db import add_to_vectorstore



database = Database()

notes_database = NotesDatabase()



def sync_database_to_vectorstore():


    # Sync Tasks

    tasks = database.get_all()


    for index, task in enumerate(tasks):


        text = f"""
Task Title: {task['title']}

Description: {task.get('description', '')}

Priority: {task.get('priority', 'Medium')}

Status: {task.get('status', 'Pending')}

Tags: {', '.join(task.get('tags', []))}

Notes: {task.get('notes', '')}
"""


        embedding = create_embedding(text)


        add_to_vectorstore(
            id=f"task_{index}",
            text=text.strip(),
            embedding=embedding,
            metadata={
                "type": "task"
            }
        )




    # Sync Notes

    notes = notes_database.get_all()


    for index, note in enumerate(notes):


        text = f"""
Note Title: {note['title']}

Content: {note['content']}

Category: {note.get('category', '')}

Tags: {', '.join(note.get('tags', []))}
"""


        embedding = create_embedding(text)


        add_to_vectorstore(
            id=f"note_{index}",
            text=text.strip(),
            embedding=embedding,
            metadata={
                "type": "note"
            }
        )



    print("Tasks and Notes synced with ChromaDB successfully!")