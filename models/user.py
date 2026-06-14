from models.project import Project

class User:
    def __init__(self, name):
        self.name = name
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)

    def to_dict(self):
        return {
            "name": self.name,
            "projects": [project.to_dict() for project in self.projects]
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["name"])

        for project_data in data["projects"]:
            user.projects.append(Project.from_dict(project_data))

        return user