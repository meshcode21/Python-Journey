import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_task():
    clear_screen()
    title = input("Enter task title: ")
    tasks.append({"title": title, "done": False})
    print("Task added successfully!")

def view_tasks():
    clear_screen()
    if not tasks:
        print("No tasks available...😓")
        return
    
    for idx, task in enumerate(tasks, 1):
        status = "Done" if task["done"] else "Pending"
        print(f"{idx}. {task['title']} - {status}")

def mark_task():
    pass

def delete_task():
    pass

def menu():
    print("""
    1. Add Task
    2. View Tasks
    3. Mark Task as Done
    4. Delete Task
    5. Exit
    """)
    return input("Enter your choice: ")

tasks = [
    {"title": "Learn Python", "done": False},
    {"title": "Build ToDo App", "done": True},
]

while True:
    clear_screen()
    try:
        choice = int(menu())
    except ValueError:
        print("Please enter valid input...!!! ☹️")
        continue

    match choice:
        case 1:
            add_task()
        case 2:
            view_tasks()
        case 3:
            mark_task()
        case 4:
            delete_task()
        case 5:
            print("Good bye...!!!🤗")
            break
        case _:
            print("Invalid choice...!!! ☹️")
        
    input("\nPress Enter to continue...")