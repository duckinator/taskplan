from pathlib import Path
import sys
from .task_list import TaskList


CONFIG_FILE = "~/.config/taskplan.txt"


def cli_add(argv):
    if len(argv) < 4:
        print_help()
        sys.exit(1)

    task_list = TaskList(CONFIG_FILE)
    task_list.add(' '.join(argv[1:]))
    task_list.save()


def cli_done(args):
    if len(args) > 3:
        print_help()
        sys.exit(1)

    task_list = TaskList(CONFIG_FILE)
    task_list.done(int(args[2]))
    task_list.save()


def cli_list(args):
    if len(args) > 2:
        print_help()
        sys.exit(1)

    task_list = TaskList(CONFIG_FILE)
    for task in task_list.tasks:
        print(task)


def cli_next(argv):
    if len(argv) > 2:
        print_help()
        sys.exit(1)

    task_list = TaskList(CONFIG_FILE)
    print(task_list.next())


def print_help():
    print("Usage: taskplan MODIFIER TIME TASK")
    print("       taskplan -- TASK")
    print("       taskplan done TASK_ID")
    print("       taskplan next")
    print("       taskplan list")


def main(argv=None):
    if argv is None:
        argv = sys.argv

    if len(argv) == 2 and ' ' in argv[1]:
        argv = [argv[0], *argv[1].split(' ')]

    if '--help' in argv or len(argv) < 2:
        print_help()
        sys.exit(1)

    commands = {
        '--':       cli_add,
        'after':    cli_add,
        'before':   cli_add,
        'by':       cli_add,
        'done':     cli_done,
        'list':     cli_list,
        'next':     cli_next,
    }
    commands[argv[1]](argv)
