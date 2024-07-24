import os
import psutil
import datetime
import json
import argparse
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

class DailyTool:
    def __init__(self):
        self.tasks_file = "tasks.json"
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as file:
                return json.load(file)
        return {}

    def save_tasks(self):
        with open(self.tasks_file, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, task, due_date):
        task_id = len(self.tasks) + 1
        self.tasks[task_id] = {"task": task, "due_date": due_date, "completed": False}
        self.save_tasks()

    def list_tasks(self):
        for task_id, task_info in self.tasks.items():
            status = "Done" if task_info["completed"] else "Pending"
            print(f"Task ID: {task_id}, Task: {task_info['task']}, Due: {task_info['due_date']}, Status: {status}")

    def complete_task(self, task_id):
        if task_id in self.tasks:
            self.tasks[task_id]["completed"] = True
            self.save_tasks()
        else:
            print(f"Task ID {task_id} not found.")

    def system_monitor(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory_info.percent}%")

    def quick_reference(self, topic):
        references = {
            "python": "Python is an interpreted, high-level, general-purpose programming language.",
            "docker": "Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers.",
            "kubernetes": "Kubernetes is an open-source container-orchestration system for automating computer application deployment, scaling, and management.",
            # Add more topics as needed
        }
        print(references.get(topic.lower(), "Topic not found."))

def main():
    tool = DailyTool()

    menu = """Choose an option:
    1. Add Task
    2. List Tasks
    3. Complete Task
    4. System Monitor
    5. Quick Reference
    6. Exit
    """
    options_completer = WordCompleter(['1', '2', '3', '4', '5', '6'])

    while True:
        choice = prompt(menu, completer=options_completer)
        
        if choice == '1':
            task = prompt("Enter the task description: ")
            due_date = prompt("Enter the due date (YYYY-MM-DD): ")
            tool.add_task(task, due_date)
            print("Task added.")
        elif choice == '2':
            tool.list_tasks()
        elif choice == '3':
            task_id = int(prompt("Enter the task ID to complete: "))
            tool.complete_task(task_id)
            print("Task completed.")
        elif choice == '4':
            tool.system_monitor()
        elif choice == '5':
            topic = prompt("Enter the topic for quick reference: ")
            tool.quick_reference(topic)
        elif choice == '6':
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
