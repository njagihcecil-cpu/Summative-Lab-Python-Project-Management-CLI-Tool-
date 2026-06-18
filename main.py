"""
main.py — CLI entry point for the Project Management Tool.

Usage:
    python main.py <command> [options]

Run `python main.py --help` for a full list of commands.
"""

import argparse
import logging
import sys

from rich.console import Console
from rich.table import Table
from rich import print as rprint

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import load_data, save_data

console = Console()

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s | %(name)s | %(message)s",
)

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def find_user_dict(data: list[dict], name: str) -> dict | None:
    """Return the raw dict for a user by name, or None."""
    for user in data:
        if user["name"].lower() == name.lower():
            return user
    return None


def find_project_dict(data: list[dict], project_title: str) -> dict | None:
    """Search all users for a project matching project_title."""
    for user in data:
        for project in user["projects"]:
            if project["title"].lower() == project_title.lower():
                return project
    return None


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_add_user(args):
    """Create a new user (name + optional email)."""
    data = load_data()

    if find_user_dict(data, args.name):
        rprint(f"[yellow]⚠[/yellow]  User '[bold]{args.name}[/bold]' already exists.")
        return

    user = User(name=args.name, email=args.email or "")
    data.append(user.to_dict())

    if save_data(data):
        rprint(f"[green]✓[/green]  User '[bold]{args.name}[/bold]' added.")
    else:
        rprint("[red]✗[/red]  Failed to save data.")


def cmd_list_users(args):
    """Display all users in a rich table."""
    data = load_data()

    if not data:
        rprint("[dim]No users found.[/dim]")
        return

    table = Table(title="Users", show_lines=True)
    table.add_column("Name", style="bold cyan")
    table.add_column("Email")
    table.add_column("Projects", justify="center")

    for u in data:
        table.add_row(u["name"], u.get("email", ""), str(len(u["projects"])))

    console.print(table)


def cmd_add_project(args):
    """Add a project to a user."""
    data = load_data()
    user = find_user_dict(data, args.user)

    if not user:
        rprint(f"[red]✗[/red]  User '[bold]{args.user}[/bold]' not found.")
        return

    # Check for duplicate project title under this user
    for p in user["projects"]:
        if p["title"].lower() == args.title.lower():
            rprint(f"[yellow]⚠[/yellow]  Project '[bold]{args.title}[/bold]' already exists for this user.")
            return

    project = Project(
        title=args.title,
        description=args.description or "",
        due_date=args.due_date or "",
    )
    user["projects"].append(project.to_dict())

    if save_data(data):
        rprint(f"[green]✓[/green]  Project '[bold]{args.title}[/bold]' added to {args.user}.")
    else:
        rprint("[red]✗[/red]  Failed to save data.")


def cmd_list_projects(args):
    """List all projects for a specific user."""
    data = load_data()
    user = find_user_dict(data, args.user)

    if not user:
        rprint(f"[red]✗[/red]  User '[bold]{args.user}[/bold]' not found.")
        return

    projects = user["projects"]
    if not projects:
        rprint(f"[dim]{args.user} has no projects yet.[/dim]")
        return

    table = Table(title=f"{args.user}'s Projects", show_lines=True)
    table.add_column("Title", style="bold")
    table.add_column("Description")
    table.add_column("Due Date")
    table.add_column("Tasks", justify="center")

    for p in projects:
        total = len(p["tasks"])
        done = sum(1 for t in p["tasks"] if t.get("status") == "done")
        table.add_row(
            p["title"],
            p.get("description", ""),
            p.get("due_date", ""),
            f"{done}/{total}",
        )

    console.print(table)


def cmd_add_task(args):
    """Add a task to a project."""
    data = load_data()
    project = find_project_dict(data, args.project)

    if not project:
        rprint(f"[red]✗[/red]  Project '[bold]{args.project}[/bold]' not found.")
        return

    task = Task(
        title=args.title,
        assigned_to=args.assigned_to or "Unassigned",
    )
    project["tasks"].append(task.to_dict())

    if save_data(data):
        rprint(f"[green]✓[/green]  Task '[bold]{args.title}[/bold]' added to '{args.project}'.")
    else:
        rprint("[red]✗[/red]  Failed to save data.")


