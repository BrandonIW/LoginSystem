import sqlite3
import bcrypt
from time import sleep
from user_create import User, Admin
from getpass import getpass
from itertools import count
import logging


# Prompt: Who do you want to login as? - Supply Username and Password                                             - Done
# If a match, then we login as that user and supply a little text saying "logged in as {user}"                    - Done
# If no match. Counter to track failed attempts. At 5 attempts or w/e we lock out                                 - Done


####### Logging Setup ########
logger = logging.getLogger(__name__)                             # This creates a logger with the name of the module
file_handler_for_debug = logging.FileHandler('logdebug.txt')     # We make a new handler that points to a file
file_handler_for_warning = logging.FileHandler('logwarning.txt') # We made a new handler for warnings
logger.addHandler(file_handler_for_debug)                        # Add that handler to our logger
logger.addHandler(file_handler_for_warning)

#### Formatting our file Handler and setting log levels ####
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s:%(name)s')
file_handler_for_debug.setFormatter(formatter)
file_handler_for_warning.setFormatter(formatter)
file_handler_for_warning.setLevel(logging.WARNING)
file_handler_for_debug.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)


conn = sqlite3.connect("users.db")
sql_cursor = conn.cursor()

def main():
    failed_logins = count(0)

    # Get connected to DB and pull list of usernames
    user_list = pull_username_list()

    # Select user
    user = input("Please enter your username (case sensitive): ")

    # Select User loop
    while user not in user_list:
        print("Username does not exist. Try again\n")
        user = input("Please enter your username (case sensitive): ")

    # If user exists, check password logic
    while next(failed_logins) < 5:
        pwd = bytes(getpass("Please enter your password: "), encoding="utf-8")
        if check_password(user,pwd):
            print("Correct password")

            logger.debug(f"User {user} successfully logged in")
            login(user)

        print("Password incorrect. Try again: ")
        logger.warning(f"User {user} inputted wrong password")

    #Lockout
    print("Nah man, you're gettin' locked for 5 min sry lol")
    logger.warning(f"User {user} has been locked out after 5 failed login attempts")
    sleep(300)

def pull_username_list():
    with conn:
        sql_cursor.execute("SELECT username FROM employees")
        return [name[0] for name in sql_cursor.fetchall()]

def check_password(user,pwd):
    with conn:
        sql_cursor.execute("SELECT pass FROM employees WHERE username = ?", (user,))
        stored_hash = sql_cursor.fetchone()[0]

    print("Checking hash...")

    if bcrypt.checkpw(pwd,stored_hash):
        return True
    return False

def login(user):
    print(f"You are logged in as: {user}")
    exit()

if __name__ == '__main__':
    main()




