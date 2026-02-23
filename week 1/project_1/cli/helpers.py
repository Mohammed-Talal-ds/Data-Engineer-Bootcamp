
from models.classroom import Classroom


def divider(char: str = "─", width: int = 50) -> None:
    print(char * width)


def header(title: str) -> None:
    divider("═")
    print(f"  {title}")
    divider("═")


def prompt(label: str) -> str:
    return input(f"  {label}: ").strip()


def pause() -> None:
    input("\n  Press Enter to continue...")


def require_students(classroom: Classroom) -> bool:
    """Print a warning and return False when the classroom is empty."""
    if not classroom.students:
        print("\n  ⚠  No students in the classroom yet.")
        return False
    return True
