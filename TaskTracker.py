import sys 

#initialize list of tasks
tasks: list = []
FILENAME = "tasks.txt"

## Functions--------------------------------------------------------------

def to_menu():
    
    print("""1. Add Task
2. View tasks
3. Remove task
4. Exit
5. Mark task as completed
6. Edit a task""")
    
def list_length(filename):
    tasks = load_tasks(filename)
    print(f"You have {len(tasks)} task(s) on your list.")
    

    
def load_tasks(filename):
    ##Read in tasks list from .txt file. 
    loaded_tasks = []
    try:
        with open(filename,'r') as file:
            # for task in tasks:
            #     file.read(f"{task["name"]}|{task["done"]}\n")
            
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
    return tasks
    
    
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




## Greeting message and option menu --------------------------------------

list_length(FILENAME)
tasks = load_tasks(FILENAME)
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
        tasks_dict = {
            "name": new_task,
            "done": False
        }
        tasks.append(tasks_dict)
        write_tasks(FILENAME, tasks)
        
        
    elif choice == 2:
        if not tasks:
            print("No tasks to display.")
        else:
            view_tasks(tasks)


    elif choice == 3:
        remove_task = input("Enter the task number you wish to remove: ")
        
        if not remove_task.isdigit():
            print("Please enter a valid number.")
            continue
        
        index = int(remove_task) - 1

        if 0 <= index < len(tasks):
            del tasks[index]
            write_tasks(FILENAME, tasks)
            
        else:
            print("Invalid task number.")
             
    elif choice == 4:
        print("Goodbye!")
        sys.exit()

    elif choice == 5:
        complete_task = input("Enter the task number you wish to complete: ")
        
        if not complete_task.isdigit():
            print("Please enter a valid number.")
            continue

        index = int(complete_task) - 1

        if 0 <= index < len(tasks):
            tasks[index]['done'] = True
            write_tasks(FILENAME, tasks)
            print("Task completed!")
    elif choice == 6:
        edit_task = input("Enter the task number you wish to edit: ")

        if not edit_task.isdigit():
            print("Please enter a valid number.")
            continue

        index = int(edit_task) - 1
        
        if 0 <= index < len(tasks):
            new_name = input("Enter new task name:")
            tasks[index]['name'] = new_name
            write_tasks(FILENAME, tasks)
            print("Task updated!")
        else:
            print("Invalid tasks number.")

    list_length(FILENAME)        
    to_menu()
        