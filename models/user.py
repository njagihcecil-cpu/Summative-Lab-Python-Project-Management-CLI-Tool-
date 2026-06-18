"""User model — a person who owns projects."""

from models.project import Project
from models.task import Entity


class Person(Entity):
    """
    Base class for any person in the system.

    Attributes:
        name (str): Display name.
        email (str): Contact email.
    """

    def __init__(self, name: str, email: str = ""):
        super().__init__()
        self._name = name
        self._email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value

    def __repr__(self):
        return f"<{self.__class__.__name__} name='{self.name}'>"


class User(Person):
    """
    A registered user who owns one or more projects.

    Inherits from Person (which inherits from Entity).

    Attributes:
        projects (list[Project]): Projects belonging to this user.
    """

    def __init__(self, name: str, email: str = ""):
        super().__init__(name, email)
        self.projects: list[Project] = []

    # --- properties ---

    @property
    def project_count(self) -> int:
        """Number of projects this user owns."""
        return len(self.projects)

    # --- methods ---

    def add_project(self, project: Project):
        """Attach a Project to this user."""
        self.projects.append(project)

    def find_project(self, title: str) -> Project | None:
        """Return the first project matching title, or None."""
        for project in self.projects:
            if project.title == title:
                return project
        return None

    def __str__(self):
        email_str = f" <{self.email}>" if self.email else ""
        return f"{self.name}{email_str} — {self.project_count} project(s)"

    def to_dict(self) -> dict:
        """Serialize to JSON-safe dict."""
        return {
            "name": self.name,
            "email": self.email,
            "projects": [p.to_dict() for p in self.projects],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Deserialize from a dict loaded out of JSON."""
        user = cls(name=data["name"], email=data.get("email", ""))
        for project_data in data.get("projects", []):
            user.projects.append(Project.from_dict(project_data))
        return user
