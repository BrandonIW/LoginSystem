import sqlite3
import bcrypt
from time import sleep
from user_create import User, Admin
from getpass import getpass
from itertools import count

# Prompt: Who do you want to login as? - Supply Username and Password                                              -Done
# Check the DB for associates username and password, also check if that user is an admin
# If a match, then we login as that user and supply a little text saying "logged in as {user}"
# If no match. Counter to track failed attempts. At 5 attempts or w/e we lock out                                  -Done

# If we login as admin, we have access to change other's password and information
# If we do not login as admin, that ability is restricted



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
            login(user)

        print("Password incorrect. Try again: ")

    #Lockout
    print("Nah man, you're gettin' locked for 5 min sry lol")
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
    pass


if __name__ == '__main__':
    main()




