import sqlite3

def studentData():
    con = sqlite3.connect("student-database.db")
    cur = con.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY, 
                StudentID INTEGER,
                FirstName TEXT,
                LastName TEXT,
                DateOfBirth DATE,
                Address TEXT, 
                PhoneNumber TEXT, 
                )""")
    con.commit()
    con.close()