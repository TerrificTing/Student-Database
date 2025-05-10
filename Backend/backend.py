from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__, template_folder = '../Frontend/templates', static_folder = '../Frontend/static')

def get_db():
    con = sqlite3.connect("student-database.db")
    con.row_factory = sqlite3.Row
    return con

def create_student_database():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS student(
                    StudentNumber INTEGER,
                    FirstName TEXT NOT NULL,
                    LastName TEXT NOT NULL,
                    EnrollmentDate DATE,
                    PRIMARY KEY (StudentNumber, EnrollmentDate));
                """)
    con.commit()
    con.close()

def create_daily__counter_database():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS daily_counter(
                    date DATE,
                    count INTEGER NOT NULL,
                    PRIMARY KEY (date, count));
                """)
    con.commit()
    con.close()

@app.before_request
def initialize():
    create_student_database()
    create_daily__counter_database()

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/add_student', methods = ['POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        current_date = datetime.now().strftime('%Y-%m-%d')

        con = get_db()
        cur = con.cursor()

        cur.execute('SELECT count FROM daily_counter WHERE date = ?', (current_date,))
        number_students = cur.fetchone()

        if number_students:
            new_count = number_students[0] + 1
            cur.execute('UPDATE daily_counter SET count = ? WHERE date = ?', (new_count, current_date))
        else:
            new_count = 1
            cur.execute('INSERT INTO daily_counter (date,count) VALUES (?, ?)', (current_date, new_count))
        number_students = new_count

        cur.execute("""
                    INSERT INTO student(StudentNumber, FirstName, LastName, EnrollmentDate)
                    VALUES (?, ?, ?, ?) """, 
                    (number_students, first_name, last_name, current_date))
        con.commit()
        con.close()

        return redirect(url_for('view_data'))

@app.route('/students')
def view_data():
    con = sqlite3.connect("student-database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    con.close()

    return render_template('students.html', students = rows)

if __name__ == '__main__':
    app.run(debug = True)