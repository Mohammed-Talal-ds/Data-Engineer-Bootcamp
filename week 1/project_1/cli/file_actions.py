
from models.classroom import Classroom
from utils.utils import (
    load_students_from_csv,
    save_students_to_json,
    save_classroom_to_csv,
)
from cli.helpers import header, prompt, pause, require_students


def action_load_csv(classroom: Classroom) -> None:
    header("Load Students from CSV")
    filepath = prompt("CSV file path (e.g. data/students.csv)")
    try:
        students = load_students_from_csv(filepath)
        added    = 0
        skipped  = 0
        for student in students:
            try:
                student.classroom_id = classroom.classroom_id  # stamp FK
                classroom.add_student(student)
                added += 1
            except ValueError:
                skipped += 1  # duplicate ID — skip silently
        print(f"\n  ✔  Loaded {added} student(s).", end="")
        if skipped:
            print(f" ({skipped} duplicate(s) skipped.)", end="")
        print()
    except (FileNotFoundError, ValueError) as e:
        print(f"\n  ✘  Error: {e}")
    pause()


def action_save_csv(classroom: Classroom) -> None:
    header("Save Classroom to CSV")
    if not require_students(classroom):
        pause()
        return
    filepath = prompt("Save path (e.g. data/students.csv)")
    try:
        save_classroom_to_csv(classroom, filepath)
        print(f"\n  ✔  Saved {len(classroom.students)} student(s) to '{filepath}'.")
    except OSError as e:
        print(f"\n  ✘  Error: {e}")
    pause()


def action_save_json(classroom: Classroom) -> None:
    header("Save Students to JSON")
    if not require_students(classroom):
        pause()
        return
    filepath = prompt("Save path (e.g. data/students.json)")
    try:
        save_students_to_json(classroom.students, filepath)
        print(f"\n  ✔  Saved {len(classroom.students)} student(s) to '{filepath}'.")
    except OSError as e:
        print(f"\n  ✘  Error: {e}")
    pause()


def action_save_classroom(classroom: Classroom, filepath: str) -> str:
    """Save classroom and return the (possibly updated) filepath."""
    header("Save Classroom")
    entered = prompt(f"Save path [{filepath}] — press Enter to keep")
    target  = entered if entered else filepath
    try:
        save_classroom_to_csv(classroom, target)
        print(f"\n  ✔  Classroom '{classroom.classroom_id}' saved to '{target}'.")
    except OSError as e:
        print(f"\n  ✘  Error: {e}")
    pause()
    return target
