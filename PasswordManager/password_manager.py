import hashlib
import sys


vault = "vault.txt"



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
    




    
#--------------------------------------------------------------
if not verify_master_password(vault):
    print("Access is denied!")
    sys.exit()

file_exists(vault)
print(hash_password("Test 123"))
print(hash_password("Test 123"))
