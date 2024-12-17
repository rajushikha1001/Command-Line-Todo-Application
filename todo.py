import argparse
import json
import os

# Define the file where tasks will be saved
TASKS_FILE = "tasks.json"


# Helper function to load tasks from the JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []


# Helper function to save tasks to the JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


# Function to add a new task
def add_task(task_name):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "task": task_name,
        "completed": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {task_name}")


# Function to list all tasks
def list_tasks():
    tasks = load_tasks()
    if tasks:
        print("Todo List:")
        for task in tasks:
            status = "Completed" if task["completed"] else "Pending"
            print(f"{task['id']}. {task['task']} - {status}")
    else:
        print("No tasks found.")


# Function to remove a task by its ID
def remove_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        tasks.remove(task)
        save_tasks(tasks)
        print(f"Task with ID {task_id} has been removed.")
    else:
        print(f"Task with ID {task_id} not found.")


# Function to mark a task as completed or pending
def toggle_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        task["completed"] = not task["completed"]
        save_tasks(tasks)
        status = "Completed" if task["completed"] else "Pending"
        print(f"Task with ID {task_id} is now marked as {status}.")
    else:
        print(f"Task with ID {task_id} not found.")


# Main function to parse command-line arguments
def main():
    parser = argparse.ArgumentParser(description="A simple command-line todo app.")
    
    # Add subcommands for each task (add, list, remove, toggle)
    subparsers = parser.add_subparsers()

    # Add task command
    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.add_argument("task_name", type=str, help="Name of the task to add.")
    add_parser.set_defaults(func=lambda args: add_task(args.task_name))

    # List tasks command
    subparsers.add_parser("list", help="List all tasks.").set_defaults(func=lambda args: list_tasks())

    # Remove task command
    remove_parser = subparsers.add_parser("remove", help="Remove a task by ID.")
    remove_parser.add_argument("task_id", type=int, help="ID of the task to remove.")
    remove_parser.set_defaults(func=lambda args: remove_task(args.task_id))

    # Toggle task completion (mark as complete or pending)
    toggle_parser = subparsers.add_parser("toggle", help="Mark a task as completed or pending.")
    toggle_parser.add_argument("task_id", type=int, help="ID of the task to toggle.")
    toggle_parser.set_defaults(func=lambda args: toggle_task(args.task_id))

    # Parse arguments and call the corresponding function
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
