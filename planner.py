#!/usr/bin/env python3

from datetime import datetime
import random

from dateutil.parser import parse as du_parse
from freezegun import freeze_time

class Task:
    """An individual task."""

    def __init__(self, task_str, task_id):
        self._task_str = task_str
        self.task_id = task_id
        self.condition = self._parse_condition(self._task_str)

    @staticmethod
    def _parse_condition(task_str):
        """Extract the condition, if any, from the task string."""
        keyword, arg, _task = task_str.split(' ', 2)
        if keyword in ['by', 'before']:
            return lambda t: t <= du_parse(arg)
        if keyword in ['after']:
            return lambda t: t >= du_parse(arg)
        return lambda _t: True

    def ready(self):
        """Returns True if the condition for running the task is resolved."""
        return self.condition(datetime.now())

    def __str__(self):
        return f"[{self.task_id}] {self._task_str}"

class TaskList:
    """A list of tasks."""

    def __init__(self):
        self.tasks = []
        self.finished_tasks = []

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
        return f"Done: {task}"

    def next(self):
        """Returns a random task."""
        valid_tasks = list(filter(Task.ready, self.tasks))

        if not valid_tasks:
            return None

        return random.choice(valid_tasks)


@freeze_time("2020-09-21 15:00:00")
def main():
    t = TaskList()
    t.add("after 2pm move laundry to dryer")
    t.add("after 12:30am get ready for bed")
    t.add("before 5pm get ready for $thing")
    t.add("after 2:30pm bork incessantly at the abyss")

    for _ in range(0, 5):
        task = t.next()
        print(task)
        if task:
            print(t.done(task))


if __name__ == "__main__":
    main()
