"""Project model — groups tasks under a title and due date."""

from models.task import Task, Entity


class Project(Entity):
    """
    A project owned by a user, containing one or more tasks.

    Inherits from Entity for shared ID tracking.

    Attributes:
        title (str): Project name.
        description (str): Brief overview of the project.
        due_date (str): Target completion date (YYYY-MM-DD or freeform).
        tasks (list[Task]): Tasks belonging to this project.
    """

    def __init__(self, title: str, description: str = "", due_date: str = ""):
        super().__init__()
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks: list[Task] = []

    # --- property ---

    @property
    def task_count(self) -> int:
        """Total number of tasks in this project."""
        return len(self.tasks)

    @property
    def completed_count(self) -> int:
        """Number of completed tasks."""
        return sum(1 for t in self.tasks if t.completed)

    # --- methods ---

    def add_task(self, task: Task):
        """Append a Task object to this project."""
        self.tasks.append(task)

    def find_task(self, title: str) -> Task | None:
        """Return the first task matching title, or None."""
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def __str__(self):
        due = f" (due: {self.due_date})" if self.due_date else ""
        return f"{self.title}{due} — {self.completed_count}/{self.task_count} tasks done"

    def __repr__(self):
        return f"<Project title='{self.title}' tasks={self.task_count}>"

    def to_dict(self) -> dict:
        """Serialize to JSON-safe dict."""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @staticmethod
    def from_dict(data: dict) -> "Project":
        """Deserialize from a dict loaded out of JSON."""
        project = Project(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
        )
        project.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return project
