from utils.utils import save_classroom_to_csv
from cli.helpers import header, prompt, pause, divider
from cli.student_actions import (
    action_view_all,
    action_add_student,
    action_remove_student,
    action_search_student,
    action_add_grade,
)
from cli.file_actions import action_save_classroom
from cli.menus import setup_classroom, menu_files, menu_analytics


def main() -> None:
    classroom, filepath = setup_classroom()

    def _save_shortcut(_classroom=None) -> None:
        nonlocal filepath
        filepath = action_save_classroom(classroom, filepath)

    main_options = {
        "1": ("View all students",        action_view_all),
        "2": ("Add student",              action_add_student),
        "3": ("Remove student",           action_remove_student),
        "4": ("Search student",           action_search_student),
        "5": ("Add grade to student",     action_add_grade),
        "6": ("Save classroom",           _save_shortcut),
        "7": ("File management",          menu_files),
        "8": ("Analytics",                menu_analytics),
        "0": ("Exit",                     None),
    }

    while True:
        header(
            f"Main Menu — {classroom.classroom_id} "
            f"({classroom.subject})  |  Students: {len(classroom.students)}"
        )
        for key, (label, _) in main_options.items():
            print(f"  [{key}] {label}")
        divider()
        choice = prompt("Choose an option")

        if choice == "0":
            if classroom.students:
                answer = prompt(
                    f"Save classroom before exiting? [Y/n] (file: {filepath})"
                ).lower()
                if answer != "n":
                    try:
                        save_classroom_to_csv(classroom, filepath)
                        print(f"\n  ✔  Classroom saved to '{filepath}'.")
                    except OSError as e:
                        print(f"\n  ✘  Could not save: {e}")
            print("\n  Goodbye!\n")
            break

        entry = main_options.get(choice)
        if entry:
            _, action = entry
            action(classroom)
        else:
            print("\n  ✘  Invalid option. Please try again.")
            pause()


if __name__ == "__main__":
    main()

