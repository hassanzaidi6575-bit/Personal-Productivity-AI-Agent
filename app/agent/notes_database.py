import json
import os
from datetime import datetime


class NotesDatabase:


    def __init__(self):

        self.file_name = "notes.json"
        self.notes = []

        self.load()



    def load(self):

        if os.path.exists(self.file_name):

            with open(self.file_name, "r") as file:

                try:
                    self.notes = json.load(file)

                except json.JSONDecodeError:
                    self.notes = []



    def save(self):

        with open(self.file_name, "w") as file:

            json.dump(
                self.notes,
                file,
                indent=4
            )



    def get_all(self):

        return self.notes



    def get_by_id(self, note_id):

        for note in self.notes:

            if note["id"] == note_id:

                return note


        return None



    def add(self, note):

        note["id"] = len(self.notes) + 1


        today = datetime.now().strftime("%Y-%m-%d")


        note.setdefault(
            "created_date",
            today
        )

        note.setdefault(
            "updated_date",
            today
        )


        self.notes.append(note)

        self.save()


        return note



    def update(self, note_id, updates):

        note = self.get_by_id(note_id)


        if note:

            note.update(updates)

            note["updated_date"] = datetime.now().strftime("%Y-%m-%d")

            self.save()

            return note


        return None



    def delete(self, note_id):

        note = self.get_by_id(note_id)


        if note:

            self.notes.remove(note)

            self.save()

            return note


        return None