import sqlite3

conn = sqlite3.connect("users.db")
sql_cursor = conn.cursor()             # This allows us to start executing sql commands

# Creates our table called employees with Columns for firstname, lastname, password, username, email and salary
sql_cursor.execute("""                 
                   CREATE TABLE employees(
                   first TEXT,
                   last TEXT,
                   full TEXT,
                   pass TEXT,
                   username TEXT,
                   email TEXT,
                   salary INTEGER,
                   admin BOOL,
                   salt TEXT);
                   """)
conn.commit()
conn.close()