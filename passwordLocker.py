import sys, pyperclip, argparse, json, os, base64
from cryptography.fernet import Fernet



def isFileEmpty(file):
    with open(file, "r") as f:
        if f.read().strip() == "":  
            return True
    return False

def load_or_generate_key():
    keyFile = "fernetkey.key"
    if os.path.exists(keyFile):
        with open(keyFile, "r") as file:
            key = file.read()
    else:

        key = Fernet.generate_key()

        with open(keyFile, "wb") as file:
            file.write(key)
    return key
    


FERNET_KEY = load_or_generate_key()
fernet = Fernet(FERNET_KEY)

parser = argparse.ArgumentParser(description="Password saver")

parser.add_argument('--add', type=str)
parser.add_argument('--query', type=str)
parser.add_argument("--printAll", action='store_true')
parser.add_argument("--remove", type=str)

args = parser.parse_args()

PASSWORD_STORAGE_FILENAME = "passwords.json"
PASSWORD_FILE_PATH = f"./{PASSWORD_STORAGE_FILENAME}"

if args.add:
    print(f"Enter your password for {args.add}: ")
    account_password_input = input().strip()

    isFileExist = os.path.isfile(PASSWORD_FILE_PATH)
    encrypted_pass = fernet.encrypt(account_password_input.encode())

    # convert to a string because encrypted_pass is in bytes format
    encrypted_pass_str = encrypted_pass.decode()

    if isFileExist:
        if isFileEmpty(PASSWORD_STORAGE_FILENAME):   
            newData = {args.add: encrypted_pass_str}
            with open(PASSWORD_STORAGE_FILENAME, "w") as file:
                json.dump(newData, file, indent=4)
            print(f"{args.add} account and password is added!")
        else:
            with open(PASSWORD_STORAGE_FILENAME, "r") as jsonFile:
                data = json.load(jsonFile)

            data[args.add] = encrypted_pass_str

            with open(PASSWORD_STORAGE_FILENAME, "w") as jsonFile:
                json.dump(data, jsonFile, indent=4)

    else:
        with open(PASSWORD_STORAGE_FILENAME, "w") as file:  
            json.dump({}, file, indent=4)
        print(f"File {PASSWORD_STORAGE_FILENAME} created and {args.add} account added!")

elif args.remove:
    if isFileEmpty(PASSWORD_STORAGE_FILENAME):
        print("File is empty")
    else:
        with open(PASSWORD_STORAGE_FILENAME, "r") as jsonfile:
            data = json.load(jsonfile)

        if args.remove in data.keys():
            del data[args.remove]
            with open(PASSWORD_STORAGE_FILENAME, "w") as file:
                json.dump(data, file, indent=4)

            print(f"Account {args.remove} is removed from the list")
        else:
            print(f"Account {args.remove} is not found")

elif args.query:
    with open(PASSWORD_STORAGE_FILENAME, "r") as jsonfile:
        data = json.load(jsonfile)

    if args.query in data.keys():
        encrypted_pass_str = data[args.query]

        encrypted_pass = encrypted_pass_str.encode()
        decrypted_pass = fernet.decrypt(encrypted_pass).decode() 

        print(decrypted_pass)
    else:
        print(f"No password stored for account {args.query}")

elif args.printAll:
    if isFileEmpty(PASSWORD_STORAGE_FILENAME):
        print("No saved passwords")
    else:
        with open(PASSWORD_STORAGE_FILENAME, "r") as jsonfile:
            data = json.load(jsonfile)
        print(data)
