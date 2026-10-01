from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    if search_query:
        cursor.execute("SELECT * FROM students WHERE name LIKE ? OR course LIKE ?", 
                       (f'%{search_query}%', f'%{search_query}%'))
    else:
        cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students, search_query=search_query)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, email, course) VALUES (?, ?, ?)", (name, email, course))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    return {"status": "healthy", "database": "connected"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
