import hashlib
import sys
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os
from getpass import getpass
import time


vault: str = "Projects/Python/PasswordManager/vault.txt"
master: str = "Projects/Python/PasswordManager/master.txt"
salt_store: str = "Projects/Python/PasswordManager/salt.bin"

inactivity_timeout = 300 #seconds = 5mins



#Master Functions-----------------------------------------------

def check_master_password(filename: str) -> bool:
    return file_exists(filename)

def ensure_file_exists(filename: str) -> None:
    try: 
        with open (filename, "a") as f:
            pass
    except Exception as e:
        print(f"An error occured creating {filename}: {e}")


def create_master_password(filename: str) -> None:
    if check_master_password(filename):
        print("Master password already exists!")
        return None     ## Return none here if password exists to prevent if from executing.
    
    while True:
        password = getpass("Please enter a new master password: ")
        confirm = getpass("Please confirm the master password: ")

        #add loop to check for matching master passwords.
        if confirm != password:
            print("Passwords do not match.\n")
            continue          
        break

    hashed = hash_password(password)
    
    with open (filename, "w") as f:
        f.write(hashed + "\n")
        return None
    
def derive_key(master_password: str, salt: bytes) -> bytes:
    
    kdf = PBKDF2HMAC(   #Password-Based Key Derivation Function 2 with HMAC
        algorithm=hashes.SHA256(),
        length=32,#lenght in bytes or 32 * 8 = 256bits 
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    key = kdf.derive(master_password.encode('utf-8'))
    return base64.urlsafe_b64encode(key)

def get_salt(filename: str) -> bytes:
    try:
        with open(filename, "rb") as f:
            salt = f.read() ##Validate file is not empty FIRST.
            if salt:
                return salt ##If it's not, return the salt.
    except FileNotFoundError:
        pass
    salt = os.urandom(16)
    with open(filename, "wb") as f:
        f.write(salt)
        return salt


def verify_master_password(filename: str, password: str) -> bool:
    try:
        with open (filename, "r") as f:
            stored_hash = f.read().strip()
        password = hash_password(password)
        return  password == stored_hash
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
    
def add_password_entry(filename: str, fernet: Fernet) -> None:
   
 
    site = input("Please enter the site this password is used for: ")
    username = input("Please enter the associated username: ")
    password = getpass("Please enter your password:")
    confirm = getpass("Please confirm your password: ")

    if password != confirm:
        print("Passwords do not match")
        return

    encrypted_password = fernet.encrypt(password.encode())

    entry = f"{site}|{username}|{encrypted_password.decode()}\n"
    try:
        with open (filename, "a") as f:
            f.write(entry)
        print(f"Password entry for {site} has been added!")
    except Exception as e:
        print(f"An error has occured: {e}")

def view_vault(filename: str) -> None:
    try:
        entries = load_vault_entries(filename)

        if not entries:
            print("The Vault is empty")
            return
        for index, site, username, _ in entries:
            print(f"{index}. {site:<15} {username}")    
    except FileNotFoundError:
        print("Vault file not found.")
    except Exception as e:
        print(f"An error occured: {e}")

def load_vault_entries(filename:str) -> list[tuple]:  ## Helper function
    entries = []

    try:
        with open (filename, "r") as f:
            for index, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split("|") #split line into list, which should contain 3 values.
                if len(parts) != 3:
                    print(f"Skipping bad entry on line {index}")
                    continue
                site, username, encrypted_password = parts
                entries.append(( site, username, encrypted_password)) #append index from enumerate to entries list
    except FileNotFoundError:
        print("Vault file not found")
    except Exception:
        print("An error has occured")
    return entries


def retrieve_password(filename: str, fernet: Fernet) -> None:
    
  
    try:
        with open (filename, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                #open file, assign each line read to lines and strip the line.
                #reads each line --> strips whitespace --> if line has data, or discards empty lines
                #  --> in f.

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

        if not (1 <= get_passwd <= len(lines)):
            print("Out of range!")
            return None
        #validate input is in the valid range of indexes, and return None stops execution.

        site, username, encrypted_password_str = lines[get_passwd - 1].split("|")
        #format output and decrement input by 1 to match python indexing, IE selecting 1 actually is index 0
        # or the first item.
        password = fernet.decrypt(encrypted_password_str.encode()).decode()
        print(f"Password for {site} {username}: {password}")
        #print selected index site and password
    except FileNotFoundError:
        print("Vault file not found")
    except Exception as e:
        print(f"An error occured: {e}")


def search_password(filename: str, fernet: Fernet) -> None:

    try:
        with open (filename, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                #open file, assign each line read to lines and strip the line.
                #reads each line --> strips whitespace --> if line has data, or discards empty lines
                #  --> in f.

        if not lines:
            print("The vault is empty")

        search_passwd: str = input("Type the name of the site you'd like the password for: ")
        #take user input which is a string of the site.
        if not search_passwd.strip():
            print("Please enter a valid site name.")
            #validate we are getting a some kind of input. Leave as normal to be able include .com for example.
            return
        matches = [] ## initialize new list to catch matches from first search.

        for index, line in enumerate(lines, 1):
            site, username, encrypted_password_str = line.split("|")
            if search_passwd.lower() in site.lower(): #Normalize input and site from file.
                matches.append((index, site,username, encrypted_password_str)) ## add any matches to the new list.
        if not matches: 
            print("No Matches found")
            return
        for i, site, username, _ in matches: # For each match, print the index, site and username.
            print(f"{i}. {site} {username}")

        choice = input("Select the number of the password to retrieve: ")
        if not choice.isdigit():
            print("Invalid number")
            return
        choice = int(choice) ## continue with our normal index selection of the matching results.

        selected = next((m for m in matches if m[0]== choice), None)
        if not selected:
            print("Choice out of range")
            return
        _, site, username, encrypted_password_str = selected
        password = fernet.decrypt(encrypted_password_str.encode()).decode()
        print(f"Password for {site} {username}: {password}")

    except FileNotFoundError:
        print("Vault file not found")
    except Exception as e:
        print(f"An error occured: {e}")

def edit_entry(filename: str, fernet: Fernet) -> None:
      ## Encrypt, Salt, Key values
    
    try:
        with open (filename, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                #open file, assign each line read to lines and strip the line.
                #reads each line --> strips whitespace --> if line has data, or discards empty lines
                #  --> in f.

        if not lines:
            print("The vault is empty")

        search_passwd: str = input("Type the name of the site you'd like to update: ")
        #take user input which is a string of the site.
        if not search_passwd.strip():
            print("Please enter a valid site name.")
            #validate we are getting a some kind of input. Leave as normal to be able include .com for example.
            return
        matches = [] ## initialize new list to catch matches from first search.

        for index, line in enumerate(lines, 1):
            site, username, encrypted_password_str = line.split("|")
            if search_passwd.lower() in site.lower(): #Normalize input and site from file.
                matches.append((index, site,username, encrypted_password_str)) ## add any matches to the new list.
        if not matches: 
            print("No Matches found")
            return
        for i, site, username, _ in matches: # For each match, print the index, site and username.
            print(f"{i}. {site} {username}")

        choice = input("Select the number of the site you'd like to update: ")
        if not choice.isdigit():
            print("Invalid number")
            return
        choice = int(choice) ## continue with our normal index selection of the matching results.

        selected = next((m for m in matches if m[0]== choice), None)
        if not selected:
            print("Choice out of range")
            return
        new_username = input("Enter new username: ")

        index, site, _, encrypted_password_str = selected 
        ### _ represents a place holder for the oldusername variable,
        # it is written like this to show it's not needed, will be discarded for the new_username.
        lines_index = index - 1
        lines[lines_index] = f"{site}|{new_username}|{encrypted_password_str}" ## replaces line at line_index with fstring.

        with open(filename,"w") as f:
            for line in lines:
                f.write(line + "\n") ## Overwrites the file with new changes.

    except FileNotFoundError:
        print("Vault file not found")
    except Exception as e:
        print("An error occured: {e}")

def edit_username_by_index(filename: str) -> None: ##index and I/O practice function.
    try:
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            #Create memory object of each line of our vault file
        if not lines:
            print("The vault is empty!")
            return
            #If no data read, print empty.
        
        for index, line in enumerate(lines, 1):
            site, username, _ = line.split("|")
            print(f"{index}. {site} {username}")
            #enumerate our lines variable and print our list with possible options with the
            #above format for the user.
        choice = input("What index would you like to edit: ")
        if not choice.isdigit():
            print("Please enter a valid number")
            return
        #Get input, confirm isdigit()
        choice = int(choice) - 1 
        #convert to integer and list index for matching.
        if not (0 <= choice < len(lines)):
            print("Out of range!")
            return
        #confirm choice is within the range of our list of lines
        site, _ , encrypted_password_str = lines[choice].split("|")
        #assigned the selected list index the data associated with that lines index data
        new_username = input("Please enter a new username: ")
        lines[choice] = f"{site}|{new_username}|{encrypted_password_str}"
        #Assign new_username to input and update the associate line with the fstring format.


        with open (filename, "w") as f:
            for line in lines:
                f.write(line + "\n")
        print("Username updated successfully!")
                #Write each line to the vault file with the changes.
    except FileNotFoundError:
        print("Vault File not Found!")
    except Exception as e:
        print(f"An error occured: {e}")

def delete_entry_by_index(filename: str) -> None:
    
    index = select_entry(filename)
    if index is None:
        return  
   
    
    entries = load_vault_entries(filename)
    del entries[index]

    try:
        with open (filename, "w") as f:
            for site, username, encrypted_password in entries:
                f.write(f"{site}|{username}|{encrypted_password}\n")
        print("\nEntry deleted successfully!")
    except FileNotFoundError:
        print("Vault file not found!")
    except Exception as e:
        print(f"An error occured: {e}")

def check_inactivity(last_activity: float) -> None:
    if time.time() - last_activity > inactivity_timeout:
        print("\nSession timed out due to inactivity.")
        sys.exit()        

def select_entry(filename:str) -> None:
    entries = load_vault_entries(filename)
    if not entries: 
        print("The vault is empty.")
    for idx, entry in enumerate(entries, 1):
        site, username, _ = entry
        print(f"{idx}. {site} {username}")

    choice = input("What entry index would you like to edit: ")
    if not choice.isdigit():
        print("Please enter a valid number")
        return
    choice = int(choice) - 1 ## CONVERT TO LIST INDEX from DISPLAY INDEX
    if not (0 <= choice < len(entries)):
        print("Out of range!")
        return
    return choice

###Indexing rules----------------------------------------------
# display_index = list_index + 1
# list_index = display_index - 1




#Menu----------------------------------------------------------
def show_menu():
    print(f"""
{ADD}. Add password
{VIEW}. View vault
{RETRIEVE}. Retrieve password
{EXIT}. Exit
{SEARCH}. Search password by site name
{EDIT}. Edit existing entry
{EDIT_I}. Edit by username by index
{DEL_I}. Delete entry by index""")

ADD = 1
VIEW = 2
RETRIEVE = 3
EXIT = 4
SEARCH = 5
EDIT = 6
EDIT_I = 7
DEL_I = 8

#Initialize Master and Vault files-------------------------------------------------
ensure_file_exists(vault)
ensure_file_exists(master)
ensure_file_exists(salt_store)
#Authentication-------------------------------------------------------------
if not check_master_password(master):
    create_master_password(master)
password = getpass("Please enter the master password: ")
if not verify_master_password(master, password):
    print("Access is denied!")
    sys.exit()

#Encrypt & Decrypt-------------------------------------------------------------
## Derive Key

salt = get_salt(salt_store)
key = derive_key(password, salt)
fernet = Fernet(key)



#Inactivity Timeout--------------------------------------------
last_activity = time.time()

#Logic loop----------------------------------------------------

while True: 
    check_inactivity(last_activity)
    show_menu()
    choice = input("Please select the action number you'd like to perform: ")
    check_inactivity(last_activity)
    last_activity = time.time()

    if not choice.isdigit():
        print("Please enter a valid number!")
        continue  ## validates that input is indeed a number, and continues to the next loop flow preventing crashing.
    choice = int(choice)
    if choice == ADD:
        add_password_entry(vault, fernet)
    elif choice == VIEW:
        view_vault(vault)
    elif choice == RETRIEVE:
        retrieve_password(vault, fernet)
    elif choice == EXIT:
        print("Goodbye!")
        sys.exit()
    elif choice == SEARCH:
        search_password(vault, fernet)
    elif choice == EDIT:
        edit_entry(vault, fernet)
    elif choice == EDIT_I:
        edit_username_by_index(vault)
    elif choice == DEL_I:
        delete_entry_by_index(vault)
    last_activity = time.time()
