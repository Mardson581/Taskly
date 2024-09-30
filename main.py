from tasklist import TaskStatus, Task
from taskmanager import TaskManager
from argparse import ArgumentParser

def main():
    _choices=["add", "update", "delete", "mark-in-progress", "mark-done", "list"]
    parser = ArgumentParser(prog="Taskly", description="An cli app to manage tasks")
    parser.add_argument(
        "command",
        choices=_choices,
        action="append",
        help="What you want to do. You can add, update, delete, mark-in-progress, mark-done or list tasks"
    )
    parser.add_argument("option", help="The task description or ID", default=None, nargs="?")
    parser.add_argument("second_option", help="The task description or ID", default=None, nargs="?")
    args = parser.parse_args()

    command = None
    option = None
    second_option = None
    
    if args.command:
        command = args.command[0]
    if args.option:
        option = args.option
    if args.second_option:
        second_option = args.second_option
    manager = TaskManager()

    if command == "add":
        if option is not None:
            manager.save(Task(description=args.option, status=TaskStatus.TO_DO))
            manager.close()
            return
    if command == "update":
        if args.option[0] and second_option:
            manager.update(int(args.option), second_option)
            manager.close()
            return
    if command == "delete":
        if option is not None:
            manager.delete(int(args.option))
            manager.close()
            return
    if command == "mark-in-progress":
        if option is not None:
            manager.update_status(int(option), TaskStatus.IN_PROGRESS)
            manager.close()
            return
    if command == "mark-done":
        if option is not None:
            manager.update_status(int(option), TaskStatus.DONE)
            manager.close()
            return
    if command == "list":
        status = None
        if option == "done":
            status = TaskStatus.DONE
        elif option == "todo":
            status = TaskStatus.TO_DO
        elif option == "in-progress":
            status = TaskStatus.IN_PROGRESS
        manager.list(status)
        manager.close()
        return
    
    parser.print_help()

if __name__ == "__main__":
    main()