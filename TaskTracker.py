import sys 



FILENAME = "tasks.txt"

## Functions--------------------------------------------------------------

def to_menu():
    
    print("""1. Add Task
2. View tasks
3. Remove task
4. Exit
5. Mark task as completed
6. Edit a task
7. View completed tasks
8. View incomplete tasks""")

def list_length(tasks):
    
   
    print(f"You have {len(tasks)} task(s) on your list.")
    

    
def load_tasks(filename):
    ##Read in tasks list from .txt file. 
    loaded_tasks = []
    try:
        with open(filename,'r') as file:
        
            for line in file:
                line = line.strip()
                if not line:
                    continue

                name, done = line.strip().split("|")
                loaded_tasks.append({"name":name, "done":done == "True"})           

    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"An error occured during loading: {e}")
        return []
    return loaded_tasks
    
    
def write_tasks(filename, tasks):
    try:
        with open(filename, 'w') as file:
            for task in tasks: 
                file.write(f"{task['name']}|{task['done']}\n")
    except Exception as e:
        print(f"An error occured during writing: {e}")

def view_tasks(tasks):
    if not tasks:
        print("No tasks to display.")
    else:
        for index, item in enumerate(tasks, 1):
            if item['done'] == True:
                print(f"{index}. {item['name']} \u2705")
            else:
                print(f"{index}. {item['name']} \u274c")

def valid_number_index(prompt, tasks):
    choice = input(prompt)
    if not choice.isdigit():
        print("Please enter a valid number.")
        return None
    index = int(choice) - 1
    if not (0 <= index < len(tasks)):
        print("Invalid task number.")
        return None
    return index



## Greeting message and option menu --------------------------------------
tasks: list = load_tasks(FILENAME)
list_length(tasks)
print("What would you like to do? ")
to_menu()



## User choice prompt and logic loop.------------------------------------------
while True:
    
    choice:str = input("Please select the number of the action you'd like to perform: ")

    if not choice.isdigit():
        print("Please enter a valid number.")
        continue
    choice = int(choice)
    
    if choice == 1:
        new_task = input("Enter task: ")
        task = {
            "name": new_task,
            "done": False
        }
        tasks.append(task)
        write_tasks(FILENAME, tasks)
        
        
    elif choice == 2:
        if not tasks:
            print("No tasks to display.")
        else:
            view_tasks(tasks)


    elif choice == 3:
        
        index = valid_number_index("Enter the task number you wish to remove: ", tasks)
        if index is None:
            continue

        if 0 <= index < len(tasks):
            del tasks[index]
            write_tasks(FILENAME, tasks)
            
        else:
            print("Invalid task number.")
             
    elif choice == 4:
        print("Goodbye!")
        sys.exit()

    elif choice == 5:

        index = valid_number_index("Enter the task number you wish to mark complete: ", tasks)
        if index is None:
            continue

        
        tasks[index]['done'] = True
        write_tasks(FILENAME, tasks)
        print("Task completed!")
    elif choice == 6:
        
        index = valid_number_index("Enter the task number you wish to edit: ", tasks)
        
        new_name = input("Enter new task name:")
        tasks[index]['name'] = new_name
        write_tasks(FILENAME, tasks)
        print("Task updated!")
        
    elif choice == 7:
        completed_tasks = [task for task in tasks if task['done']]
        view_tasks(completed_tasks)
    elif choice == 8:
        incomplete_tasks = [task for task in tasks if not task['done']]
        view_tasks(incomplete_tasks)


    list_length(tasks)        
    to_menu()
        