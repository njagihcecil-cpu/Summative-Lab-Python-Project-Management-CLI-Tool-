"""Task model — represents a single unit of work within a project."""


class Entity:
    """Base class providing shared ID counter and repr logic."""

    _count = 0

    def __init__(self):
        Entity._count += 1
        self.id = Entity._count

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"


class Task(Entity):
    """
    A task belonging to a project.

    Inherits from Entity for shared ID tracking.

    Attributes:
        title (str): Short description of the work.
        status (str): 'pending' or 'done'.
        assigned_to (str): Name of the person responsible.
    """

    VALID_STATUSES = ("pending", "done")

    def __init__(self, title: str, assigned_to: str = "Unassigned", status: str = "pending"):
        super().__init__()
        self.title = title
        self.assigned_to = assigned_to
        self._status = status  # private backing field for @property

    # --- property with setter ---

    @property
    def status(self) -> str:
        """Current status of the task."""
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        self._status = value

    @property
    def completed(self) -> bool:
        """Convenience bool — True when status is 'done'."""
        return self._status == "done"

    # --- methods ---

    def mark_complete(self):
        """Mark this task as done."""
        self.status = "done"

    def __str__(self):
        icon = "✓" if self.completed else "○"
        return f"[{icon}] {self.title} (assigned: {self.assigned_to})"

    def to_dict(self) -> dict:
        """Serialize to JSON-safe dict."""
        return {
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """Deserialize from a dict loaded out of JSON."""
        return Task(
            title=data["title"],
            assigned_to=data.get("assigned_to", "Unassigned"),
            status=data.get("status", "pending"),
        )
