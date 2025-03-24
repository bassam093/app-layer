"""Example student management app."""

from flask import Flask, render_template, request, make_response, redirect, jsonify, url_for

from config import CONFIG
from student_api_shim import add_student, list_of_students, get_student, update_student, delete_student

# --- Flask stuff below ---
app = Flask(__name__)

# Standard route, nothing special happening.
@app.route("/")
def homepage():
    return render_template("students/main.html", students=list_of_students())

# A method that accepts both GET and POST methods, but no dynamic parameters in URL.
@app.route("/new/", methods=["GET", "POST"])
def newstudent():
    if request.method == "GET":
        return render_template("students/new_student.html")
    elif request.method == "POST":
        student = {}
        student["first_name"] = request.form["first_name"]
        student["last_name"] = request.form["last_name"]
        student["email"] = request.form["email"]
        student["phone"] = request.form["phone"]
        student["student_id"] = add_student(student["first_name"], student["last_name"], student["email"], student["phone"])
        return render_template("students/new_student.html", student_added=student)

    return make_response("Invalid request", 400)

@app.route("/deletestudent/<int:student_id>")
def deletestudent(student_id):
    delete_student(student_id)

    return redirect("/")

@app.route("/editstudent/<int:student_id>", methods=["GET", "POST"])
def editstudent(student_id):
    if request.method == "GET":
        student = get_student(student_id)
        return render_template("students/edit_student.html", student=student)
    elif request.method == "POST":
        student = {
            "student_id": student_id,
            "first_name": request.form["first_name"],
            "last_name":  request.form["last_name"],
            "phone":      request.form["phone"],
            "email":      request.form["email"]
        }
        update_student(student)
        return render_template("students/edit_student.html", student=student, student_updated=student)
    
    return make_response("Inalid request", 400)

if __name__ == "__main__":
    app.run(host=CONFIG["frontend"]["listen_ip"], port=CONFIG["frontend"]["port"], debug=CONFIG["frontend"]["debug"])
