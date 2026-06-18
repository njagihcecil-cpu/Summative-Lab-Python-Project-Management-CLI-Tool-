"""
tests/test_models.py
Unit tests for User, Project, Task models and storage utilities.
Run with: pytest tests/test_models.py -v
"""

import json
import os
import pytest

from models.task import Task
from models.project import Project
from models.user import User

class TestTask:
    def test_default_status_is_pending(self):
        task = Task("Write docs")
        assert task.status == "pending"

    def test_completed_property_false_by_default(self):
        task = Task("Write docs")
        assert task.completed is False

    def test_mark_complete_sets_status_done(self):
        task = Task("Write docs")
        task.mark_complete()
        assert task.status == "done"
        assert task.completed is True

    def test_status_setter_rejects_invalid_value(self):
        task = Task("Write docs")
        with pytest.raises(ValueError):
            task.status = "in-progress"

    def test_to_dict_contains_expected_keys(self):
        task = Task("Write docs", assigned_to="Alex")
        d = task.to_dict()
        assert d["title"] == "Write docs"
        assert d["assigned_to"] == "Alex"
        assert d["status"] == "pending"

    def test_from_dict_round_trip(self):
        original = Task("Deploy", assigned_to="Sam", status="done")
        restored = Task.from_dict(original.to_dict())
        assert restored.title == "Deploy"
        assert restored.assigned_to == "Sam"
        assert restored.completed is True

    def test_str_shows_check_when_complete(self):
        task = Task("Deploy")
        task.mark_complete()
        assert "✓" in str(task)

    def test_str_shows_circle_when_pending(self):
        task = Task("Deploy")
        assert "○" in str(task)

class TestProject:
    def test_new_project_has_no_tasks(self):
        project = Project("Alpha")
        assert project.task_count == 0

    def test_add_task_increments_count(self):
        project = Project("Alpha")
        project.add_task(Task("T1"))
        project.add_task(Task("T2"))
        assert project.task_count == 2

    def test_completed_count_tracks_done_tasks(self):
        project = Project("Alpha")
        t1 = Task("T1")
        t2 = Task("T2")
        t1.mark_complete()
        project.add_task(t1)
        project.add_task(t2)
        assert project.completed_count == 1

    def test_find_task_returns_correct_task(self):
        project = Project("Alpha")
        project.add_task(Task("Setup CI"))
        found = project.find_task("Setup CI")
        assert found is not None
        assert found.title == "Setup CI"

    def test_find_task_returns_none_for_missing(self):
        project = Project("Alpha")
        assert project.find_task("Ghost") is None

    def test_to_dict_serializes_tasks(self):
        project = Project("Alpha", description="Desc", due_date="2025-12-31")
        project.add_task(Task("T1"))
        d = project.to_dict()
        assert d["title"] == "Alpha"
        assert d["description"] == "Desc"
        assert len(d["tasks"]) == 1

    def test_from_dict_round_trip(self):
        project = Project("Beta", due_date="2025-06-01")
        project.add_task(Task("Build"))
        restored = Project.from_dict(project.to_dict())
        assert restored.title == "Beta"
        assert restored.task_count == 1


# ---------------------------------------------------------------------------
# User tests
# ---------------------------------------------------------------------------

class TestUser:
    def test_new_user_has_no_projects(self):
        user = User("Alex")
        assert user.project_count == 0

    def test_add_project_increments_count(self):
        user = User("Alex")
        user.add_project(Project("P1"))
        assert user.project_count == 1

    def test_find_project_returns_correct_project(self):
        user = User("Alex")
        user.add_project(Project("CLI Tool"))
        found = user.find_project("CLI Tool")
        assert found is not None

    def test_find_project_returns_none_for_missing(self):
        user = User("Alex")
        assert user.find_project("Ghost") is None

    def test_name_setter_rejects_empty_string(self):
        user = User("Alex")
        with pytest.raises(ValueError):
            user.name = "   "

    def test_to_dict_includes_email(self):
        user = User("Alex", email="alex@example.com")
        d = user.to_dict()
        assert d["email"] == "alex@example.com"

    def test_from_dict_round_trip(self):
        user = User("Sam", email="sam@test.com")
        user.add_project(Project("Alpha"))
        restored = User.from_dict(user.to_dict())
        assert restored.name == "Sam"
        assert restored.email == "sam@test.com"
        assert restored.project_count == 1

class TestInheritance:
    def test_user_is_subclass_of_person(self):
        from models.user import Person
        user = User("Alex")
        assert isinstance(user, Person)

    def test_task_has_id(self):
        task = Task("Test")
        assert hasattr(task, "id")
        assert isinstance(task.id, int)

    def test_project_has_id(self):
        project = Project("Test")
        assert hasattr(project, "id")
