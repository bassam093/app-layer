import sqlite3

DATABASE_PATH = '/app/db/students.db'

# Connect to the SQLite database
with sqlite3.connect(DATABASE_PATH) as connection:
    # Perform database operations here
    cursor = connection.cursor()
    # Example query
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        print(row)



from flask import jsonify

from config import CONFIG

def dict_factory(cursor, row):
    fields = [ column[0] for column in cursor.description ]
    return {key: value for key, value in zip(fields, row)}

def get_db_connection():
    db_conn = sqlite3.connect(CONFIG["database"]["name"])
    db_conn.row_factory = dict_factory
    return db_conn

def read_all():
    ALL_STUDENTS = "SELECT * FROM student"
    
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(ALL_STUDENTS)
    resultset = cursor.fetchall()
    db_conn.close()

    return jsonify(resultset)

def create(student):
    INSERT_STUDENT = "INSERT INTO student (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)"
    
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(INSERT_STUDENT, (student["first_name"], student["last_name"], student["email"], student["phone"]))
    db_conn.commit()
    new_student_id = cursor.lastrowid
    db_conn.close()
    
    return new_student_id, 201

def read_one(student_id):
    GET_STUDENT = "SELECT * FROM student WHERE student_id = ?"

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(GET_STUDENT, (student_id, ) )
    resultset = cursor.fetchall()
    db_conn.close()

    if len(resultset) < 1:
        return "Not found", 404
    elif len(resultset) > 2:
        return "Too many results found.", 500

    return jsonify(resultset[0])

def update(student_id, student):
    UPDATE_STUDENT = """
    UPDATE student
    SET first_name = ?,
        last_name = ?,
        email = ?,
        phone = ?
    WHERE student_id = ?
    """

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(UPDATE_STUDENT, (student["first_name"], student["last_name"], student["email"], student["phone"], student_id) )
    db_conn.commit()

    return read_one(student_id)

def delete(student_id):
    DELETE_STUDENT = "DELETE FROM student WHERE student_id=?"

    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    cursor.execute(DELETE_STUDENT, (student_id, ) )
    db_conn.commit()

    return "Succesfully deleted.", 204
