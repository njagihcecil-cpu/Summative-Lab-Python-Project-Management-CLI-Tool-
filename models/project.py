from models.task import Task


class Project:
    def __init__(self, title):
        self.title = title
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def to_dict(self):
        return {
            "title": self.title,
            "tasks": [t.to_dict() for t in self.tasks]
        }

    @staticmethod
    def from_dict(data):
        project = Project(data["title"])
        project.tasks = [Task.from_dict(t) for t in data["tasks"]]
        return project