import csv
import hashlib
import os
import getpass

USERS_FILE = "users.csv"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(username):
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                return True
    return False

def register():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "password"])
            writer.writeheader()

    while True:
        username = input("New username: ").strip()
        if user_exists(username):
            print("Username already exists. Try a different one.")
        elif not username:
            print("Username cannot be empty.")
        else:
            break
    while True:
        password = getpass.getpass("New password: ")
        if not password:
            print("Password cannot be empty.")
        else:
            break
    hashed_pw = hash_password(password)
    with open(USERS_FILE, 'a', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "password"])
        writer.writerow({"username": username, "password": hashed_pw})
    print("Registration successful! Please login to continue.")

def authenticate():
    if not os.path.exists(USERS_FILE):
        print("No users registered yet. Please register first.")
        return None
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    hashed_pw = hash_password(password)
    with open(USERS_FILE, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username and row['password'] == hashed_pw:
                print(f"Welcome, {username}!")
                return username
    print("Login failed. Invalid username or password.")
    return None

def get_tasks_file(username):
    return f"tasks_{username}.csv"

def load_tasks(username):
    tasks = []
    filename = get_tasks_file(username)
    if os.path.exists(filename):
        with open(filename, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['id'] = int(row['id'])
                tasks.append(row)
    return tasks

def save_tasks(username, tasks):
    filename = get_tasks_file(username)
    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['id', 'description', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for t in tasks:
            writer.writerow(t)
    print("Tasks saved.")

def add_task(username, tasks):
    description = input("Task description: ").strip()
    if not description:
        print("Task description cannot be empty.")
        return
    next_id = (max((t['id'] for t in tasks), default=0) + 1) if tasks else 1
    tasks.append({'id': next_id, 'description': description, 'status': "Pending"})
    print(f"Task added with ID {next_id}.")

def view_tasks(tasks):
    if not tasks:
        print("No tasks.")
        return
    print("\nYour Tasks:")
    for t in tasks:
        print(f"ID: {t['id']} | {t['description']} | Status: {t['status']}")

def mark_task_completed(tasks):
    task_id = input("Enter Task ID to mark as completed: ")
    try:
        tid = int(task_id)
        for t in tasks:
            if t['id'] == tid:
                if t['status'] == "Completed":
                    print("Task is already completed.")
                else:
                    t['status'] = "Completed"
                    print("Task marked as completed.")
                return
        print("Task not found.")
    except ValueError:
        print("Invalid Task ID.")

def delete_task(tasks):
    task_id = input("Enter Task ID to delete: ")
    try:
        tid = int(task_id)
        for t in tasks:
            if t['id'] == tid:
                tasks.remove(t)
                print("Task deleted.")
                return
        print("Task not found.")
    except ValueError:
        print("Invalid Task ID.")

def task_menu(username):
    tasks = load_tasks(username)
    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Logout")
        choice = input("Choose option: ").strip()
        if choice == "1":
            add_task(username, tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            mark_task_completed(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            save_tasks(username, tasks)
            print("Logged out!")
            break
        else:
            print("Invalid choice.")

def main():
    print("Welcome to the Task Manager")
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose option: ").strip()
        if choice == "1":
            register()
        elif choice == "2":
            username = authenticate()
            if username:
                task_menu(username)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()