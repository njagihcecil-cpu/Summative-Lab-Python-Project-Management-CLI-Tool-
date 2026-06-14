import argparse
from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import load_data, save_data


def find_user(data, name):
    for user in data:
        if user["name"] == name:
            return user
    return None


def add_user(name):
    data = load_data()

    if find_user(data, name):
        print("User already exists")
        return

    user = User(name)
    data.append(user.to_dict())
    save_data(data)

    print("User added")


def list_users():
    data = load_data()

    for u in data:
        print(u["name"])


def add_project(username, title):
    data = load_data()
    user = find_user(data, username)

    if not user:
        print("User not found")
        return

    project = Project(title)
    user["projects"].append(project.to_dict())

    save_data(data)
    print("Project added")


def add_task(project_title, task_title):
    data = load_data()

    for user in data:
        for project in user["projects"]:
            if project["title"] == project_title:
                task = Task(task_title)
                project["tasks"].append(task.to_dict())
                save_data(data)
                print("Task added")
                return

    print("Project not found")


def complete_task(project_title, task_title):
    data = load_data()

    for user in data:
        for project in user["projects"]:
            if project["title"] == project_title:
                for task in project["tasks"]:
                    if task["title"] == task_title:
                        task["completed"] = True
                        save_data(data)
                        print("Task completed")
                        return

    print("Task not found")


# CLI
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

p1 = subparsers.add_parser("add-user")
p1.add_argument("--name", required=True)

p2 = subparsers.add_parser("list-users")

p3 = subparsers.add_parser("add-project")
p3.add_argument("--user", required=True)
p3.add_argument("--title", required=True)

p4 = subparsers.add_parser("add-task")
p4.add_argument("--project", required=True)
p4.add_argument("--title", required=True)

p5 = subparsers.add_parser("complete-task")
p5.add_argument("--project", required=True)
p5.add_argument("--title", required=True)

args = parser.parse_args()

if args.command == "add-user":
    add_user(args.name)

elif args.command == "list-users":
    list_users()

elif args.command == "add-project":
    add_project(args.user, args.title)

elif args.command == "add-task":
    add_task(args.project, args.title)

elif args.command == "complete-task":
    complete_task(args.project, args.title)

else:
    parser.print_help()