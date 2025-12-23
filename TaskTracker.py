import sys 

#initialize list of tasks
tasks: list = []

## Functions--------------------------------------------------------------

def to_menu():
   
    print("""1. Add Task
2. View tasks
3. Remove task
4. Exit
5. Mark task as completed""")
    
def list_length(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            length = len(lines)
            print(f"You have {length} task(s) on your list.")
    except Exception as e:
        return f"An error has occured: {e}"

    
def load_tasks(filename):
    ##Read in tasks list from .txt file. 
    try:
        with open(filename,'r') as file:
            # for task in tasks:
            #     file.read(f"{task["name"]}|{task["done"]}\n")
            
            for line in file:
                name, done = line.strip().split("|")
                tasks.append({"name":name, "done":done == "True"})

    except FileNotFoundError:
        return f"Error: The file {filename} was not found."
    except Exception as e:
        return f"An error occured during loading: {e}"
    
def write_tasks(filename, tasks):
    try:
        with open(filename, 'w') as file:
            for task in tasks: 
                file.write(f"{task["name"]}|{task["done"]}\n")
    except Exception as e:
        return f"An error occured during writing: {e}"
    
# def completed_task(filename, tasks):
#     try:
#         with open(filename, 'w') as file:
#             lines = file.readlines()
#             for line in lines:
#                 if line 
#     except Exception as e:
#         return f"An error occured completing task: {e}"




## Greeting message and option menu --------------------------------------
# if list_length("tasks.txt") == 0:
#     print(f"Hello! You currently have 0 tasks.")
# else:
#     print(f"You have {list_length("tasks.txt")}")
list_length("tasks.txt")
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
        write_tasks("tasks.txt", tasks_dict)
        list_length("tasks.txt")
        to_menu()
        
    elif choice == 2:
        if not tasks:
            print("No tasks to display.")
        else:
            load_tasks("tasks.txt")
            
           
            # for index, item in enumerate(tasks, 1):
            #     if item['done'] == True:
            #         print(f"{index}. {item['name']} \u2705")
            #     else:
            #         print(f"{index}. {item['name']} \u274c")

    elif choice == 3:
        remove_task = input("Enter the task number you wish to remove: ")
        index = int(remove_task) - 1

        if 0 <= index < len(tasks):
            del tasks[index]
            write_tasks("tasks.txt", tasks)
            to_menu()
        else:
            print("Invalid task number.")
            to_menu() 
    elif choice == 4:
        print("Goodbye!")
        sys.exit()

    elif choice == 5:
        complete_task = input("Enter the task number you wish to complete: ")
        index = int(complete_task) - 1

        if 0 <= index < len(tasks):
            tasks[index]['done'] = True
            write_tasks("tasks.txt", tasks)
            print("Task completed!")
            to_menu()