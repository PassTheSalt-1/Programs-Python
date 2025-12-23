import sys 

#initialize list of tasks
tasks: list = []

def to_menu():
    print(f"You have {len(tasks)} task(s).")
    print("""1. Add Task
2. View tasks
3. Remove task
4. Exit
5. Mark task as completed""")


## Greeting message and option menu
if len(tasks) == 0:
    print(f"Hello! You currently have {len(tasks)} tasks.")
print("What would you like to do? ")
to_menu()



## User choice prompt and logic.   
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
        to_menu()
        
    elif choice == 2:
        if not tasks:
            print("No tasks to display.")
        else:
            for index, item in enumerate(tasks, 1):
                if item['done'] == True:
                    print(f"{index}. {item['name']} \u2705")
                else:
                    print(f"{index}. {item['name']} \u274c")

    elif choice == 3:
        remove_task = input("Enter the task number you wish to remove: ")
        index = int(remove_task) - 1

        if 0 <= index < len(tasks):
            del tasks[index]
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
            print("Task completed!")
            to_menu() 