import csv
import json
import os
import pandas as pd
from models.student import Student
from models.classroom import Classroom




def load_students_from_csv(filepath: str) -> list[Student]:
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"CSV file not found: '{filepath}'")

    students = []
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        required_columns = {"student_id", "name", "grades"}
        if not required_columns.issubset(set(reader.fieldnames or [])):
            raise ValueError(
                f"CSV must contain columns: {required_columns}. "
                f"Found: {set(reader.fieldnames or [])}"
            )
        for row_num, row in enumerate(reader, start=2):
            try:
                students.append(Student.from_csv_row(row))
            except (ValueError, TypeError) as e:
                raise ValueError(f"Error on row {row_num}: {e}") from e

    return students




def save_students_to_csv(students: list[Student], filepath: str):

    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["student_id", "name", "grades"])
        for student in students:
            grades_str = ",".join(str(g) for g in student.grades)
            writer.writerow([student.student_id, student.name, grades_str])




def save_students_to_json(students: list[Student], filepath: str):
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    data = [
        {
            "student_id": s.student_id,
            "name": s.name,
            "grades": s.grades,
        }
        for s in students
    ]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)




def save_classroom_to_csv(classroom: Classroom, filepath: str):
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    existing_rows: list[dict] = []
    if os.path.isfile(filepath):
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if "classroom_id" in (reader.fieldnames or []):
                existing_rows = [
                    row for row in reader
                    if row["classroom_id"] != classroom.classroom_id
                ]

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["classroom_id", "subject", "student_id", "name", "grades"])
        for row in existing_rows:
            writer.writerow([row["classroom_id"], row["subject"],
                             row["student_id"], row["name"], row["grades"]])
        for student in classroom.students:
            grades_str = ",".join(str(g) for g in student.grades)
            writer.writerow([classroom.classroom_id, classroom.subject,
                             student.student_id, student.name, grades_str])


def load_classrooms_from_csv(filepath: str) -> list[Classroom]:
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"CSV file not found: '{filepath}'")

    classroom_data: dict[str, dict] = {}
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"classroom_id", "subject", "student_id", "name", "grades"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(
                f"CSV must contain columns: {required}. "
                f"Found: {set(reader.fieldnames or [])}"
            )
        for row_num, row in enumerate(reader, start=2):
            try:
                cid     = Classroom.validate_classroom_id(row["classroom_id"])
                subject = row["subject"].strip()
                student = Student.from_csv_row(row, cid)
                if cid not in classroom_data:
                    classroom_data[cid] = {"subject": subject, "students": []}
                classroom_data[cid]["students"].append(student)
            except (ValueError, TypeError) as e:
                raise ValueError(f"Error on row {row_num}: {e}") from e

    return [
        Classroom.from_student_list(cid, data["subject"], data["students"])
        for cid, data in classroom_data.items()
    ]


def list_saved_classrooms(filepath: str) -> list[dict]:
    if not os.path.isfile(filepath):
        return []
    try:
        return [
            {
                "Classroom ID":  c.classroom_id,
                "Subject":       c.subject,
                "Students":      len(c.students),
                "Class Average": f"{c.calculate_classroom_average():.2f}",
            }
            for c in load_classrooms_from_csv(filepath)
        ]
    except (ValueError, KeyError):
        return []


def build_classroom_from_csv(
    filepath: str, classroom_id: str, subject: str
) -> Classroom:

    classroom = Classroom(classroom_id, subject)
    for student in load_students_from_csv(filepath):
        classroom.add_student(student)
    return classroom




def display_student_report(student: Student):
    df = pd.DataFrame([{
        "Student ID":   student.student_id,
        "Name":         student.name,
        "Classroom ID": student.classroom_id if student.classroom_id else "—",
        "Grades":       ", ".join(str(g) for g in student.grades) or "—",
        "Average":      f"{student.calculate_average():.2f}",
        "Category":     student.grade_category(),
    }])
    print(f"\n{df.to_string(index=False)}\n")


def display_classroom_report(classroom: Classroom):
    rows = [
        {
            "Student ID": s.student_id,
            "Name":       s.name,
            "Grades":     ", ".join(str(g) for g in s.grades) or "—",
            "Average":    f"{s.calculate_average():.2f}",
            "Category":   s.grade_category(),
        }
        for s in classroom.students
    ]
    df = (
        pd.DataFrame(rows)
        if rows
        else pd.DataFrame(columns=["Student ID", "Name", "Grades", "Average", "Category"])
    )
    print(f"\n{'═' * 65}")
    print(
        f"  Classroom : {classroom.classroom_id}  |  "
        f"Subject : {classroom.subject}  |  "
        f"Class Avg : {classroom.calculate_classroom_average():.2f}"
    )
    print(f"{'═' * 65}\n")
    print(df.to_string(index=False))
    print()
