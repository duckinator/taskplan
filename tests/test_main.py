from freezegun import freeze_time
from taskplan.task_list import TaskList

@freeze_time("2020-09-21 15:00:00")
def test_main():
    task_strs = [
        "after 2pm move laundry to dryer",
        "after 12:30am get ready for bed",
        "before 5pm get ready for $thing",
        "after 2:30pm bork incessantly at the abyss",
    ]

    task_list = TaskList()
    for task in task_strs:
        task_list.add(task)

    tasks = []
    # Capture each item from the task list.
    for _ in range(4):
        task = task_list.next()
        tasks.append(task)
        task_list.done(task)

    # Sort the list.
    tasks = sorted(tasks)

    assert str(tasks[0]) == f"[0] {task_strs[0]}"
    assert str(tasks[1]) == f"[1] {task_strs[1]}"
    assert str(tasks[2]) == f"[2] {task_strs[2]}"
    assert str(tasks[3]) == f"[3] {task_strs[3]}"

    assert task_list.tasks == []
