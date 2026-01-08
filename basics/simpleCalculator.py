import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def add(a, b):
    res = a + b
    history.append(f"{a} + {b} = {res}")
    return res

def subtract(a, b):
    res = a - b
    history.append(f"{a} - {b} = {res}")
    return res

def multiply(a, b):
    res = a * b
    history.append(f"{a} * {b} = {res}")
    return res

def divide(a, b):
    if b == 0:
        return None
    res = a / b
    history.append(f"{a} / {b} = {res}")
    return res

history = []


def show_menu():
    print("--- Simple Calculator ---")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. History")
    print("6. Exit")

while True:
    input("Enter any key to continue...")
    clear_screen()
    show_menu()
    choice = input("\nChoose an option (1-6): ")

    if choice == "5":
        if not history:
            print("No calculations yet.")
        else:
            print("All Calculations:")
            for res in history:
                print(res)
        continue

    if choice == "6":
        print("👋 Exiting calculator...")
        break

    try:
        if (choice > "6"): 
            raise ValueError
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
    except ValueError:
        print("❌ Please enter valid numbers")
        continue

    if choice == "1":
        print("Result:", add(a, b))
    elif choice == "2":
        print("Result:", subtract(a, b))
    elif choice == "3":
        print("Result:", multiply(a, b))
    elif choice == "4":
        result = divide(a, b)
        if result is None:
            print("❌ Cannot divide by zero")
        else:
            print("Result:", result)
    else:
        print("❌ Invalid choice")