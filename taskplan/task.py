from datetime import datetime
from dateutil.parser import parse as du_parse

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

    def __lt__(self, other):
        return self.task_id < other.task_id
