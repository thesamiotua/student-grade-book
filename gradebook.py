"""
Command-line Student Grade Book
--------------------------------
Lets a user add students, log grades per subject, view a student's
grades, and calculate their average. Data is stored in a MySQL database.
"""

import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "gradebook_user",
    "password": "GradeBook#2026",
    "database": "grade_book",
}


def get_connection():
    """
    Open and return a new connection to the MySQL database.
    Every function below calls this to get its own connection,
    keeping database logic isolated from the CLI logic.
    """
    return mysql.connector.connect(**DB_CONFIG)


def add_student(name):
    """
    Insert a new student and return their generated id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name) VALUES (%s)", (name,))
    conn.commit()
    student_id = cursor.lastrowid  # the auto-generated id for the new row
    cursor.close()
    conn.close()
    return student_id


def list_students():
    """
    Return all students as a list of (id, name) tuples.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM students ORDER BY id")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return students


def add_grade(student_id, subject, grade):
    """
    Insert a grade entry for a given student.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO grades (student_id, subject, grade) VALUES (%s, %s, %s)",
        (student_id, subject, grade),
    )
    conn.commit()
    cursor.close()
    conn.close()


def view_grades(student_id):
    """
    Return all (subject, grade) pairs for a given student.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT subject, grade FROM grades WHERE student_id = %s",
        (student_id,),
    )
    grades = cursor.fetchall()
    cursor.close()
    conn.close()
    return grades


def calculate_average(student_id):
    """
    Let MySQL calculate the average grade directly, using AVG().
    Returns None if the student has no grades yet.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT AVG(grade) FROM grades WHERE student_id = %s",
        (student_id,),
    )
    result = cursor.fetchone()[0]  # AVG() returns a single value
    cursor.close()
    conn.close()
    return result


def print_students():
    students = list_students()
    if not students:
        print("No students yet.\n")
        return
    print("\n--- Students ---")
    for sid, name in students:
        print(f"{sid}. {name}")
    print()


def handle_add_student():
    name = input("Student name: ").strip()
    if not name:
        print("Name can't be empty.\n")
        return
    student_id = add_student(name)
    print(f"Added {name} with id {student_id}.\n")


def handle_add_grade():
    print_students()
    try:
        student_id = int(input("Student id: ").strip())
    except ValueError:
        print("Invalid id.\n")
        return

    subject = input("Subject: ").strip()
    try:
        grade = float(input("Grade: ").strip())
    except ValueError:
        print("Invalid grade.\n")
        return

    add_grade(student_id, subject, grade)
    print("Grade added.\n")


def handle_view_grades():
    print_students()
    try:
        student_id = int(input("Student id: ").strip())
    except ValueError:
        print("Invalid id.\n")
        return

    grades = view_grades(student_id)
    if not grades:
        print("No grades recorded for this student.\n")
        return

    print("\n--- Grades ---")
    for subject, grade in grades:
        print(f"{subject:<15} {grade}")

    avg = calculate_average(student_id)
    print(f"\nAverage: {avg:.2f}\n")


def main():
    menu = """
Student Grade Book
1. Add student
2. Add grade
3. View a student's grades + average
4. List all students
5. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            handle_add_student()
        elif choice == "2":
            handle_add_grade()
        elif choice == "3":
            handle_view_grades()
        elif choice == "4":
            print_students()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.\n")


if __name__ == "__main__":
    main()