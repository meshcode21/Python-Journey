import os
import json

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def update_file():
    # writing to file 
    try:
        with open("tasks.json",'w') as file:
            json.dump(tasks,file,indent=4)
    except Exception as error:
        print("error: ",error)


def add_task():
    title = input("\nEnter task title: ")
    if not title.strip():
        print("\nTask title cannot be empty! 😥")
        return
    tasks.append({"title": title, "done": False})
    update_file()
    print("Task added successfully!")

def view_tasks():
    print('')
    if not tasks:
        print("No tasks available...😓")
        return
    
    for idx, task in enumerate(tasks, 1):
        status = "Done" if task["done"] else "Pending"
        print(f"{idx}. {task['title']} - {status}")

def toggle_task():
    view_tasks()
    while True:
        try:
            choice = int(input("\nEnter choice to toggle:"))
            if choice > 0 and choice <= len(tasks):
                tasks[choice-1]["done"] = not tasks[choice-1]["done"]
                update_file()
                print("Updated successfully... 🥳")
                break
            else:
                print("Please choose within a range... ☹️")
        except ValueError:
            print("No changes made. Returning to menu 😊")
            break      

def delete_task():
    view_tasks()
    while True:
        try:
            choice = int(input("\nEnter choice to delete:"))
            
            if choice > 0 and choice <= len(tasks):
                if input("Are you sure (y/n)?:") == 'n':
                    return
                tasks.pop(choice-1)
                update_file()
                print("Deleted successfully... 🤗")
                break
            else:
                print("Please choose within a range... ☹️")
        except ValueError:
            print("No changes made. Returning to menu 😊")
            break  

def show_counts():
    done = pending = 0
    for task in tasks:
        if task['done']:
            done+=1
        else:
            pending+=1
    print(f"\n\nTotal: {len(tasks)} | Done: {done} | Pending: {pending}")

def menu():
    print("""
    1. Add Task
    2. View Tasks
    3. Toggle Task
    4. Delete Task
    5. Exit
    """)

# main global object to store actual data
tasks = []

try:
    with open('tasks.json') as file:
        data = file.read()
        tasks = json.loads(data)
  
except FileNotFoundError:
    with open('tasks.json','x') as file:
        file.write("[]")

while True:
    clear_screen()
    show_counts()
    menu()
    while True:
        try:
            choice = int(input("Enter your choice: "))
            break
        except ValueError:
            print("Please enter valid input...!!! ☹️\n")
            continue

    match choice:
        case 1:
            add_task()
        case 2:
            view_tasks()
        case 3:
            toggle_task()
        case 4:
            delete_task()
        case 5:
            print("Good bye...!!!🤗")
            break
        case _:
            print("Invalid choice...!!! ☹️")
        
    input("\nPress Enter to continue...")