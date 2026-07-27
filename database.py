import json
import os
from datetime import datetime


class Database:

    def __init__(self):
        self.file_name = "tasks.json"
        self.data = []
        self.load()


    def load(self):

        if os.path.exists(self.file_name):

            with open(self.file_name, "r") as file:

                try:
                    self.data = json.load(file)

                except json.JSONDecodeError:
                    self.data = []



    def save(self):

        with open(self.file_name, "w") as file:

            json.dump(
                self.data,
                file,
                indent=4
            )



    def _next_id(self):

        # Use max existing id + 1 rather than len(self.data) + 1.
        # len(self.data) + 1 breaks after any delete, since the
        # list shrinks but past ids don't get reused or reserved,
        # leading to duplicate ids on the next add().

        if not self.data:
            return 1

        return max(task["id"] for task in self.data) + 1



    def add(self, item):

        item["id"] = self._next_id()

        today = datetime.now().strftime("%Y-%m-%d")

        item.setdefault("created_date", today)
        item.setdefault("updated_date", today)

        item.setdefault("status", "Pending")
        item.setdefault("priority", "Medium")
        item.setdefault("tags", [])
        item.setdefault("source", "user")
        item.setdefault("notes", "")


        self.data.append(item)

        self.save()

        return item



    def get_all(self):

        return self.data



    def get_by_id(self, task_id):

        for task in self.data:

            if task["id"] == task_id:
                return task

        return None



    def update(self, task_id, updates):

        task = self.get_by_id(task_id)


        if task:

            task.update(updates)

            task["updated_date"] = datetime.now().strftime("%Y-%m-%d")

            self.save()

            return task


        return None



    def delete(self, task_id):

        task = self.get_by_id(task_id)


        if task:

            self.data.remove(task)

            self.save()

            return task


        return None



    def complete(self, task_id):

        task = self.get_by_id(task_id)


        if task:

            task["status"] = "Completed"

            task["updated_date"] = datetime.now().strftime("%Y-%m-%d")

            self.save()

            return task


        return None



    def add_note(self, task_id, note):

        task = self.get_by_id(task_id)


        if task:

            task["notes"] = note

            task["updated_date"] = datetime.now().strftime("%Y-%m-%d")

            self.save()

            return task


        return None