def cmd_list_tasks(args):
    """List all tasks in a project."""
    data = load_data()
    project = find_project_dict(data, args.project)

    if not project:
        rprint(f"[red]✗[/red]  Project '[bold]{args.project}[/bold]' not found.")
        return

    tasks = project["tasks"]
    if not tasks:
        rprint(f"[dim]No tasks in '{args.project}' yet.[/dim]")
        return

    table = Table(title=f"Tasks in '{project['title']}'", show_lines=True)
    table.add_column("Title", style="bold")
    table.add_column("Assigned To")
    table.add_column("Status", justify="center")

    for t in tasks:
        status = t.get("status", "pending")
        status_display = "[green]done[/green]" if status == "done" else "[yellow]pending[/yellow]"
        table.add_row(t["title"], t.get("assigned_to", "Unassigned"), status_display)

    console.print(table)


def cmd_complete_task(args):
    """Mark a task as done."""
    data = load_data()

    for user in data:
        for project in user["projects"]:
            if project["title"].lower() == args.project.lower():
                for task in project["tasks"]:
                    if task["title"].lower() == args.title.lower():
                        task["status"] = "done"
                        if save_data(data):
                            rprint(f"[green]✓[/green]  Task '[bold]{args.title}[/bold]' marked as done.")
                        else:
                            rprint("[red]✗[/red]  Failed to save data.")
                        return
                rprint(f"[red]✗[/red]  Task '[bold]{args.title}[/bold]' not found in '{args.project}'.")
                return

    rprint(f"[red]✗[/red]  Project '[bold]{args.project}[/bold]' not found.")


# ---------------------------------------------------------------------------
# CLI definition
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Construct and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="project-mgr",
        description="📋 Project Management CLI — manage users, projects, and tasks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py add-user --name Alex --email alex@example.com\n"
            "  python main.py add-project --user Alex --title 'CLI Tool' --due-date 2025-12-31\n"
            "  python main.py add-task --project 'CLI Tool' --title 'Write tests' --assigned-to Alex\n"
            "  python main.py complete-task --project 'CLI Tool' --title 'Write tests'\n"
        ),
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")
    subparsers.required = True

    # add-user
    p = subparsers.add_parser("add-user", help="Create a new user")
    p.add_argument("--name", required=True, help="User's display name")
    p.add_argument("--email", default="", help="User's email address (optional)")
    p.set_defaults(func=cmd_add_user)

    # list-users
    p = subparsers.add_parser("list-users", help="List all users")
    p.set_defaults(func=cmd_list_users)

    # add-project
    p = subparsers.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user", required=True, help="Owner's name")
    p.add_argument("--title", required=True, help="Project title")
    p.add_argument("--description", default="", help="Short description (optional)")
    p.add_argument("--due-date", default="", dest="due_date", help="Due date e.g. 2025-12-31 (optional)")
    p.set_defaults(func=cmd_add_project)

    # list-projects
    p = subparsers.add_parser("list-projects", help="List projects for a user")
    p.add_argument("--user", required=True, help="User's name")
    p.set_defaults(func=cmd_list_projects)

    # add-task
    p = subparsers.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True, help="Project title")
    p.add_argument("--title", required=True, help="Task title")
    p.add_argument("--assigned-to", default="Unassigned", dest="assigned_to", help="Assignee name (optional)")
    p.set_defaults(func=cmd_add_task)

    # list-tasks
    p = subparsers.add_parser("list-tasks", help="List tasks in a project")
    p.add_argument("--project", required=True, help="Project title")
    p.set_defaults(func=cmd_list_tasks)

    # complete-task
    p = subparsers.add_parser("complete-task", help="Mark a task as done")
    p.add_argument("--project", required=True, help="Project title")
    p.add_argument("--title", required=True, help="Task title")
    p.set_defaults(func=cmd_complete_task)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
