from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("students/main.html")

@app.route("/students")
def students():
    return render_template("students/student_data_table.html")

@app.route("/new-student", endpoint="new_student")
def new_student():
    return render_template("students/new_student.html")

@app.route("/edit-student")
def edit_student():
    return render_template("students/edit_student.html")



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
