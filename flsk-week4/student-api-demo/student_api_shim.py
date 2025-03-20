import json
import requests

from config import CONFIG

# --- General function definitions ---
def add_student(first_name, last_name, email, phone):
    new_student = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone
    }
    response = requests.post( f"{CONFIG['api']['url']}/student", json=new_student )
    
    return int(response.text)

def list_of_students():
    results = requests.get( f"{CONFIG['api']['url']}/student")
    students = json.loads(results.text)

    return students

def get_student(student_id):
    result = requests.get( f"{CONFIG['api']['url']}/student/{student_id}")
    student = json.loads(result.text)

    return student

def update_student(student):
    response = requests.put( f"{CONFIG['api']['url']}/student/{student['student_id']}", json=student)
    student = json.loads(response.text)

    return int(student["student_id"])

def delete_student(student_id):
    requests.delete( f"{CONFIG['api']['url']}/student/{student_id}")


