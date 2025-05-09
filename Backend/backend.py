from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder = '../Frontend/templates', static_folder = '../Frontend/static')

def get_db():
    con = sqlite3.connect("student-database.db")
    con.row_factory = sqlite3.Row
    return con

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/add_student', methods = ['POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form['StudentID']
        first_name = request.form['FirstName']
        last_name = request.form['LastName']
        dob = request.form['DateOfBirth']
        address = request.form['Address']
        phone_number = request.form['PhoneNumber']

        con = get_db()
        cur = con.cursor()
        cur.execute("""
                    INSERT INTO student(StudentID, FirstName, LastName, DateOfBirth, Address, PhoneNumber)
                    VALUES (?, ?, ?, ?, ?, ?) """, 
                    (student_id, first_name, last_name, dob, address, phone_number))
        con.commit()
        con.close()

        return 'Student added successfully'
    
if __name__ == '__main__':
    app.run(debug = True)