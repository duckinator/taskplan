from pathlib import Path
import random
from .task import Task

class TaskList:
    """A list of tasks."""

    def __init__(self, filename=None):
        self.tasks = []
        self.finished_tasks = []

        self.filename = filename
        if filename:
            self.load()

    def load(self):
        path = Path(self.filename).expanduser()
        if not path.exists():
            return

        tasks = path.read_text().splitlines()
        self.tasks = []
        self.finished_tasks = []
        for task in tasks:
            task_id, task = task.split('=', 1)
            self.tasks.append(Task(task, int(task_id)))

    def save(self):
        file_obj = Path(self.filename).expanduser()
        text = "\n".join([f"{task.task_id}={task._task_str}" for task in self.tasks]) + "\n"
        file_obj.write_text(text)
        return file_obj

    def add(self, task_str):
        """Adds one or more tasks."""
        task = Task(task_str, len(self.tasks))
        self.tasks.append(task)
        return task

    def find(self, task_id):
        """Find a task by its ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def done(self, task_id):
        """Mark as task as done."""
        if isinstance(task_id, Task):
            task_id = task_id.task_id
        task = self.find(task_id)
        task_idx = self.tasks.index(task)
        self.finished_tasks.append(self.tasks.pop(task_idx))
        return task

    def next(self):
        """Returns a random task."""
        valid_tasks = list(filter(Task.ready, self.tasks))

        if not valid_tasks:
            return None

        return random.choice(valid_tasks)
