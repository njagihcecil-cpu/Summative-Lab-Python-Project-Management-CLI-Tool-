from models.task import Task

def test_task_complete():
    task = Task("Test Task")

    task.mark_complete()

    assert task.completed == True