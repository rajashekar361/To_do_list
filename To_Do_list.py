from datetime import datetime
from prettytable import PrettyTable



def welcome():
    print("Welcome to your to-do list!")
    print('To view your tasks, please write "Tasks"')
    print('To add a task to your list, please write "Add"')
    print('To mark a task as completed, please write "Completed"')
    print('To delete a task, please write "Delete"')    
    print('To exit the app, please write "Exit"')

class TaskMemento:
    def __init__(self, task_list):
        self._state = [task.__dict__.copy() for task in task_list]

    def get_state(self):
        return self._state

class TaskBuilder:
    def __init__(self, description):
        self.task = Task(description)

    def set_due_date(self, due_date):
        self.task.due_date = due_date
        return self

    def set_tags(self, tags):
        self.task.tags = tags
        return self

    def build(self):
        return self.task

class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False
        self.creation_date = datetime.now()
        self.due_date = None
        self.tags = []

    def mark_completed(self):
        self.completed = True

    def mark_pending(self):
        self.completed = False

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        due_date_str = self.due_date.strftime("%Y-%m-%d") if self.due_date else ""
        return f"{self.description} - {status}, Due: {due_date_str}"

class ToDoListManager:
    def __init__(self):
        self.tasks = []
        self.mementos = []

    def add_task(self, task):
        self.tasks.append(task)
        self.save_state()
        self.display_tasks()

    def delete_task(self, task_description):
        task_found = False
        for i, task in enumerate(self.tasks):
            if task.description == task_description:
                self.tasks.pop(i)
                self.save_state()
                self.display_tasks()
                task_found = True
                print("Task deleted successfully!")
                break
        if not task_found:
            print(f"Task with description '{task_description}' not found.")


    def mark_completed(self, task_description):
        task_found = False
        for task in self.tasks:
            if task.description == task_description:
                task.mark_completed()
                self.save_state()
                self.display_tasks()
                task_found = True
                break
        if not task_found:
            print(f"Task with description '{task_description}' not found.")

    def view_tasks(self, filter_type=None):
        if filter_type == "completed":
            filtered_tasks = [task for task in self.tasks if task.completed]
        elif filter_type == "pending":
            filtered_tasks = [task for task in self.tasks if not task.completed]
        else:
            filtered_tasks = self.tasks

        return filtered_tasks

    def save_state(self):
        self.mementos.append(TaskMemento(self.tasks))

    def display_tasks(self):
        # Move this line to the beginning of the method
        tasks = self.view_tasks()

        print("\nAll tasks:")
        if not tasks:
            print("No tasks available.")
        else:
            self.display_table(tasks)

    @staticmethod
    def display_table(tasks):
        table = PrettyTable()
        table.field_names = ["Description", "Status", "Due Date","Tags"]

        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d") if task.due_date else ""
            tags_str = ", ".join(task.tags) if task.tags else ""
            table.add_row([task.description, status, due_date.strftime("%Y-%m-%d"), tags_str])


        print(table)


if __name__ == "__main__":
    todo_manager = ToDoListManager()
    welcome()

    while True:
        user_input = input("Enter your command: ").lower()

        if user_input == "tasks":
            if not todo_manager.tasks:
                print("No tasks available.")
            else:
                todo_manager.display_tasks()

        elif user_input == "add":
            description = input("Enter task description: ")
            due_date = input("Enter due date (optional, leave blank if not applicable): ")
            tags = input("Enter tags (optional, separate with commas if multiple): ").split(",")
            task = TaskBuilder(description).set_due_date(due_date.strip()).set_tags([tag.strip() for tag in tags]).build()
            todo_manager.add_task(task)
            print("Task added successfully!")
           

        elif user_input == "completed":
            todo_manager.display_tasks()
            description = input("Enter task description to mark as completed: ")
            todo_manager.mark_completed(description)
            print("Task marked as completed!")
            

        elif user_input == "delete":
            description = input("Enter task description to delete: ")
            todo_manager.delete_task(description)
            

        elif user_input == "exit":
            todo_manager.display_tasks()
            print("Exiting...")

            break

        else:
            print("Invalid command. Please enter a valid command from the options.")
