import sys  
import json
from datetime import datetime

file_name = "tasks.json"

def load_file():
    try:
        with open(file_name, "r") as file:
            return json.load(file)   
    except json.decoder.JSONDecodeError:
        return []
    except FileNotFoundError:
        return []
    
def upload_file(file_content):
    with open(file_name, "w") as file:
        json.dump(file_content, file, indent=2)

def invalid_op(command):
    print("Invalid command")

def add_task(command):
    if len(command) != 2:
        return print("\nInvalid command\n")
    
    file_content = load_file()
    new_id = int(file_content[-1]["id"])+ 1 if file_content else 1
    date = list(datetime.now().timetuple())

    file_content.append({
        "id": new_id,
        "description": command[1],
        "status": "todo",
        "createdAt": date,
        "updatedAt": date
    })
    print("\nSuccessfully added task with ID:", new_id, "\n")
    upload_file(file_content)

def delete_task(command):
    if len(command) != 2 or not command[1].isnumeric():
        return print("\nInvalid command\n")
    
    file_content = load_file()
    if not file_content:
        return print("\nList empty: no tasks to delete\n")
    
    for i in range(len(file_content)):
        if file_content[i]["id"] == int(command[1]):
            del file_content[i]
            upload_file(file_content)
            return print("\nSuccessfully deleted task with ID", command[1], "\n")
    print("\nUnsuccessful: ID not in list\n")
    
def update_task(command):
    if len(command) != 3 or not command[1].isnumeric():
        return print("\nInvalid command\n")
    
    file_content = load_file()
    if not file_content:
        return print("\nList empty: no tasks to update\n")
    for i in range(len(file_content)):
        if file_content[i]["id"] == int(command[1]):
            file_content[i]["description"] = command[2]
            date = list(datetime.now().timetuple())
            file_content[i]["updatedAt"] = date
            upload_file(file_content)
            return print("\nSuccessfully updated task with ID:", file_content[i]["id"], "\n")
    print("\nUnsuccessful: ID not in list\n")

def in_progress(command):
    if len(command) != 2 or not command[1].isnumeric():
        return print("Invalid command")
    
    file_content = load_file()
    if not file_content:
        return print("List empty: no tasks to update")
    for i in range(len(file_content)):
        if file_content[i]["id"] == int(command[1]):
            file_content[i]["status"] = "in-progress"
            date = list(datetime.now().timetuple())
            file_content[i]["updatedAt"] = date
            upload_file(file_content)
            return print("Successfully updated: in-progress")
    print("Unsuccessful: ID not in list")

def done(command):
    if len(command) != 2 or not command[1].isnumeric():
        return print("Invalid command")
    
    file_content = load_file()
    if not file_content:
        return print("List empty: no tasks to update")
    for i in range(len(file_content)):
        if file_content[i]["id"] == int(command[1]):
            file_content[i]["status"] = "done"
            date = list(datetime.now().timetuple())
            file_content[i]["updatedAt"] = date
            upload_file(file_content)
            return print("Successfully updated: done")
    print("Unsuccessful: ID not in list")

def print_tasks(command):
    if len(command) > 2:
        return print("Invalid command")
    
    file_content = load_file()
    if not file_content:
        return print("List empty: no tasks to list")
    
    if len(command) == 1:
        return print_all(file_content)
    print_type(command, file_content)
    
def print_all(file_content):
    list_str = ""
    for i in range(len(file_content)):
        for key, v in file_content[i].items():
            if key == "updatedAt" or key == "createdAt":
                v = [str(item) for item in v]
                v = v[0] + "-" + v[1] + "-" + v[2] + " " + v[3] + ":" + v[4] + ":" + v[5]
            list_str += key + ": " + str(v) + ", "
        list_str = list_str[:-2]
        list_str += "\n"
    print(list_str[:-2])

def print_type(command, file_content):
    status = command[1]
    if status != "done" and status != "in-progress" and status != "todo":
        return print("Invalid command")
    list_str = ""
    for i in range(len(file_content)):
        if file_content[i]["status"] == status:
            for key, v in file_content[i].items():
                if key == "updatedAt" or key == "createdAt":
                    v = [str(item) for item in v]
                    v = v[0] + "-" + v[1] + "-" + v[2] + " " + v[3] + ":" + v[4] + ":" + v[5]
                list_str += key + ": " + str(v) + ", "
            list_str = list_str[:-2]
            list_str += "\n"
    print(list_str[:-2])

function_list = {
    "add": add_task,
    "delete": delete_task,
    "update": update_task,
    "mark-in-progress": in_progress,
    "mark-done": done,
    "list": print_tasks
    }

def main():  
    if len(sys.argv) <= 1:
        return print("Invalid command")
    command = sys.argv[1:]
    op = function_list.get(command[0], invalid_op)
    op(command)

if __name__ == "__main__":
    main()