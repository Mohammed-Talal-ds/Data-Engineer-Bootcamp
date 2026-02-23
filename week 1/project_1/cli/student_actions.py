
from models.student import Student
from models.classroom import Classroom
from utils.utils import display_student_report, display_classroom_report
from cli.helpers import header, prompt, pause, require_students


def action_add_student(classroom: Classroom) -> None:
    header("Add Student")
    try:
        name       = Student.validate_name(prompt("Name"))
        student_id = Student.validate_student_id(prompt("Student ID"))
        grades_raw = prompt("Grades (comma-separated, e.g. 85,90,78) — leave blank to skip")

        grades: list[float] = []
        if grades_raw:
            for part in grades_raw.split(","):
                grades.append(Student.validate_grade(part.strip()))

        student = Student(name, student_id, grades, classroom.classroom_id)
        classroom.add_student(student)
        print(f"\n  ✔  '{name}' added successfully.")
    except (ValueError, TypeError) as e:
        print(f"\n  ✘  Error: {e}")
    pause()


def action_remove_student(classroom: Classroom) -> None:
    header("Remove Student")
    if not require_students(classroom):
        pause()
        return
    try:
        student_id = prompt("Enter Student ID to remove")
        removed    = classroom.remove_student(student_id)
        print(f"\n  ✔  '{removed.name}' (ID: {removed.student_id}) removed.")
    except ValueError as e:
        print(f"\n  ✘  Error: {e}")
    pause()


def action_search_student(classroom: Classroom) -> None:
    header("Search Student")
    if not require_students(classroom):
        pause()
        return
    student_id = prompt("Enter Student ID to search")
    student    = classroom.search_student(student_id)
    if student:
        print()
        display_student_report(student)
    else:
        print(f"\n  ✘  No student found with ID '{student_id}'.")
    pause()


def action_add_grade(classroom: Classroom) -> None:
    header("Add Grade to Student")
    if not require_students(classroom):
        pause()
        return
    try:
        student_id = prompt("Student ID")
        student    = classroom.search_student(student_id)
        if not student:
            print(f"\n  ✘  No student found with ID '{student_id}'.")
            pause()
            return
        grade = Student.validate_grade(prompt(f"New grade for {student.name}"))
        student.add_grade(grade)
        print(f"\n  ✔  Grade {grade} added. New average: {student.calculate_average():.2f}")
    except (ValueError, TypeError) as e:
        print(f"\n  ✘  Error: {e}")
    pause()


def action_view_all(classroom: Classroom) -> None:
    header("All Students")
    if not require_students(classroom):
        pause()
        return
    display_classroom_report(classroom)
    pause()
