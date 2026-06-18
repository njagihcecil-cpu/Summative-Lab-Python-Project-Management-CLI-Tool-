# Project Management CLI

A command-line tool for managing users, projects, and tasks — built with Python, argparse, and rich.

## Setup

```bash
# Clone the repo
git clone <your-repo-url>
cd project_mgr

# Install dependencies
pip install -r requirements.txt

# Run any command
python main.py --help
```

## Commands

### Users

```bash
# Add a user
python main.py add-user --name Alex --email alex@example.com

# List all users
python main.py list-users
```

### Projects

```bash
# Add a project to a user
python main.py add-project --user Alex --title "CLI Tool" --description "Build the CLI" --due-date 2025-12-31

# List all projects for a user
python main.py list-projects --user Alex
```

### Tasks

```bash
# Add a task to a project
python main.py add-task --project "CLI Tool" --title "Write tests" --assigned-to Alex

# List all tasks in a project
python main.py list-tasks --project "CLI Tool"

# Mark a task complete
python main.py complete-task --project "CLI Tool" --title "Write tests"
```

## Running Tests

```bash
pytest tests/test_models.py -v
```

## Project Structure

```
project_mgr/
├── main.py            # CLI entry point
├── requirements.txt
├── README.md
├── data/
│   └── database.json  # Auto-created on first save
├── models/
│   ├── task.py        # Task (inherits Entity)
│   ├── project.py     # Project (inherits Entity)
│   └── user.py        # User (inherits Person → Entity)
├── utils/
│   └── storage.py     # JSON load/save with error handling
└── tests/
    └── test_models.py # pytest unit tests
```

## Features

- Persistent JSON storage (auto-creates `data/` directory)
- Rich terminal tables for all list commands
- Full OOP hierarchy: `Entity → Person → User`, `Entity → Task/Project`
- `@property` with validation on Task status and User name
- Error handling for missing files, malformed JSON, duplicate entries
- 15+ unit tests covering all major model behaviours

## Known Issues

- Project titles must be unique across all users (search is global)
- No authentication — single admin user assumed
