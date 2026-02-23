
import pandas as pd
from models.classroom import Classroom
from utils.utils import load_classrooms_from_csv, list_saved_classrooms
from cli.helpers import header, prompt, pause, divider
from cli.file_actions import action_load_csv, action_save_csv, action_save_json
from cli.analytics_actions import (
    action_top_student,
    action_lowest_student,
    action_rankings,
    action_grade_distribution,
)



def _create_new_classroom() -> tuple[Classroom, str]:
    header("Create New Classroom")
    while True:
        try:
            classroom_id = Classroom.validate_classroom_id(prompt("Classroom ID (e.g. C101)"))
            subject      = prompt("Subject (e.g. Mathematics)")
            if not Classroom.is_valid_subject(subject):
                raise ValueError("Subject cannot be empty.")
            filepath = prompt("Save file path (e.g. data/students.csv)")
            if not filepath:
                filepath = "data/students.csv"
            return Classroom(classroom_id, subject), filepath
        except (ValueError, TypeError) as e:
            print(f"\n  ✘  {e} — Please try again.\n")


def _load_existing_classroom() -> tuple[Classroom, str]:
    header("Load Existing Classroom")
    filepath = prompt("CSV file path (e.g. data/students.csv)")
    try:
        saved = list_saved_classrooms(filepath)
        if not saved:
            print("\n  ⚠  No classrooms found in that file. Creating a new one instead.")
            pause()
            return _create_new_classroom()

        df = pd.DataFrame(saved)
        print(f"\n{df.to_string(index=False)}\n")

        classroom_id = prompt("Enter Classroom ID to load")
        for c in load_classrooms_from_csv(filepath):
            if c.classroom_id == classroom_id:
                print(f"\n  ✔  Loaded '{classroom_id}' with {len(c.students)} student(s).")
                pause()
                return c, filepath

        print(f"\n  ✘  Classroom '{classroom_id}' not found. Creating a new one instead.")
        pause()
        return _create_new_classroom()
    except (FileNotFoundError, ValueError) as e:
        print(f"\n  ✘  {e}\n  Creating a new classroom instead.")
        pause()
        return _create_new_classroom()


def setup_classroom() -> tuple[Classroom, str]:
    header("Welcome to the Student Management System")
    print("  [1] Create a new classroom")
    print("  [2] Load an existing classroom from CSV")
    divider()
    choice = prompt("Choose an option")
    if choice == "2":
        return _load_existing_classroom()
    return _create_new_classroom()



def menu_analytics(classroom: Classroom) -> None:
    options = {
        "1": ("Top-performing student",    action_top_student),
        "2": ("Lowest-performing student", action_lowest_student),
        "3": ("Student rankings",          action_rankings),
        "4": ("Grade distribution",        action_grade_distribution),
        "0": ("Back",                      None),
    }
    while True:
        header(f"Analytics — {classroom.classroom_id} ({classroom.subject})")
        for key, (label, _) in options.items():
            print(f"  [{key}] {label}")
        divider()
        choice = prompt("Choose an option")
        if choice == "0":
            break
        entry = options.get(choice)
        if entry:
            _, action = entry
            action(classroom)
        else:
            print("\n  ✘  Invalid option. Please try again.")
            pause()


def menu_files(classroom: Classroom) -> None:
    options = {
        "1": ("Load students from CSV", action_load_csv),
        "2": ("Save classroom to CSV",  action_save_csv),
        "3": ("Save students to JSON",  action_save_json),
        "0": ("Back",                   None),
    }
    while True:
        header("File Management")
        for key, (label, _) in options.items():
            print(f"  [{key}] {label}")
        divider()
        choice = prompt("Choose an option")
        if choice == "0":
            break
        entry = options.get(choice)
        if entry:
            _, action = entry
            action(classroom)
        else:
            print("\n  ✘  Invalid option. Please try again.")
            pause()
