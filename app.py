from flask import Flask, render_template, request, redirect, flash
import sqlite3


app = Flask(__name__)

app.secret_key = "student_system_secret"



def connect_db():
    return sqlite3.connect("students.db")



@app.route("/")
def home():

    search = request.args.get("search")


    connection = connect_db()
    cursor = connection.cursor()


    if search:

        cursor.execute(
            """
            SELECT * FROM students
            WHERE name LIKE ?
            OR student_id LIKE ?
            OR course LIKE ?
            """,
            (
                "%" + search + "%",
                "%" + search + "%",
                "%" + search + "%"
            )
        )

    else:

        cursor.execute("SELECT * FROM students")


    students = cursor.fetchall()


    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]


    cursor.execute("SELECT COUNT(DISTINCT course) FROM students")
    total_courses = cursor.fetchone()[0]


    cursor.execute(
        "SELECT * FROM students ORDER BY id DESC LIMIT 1"
    )

    latest_student = cursor.fetchone()


    connection.close()


    return render_template(
        "index.html",
        students=students,
        total_students=total_students,
        total_courses=total_courses,
        latest_student=latest_student
    )



@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"]
    student_id = request.form["student_id"]
    course = request.form["course"]


    if name == "" or student_id == "" or course == "":
        flash("Please complete all student information!")
        return redirect("/")


    connection = connect_db()
    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO students
        (name, student_id, course)
        VALUES (?, ?, ?)
        """,
        (name, student_id, course)
    )


    connection.commit()
    connection.close()


    flash("Student added successfully!")

    return redirect("/")



@app.route("/delete/<int:id>")
def delete_student(id):

    connection = connect_db()
    cursor = connection.cursor()


    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )


    connection.commit()
    connection.close()


    flash("Student deleted successfully!")

    return redirect("/")



@app.route("/edit/<int:id>")
def edit_student(id):

    connection = connect_db()
    cursor = connection.cursor()


    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )


    student = cursor.fetchone()


    connection.close()


    return render_template(
        "edit.html",
        student=student
    )



@app.route("/update/<int:id>", methods=["POST"])
def update_student(id):

    name = request.form["name"]
    student_id = request.form["student_id"]
    course = request.form["course"]


    if name == "" or student_id == "" or course == "":
        flash("Please complete all student information!")
        return redirect("/edit/" + str(id))


    connection = connect_db()
    cursor = connection.cursor()


    cursor.execute(
        """
        UPDATE students
        SET name=?, student_id=?, course=?
        WHERE id=?
        """,
        (name, student_id, course, id)
    )


    connection.commit()
    connection.close()


    flash("Student updated successfully!")

    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)