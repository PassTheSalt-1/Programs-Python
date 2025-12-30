import hashlib
import sys


vault: str = "vault.txt"



#Master Functions-----------------------------------------------

def check_master_password(filename: str) -> bool:
    return file_exists(filename)

def create_master_password(filename: str) -> None:
    if check_master_password(filename):
        print("Master password already exits.")
    
    password = input("Please enter a new master password: ")
    hashed = hash_password(password)
    
    with open (filename, "w") as f:
        f.write(hashed + "\n")
        return None

def verify_master_password(filename: str) -> bool:

    try:
        with open (filename, "r") as f:
            stored_hash = f.read().strip()
        password = input("Please enter the master password:")
        hashed = hash_password(password)
        return hashed == stored_hash
    except FileNotFoundError:
        return False

def hash_password(password: str) -> str:
    #Takes user password input from user and hashes password#
    password_bytes = password.encode('utf-8')
    hashed_object = hashlib.sha256(password_bytes)
    password_hash = hashed_object.hexdigest()
    return password_hash

def file_exists(filename: str) -> bool:
    try:
        with open (filename, "r") as f:
            return bool(f.read().strip())
    except FileNotFoundError:
       return False
    
#User Input Functions------------------------------------------
    
def add_password_entry(filename: str) -> None:
    site = input("Please enter the site this password is used for: ")
    username = input("Please enter the associated username: ")
    password = input("Please enter your password:")
   

    entry = f"{site}|{username}|{password}\n"
    try:
        with open (filename, "a") as f:
            f.write(entry)
        print(f"Password entry for {site} has been added!")
    except Exception as e:
        print(f"An error has occured: {e}")

def view_vault(filename: str) -> None:
    try:
        with open (filename, "r") as f:   ### Open file in read mode
            lines = f.readlines()       ## assign variable to our lines read for indexing

        if not lines:
            print("The vault is empty")  ## if file is empty, print error

        for index, line in enumerate(lines, 1):### enumerate the file if data is found.
            line = line.strip()
            if not line:                
                continue                ### skip if line is empty, in this case the password.
            site, username, _ = line.split("|") ## format output with | separator.
            print(f"{index}. {site:<15} {username}")    
    except FileNotFoundError:
        print("Vault file not found.")
    except Exception as e:
        print("An error occured: {e}")

def retrieve_password(filename: str) -> None:

    try:
        with open (filename, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                #open file, assign each line read to lines and strip the line.

        if not lines:
            print("The vault is empty")

        get_passwd: str = input("Select the password index you'd like to retrieve: ")
        #take user input which is a string at first.
        if not get_passwd.isdigit():
            print("Please enter a valid number.")
            #validate we are getting a number through the input.
            return
        get_passwd = int(get_passwd)
        #convert string number into an integer. 

        if not (1 <= get_passwd < len(lines)):
            print("Out of range!")
        #validate input is in the valid range of indexes

        site, _, password = lines[get_passwd - 1].split("|")
        #format output and decrement input by 1 to match python indexing.

        print(f"Password for {site}: {password}")
        #print selected index.
      

    except FileNotFoundError:
        print("Vault file not found")
    except Exception as e:
        print("An error occured: {e}")
#Main----------------------------------------------------------
create_master_password(vault)

view_vault(vault)

#--------------------------------------------------------------
if not verify_master_password(vault):
    print("Access is denied!")
    sys.exit()


