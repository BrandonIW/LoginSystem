'''
The idea here is make a login system that just prints everything to console.

What I want to be able to do:
1) Create a database that stores username/password combinations                                                   - Done
2) Passwords must be hashed                                                                                       - Done
8) Monitor failed password attempts and lock out the user?                                                        - Done
9) Input validation when creating a password (password complexity for Nums, Letters, length, symbols etc)         - Done
11) Logging system to log failed logins and successful logins                                                     - Done
12) Create setters/getters to change user information                                                             - Done
'''

# TODO: Stop duplication of users being made in the DB,

import sqlite3
import re
from getpass import getpass
import bcrypt
from functools import wraps

class User:

########################################### Initialization ###############################################

# Password complexity regex. Password must have 1 uppercase, 2 numbers, 2 non-words
    regex = re.compile(r'^(?=.*[A-Z])(?=.*[0-9]{2,})(?=.*\W{2,})')


    def __init__(self,first_name,last_name,salary):
        self.first_name = first_name
        self.last_name = last_name

# Attributes that are related to properties. Underscore to avoid recursion
        self._salary = salary
        self._email = f"{self.first_name[0].upper()}.{self.last_name.title()}@gmail.com"
        self._full_name = f"{self.first_name} {self.last_name}"
        self._username = f"{self.first_name[0]}{self.last_name}"

# Complexity Check
        self._complexity = False
        self._salt = bcrypt.gensalt(16)
        while not self._complexity:
            print("Password must be at least 7 characters. 1x Uppercase. 2x Numbers. 2x Symbols")
            self._password = getpass("Please input a password for this user: ")
            self._password = self._hash_and_salt(self._password)

# Add the new employee
        self._new_employee_sql()


# Should be readable
    def __str__(self):
        return f"User's name: {self.first_name} {self.last_name}\nUser's email: {self.email}\nUser's salary: {self.salary}"


# Should be unambiguous. Python code that can be sent to eval()
    def __repr__(self):
        return {"first_name":self.first_name,"last_name":self.last_name,"email":self.email,"salary":self.salary}



########################################### Password Checking ############################################

# Decorator to confirm password complexity
    def _complexity_check(func):
        """ Password complexity checker """
        @wraps(func)
        def decorator(self, *args,**kwargs):
            if User.regex.findall(self._password) and len(self._password) >= 7:
                self._complexity = True
                return func(self, *args,**kwargs)
            self._complexity = False
        return decorator


#Hashes & salts password:
    @_complexity_check
    def _hash_and_salt(self, value):
        """ Hash a password for storage. Need a static salt else it will never match"""
        return bcrypt.hashpw(value.encode('utf-8'), self._salt)


########################################### Employee Addition ############################################
    def _new_employee_sql(self):
        """ Adds a new employee to our SQLLite DB """

        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()

        # Use context manager
        with conn:
            sql_cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (self.first_name, self.last_name, self._full_name, self._password,
                            self._username, self._email, self._salary, "FALSE", self._salt))


########################################### Define Setters/Getters ############################################

    @property
    def full_name(self):
        '''Fetch full name of user'''
        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()
        with conn:
            sql_cursor.execute("SELECT full FROM employees WHERE username=?",(self._username,))
            return sql_cursor.fetchone()[0]

    @full_name.setter
    def full_name(self,fullname):
        '''Set first, last and fullname of user'''
        self.first_name = fullname.split(" ")[0]
        self.last_name = fullname.split(" ")[1]
        self._full_name = f"{self.first_name} {self.last_name}"
        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()
        with conn:
            sql_cursor.execute("UPDATE employees SET first = ?, last = ?, full = ? WHERE username = ?",
                               (self.first_name, self.last_name, self._full_name, self._username))



    @property
    def user_name(self):
        '''Fetch username of user'''
        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()
        with conn:
            sql_cursor.execute("SELECT username FROM employees WHERE username=?",(self._username,))
            return sql_cursor.fetchone()[0]

    @user_name.setter
    def user_name(self, username):
        ''' Edit Username '''
        self._username = username
        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()
        with conn:
            sql_cursor.execute("UPDATE employees SET username = ? WHERE full = ?",
                       (self._username, self._full_name))



    @property
    def email(self):
        '''Fetch email of user'''
        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()
        with conn:
            sql_cursor.execute("SELECT email FROM employees WHERE username=?",(self._username,))
            return sql_cursor.fetchone()[0]

    @email.setter
    def email(self, new_email):
        ''' Edit email '''
        self._email = new_email
        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()
        with conn:
            sql_cursor.execute("UPDATE employees SET email = ? WHERE username = ?",
                           (self._email, self._username))



    @property
    def salary(self):
        ''' Fetch Salary '''
        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()
        with conn:
            sql_cursor.execute("SELECT salary FROM employees WHERE username=?",(self._username,))
            return sql_cursor.fetchone()[0]

    @salary.setter
    def salary(self, value):
        ''' Edit Salary '''
        self._salary = value
        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()
        with conn:
            sql_cursor.execute("UPDATE employees SET salary = ? WHERE username = ?",
                               (self._salary, self._username))


    @property
    def is_admin(self):
        ''' Check if user is admin '''
        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()
        with conn:
            sql_cursor.execute("SELECT admin FROM employees WHERE username = ?", (self._username,))
            return sql_cursor.fetchone()[0]




class Admin(User):
    def __init__(self,first_name,last_name,salary):
        super().__init__(first_name,last_name,salary) # This is basically saying "Run the __init__ of whoever is next in MRO.
                                                      # The init will run _new_employee_sql(self) in the admin class first due to MRO

    def _new_employee_sql(self):
        """ Adds a new employee to our SQLLite DB """
        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()

        # Use context manager
        with conn:
            sql_cursor.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (self.first_name, self.last_name, self._full_name, self._password,
                            self._username, self._email, self._salary, "TRUE", self._salt))

    @property
    def is_admin(self):
        ''' Check if user is admin '''
        conn = sqlite3.connect("users.db")
        sql_cursor = conn.cursor()
        with conn:
            sql_cursor.execute("SELECT admin FROM employees WHERE username = ?", (self._username,))
            return sql_cursor.fetchone()[0]

#User1 = User("Brandon", "Wittet", 5000)
#User2 = User("Mary", "Jane", 6840)
#User3 = User("Joe", "Blow", 2345)
#Admin1 = Admin("Dick", "Butt", 5000)


