from collections import Counter
from models.student import Student
from models.classroom import Classroom



def top_performing_student(students: list[Student]) -> Student:

    if not students:
        raise ValueError("Cannot determine top performer: student list is empty.")
    return max(students, key=lambda s: s.calculate_average())


def lowest_performing_student(students: list[Student]) -> Student:

    if not students:
        raise ValueError("Cannot determine lowest performer: student list is empty.")
    return min(students, key=lambda s: s.calculate_average())




def rank_students(
    students: list[Student], descending: bool = True
) -> list[tuple[int, Student]]:

    if not students:
        return []

    sorted_students = sorted(
        students, key=lambda s: s.calculate_average(), reverse=descending
    )

    ranked: list[tuple[int, Student]] = []
    rank = 1
    for i, student in enumerate(sorted_students):
        if i > 0:
            prev_avg = sorted_students[i - 1].calculate_average()
            curr_avg = student.calculate_average()
            if curr_avg != prev_avg:
                rank = i + 1 
        ranked.append((rank, student))

    return ranked




def grade_distribution(students: list[Student]) -> dict[str, int]:

    base: dict[str, int] = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    counts = Counter(s.grade_category() for s in students)
    return {**base, **counts}


def grade_distribution_percentage(students: list[Student]) -> dict[str, float]:

    if not students:
        return {"A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0, "F": 0.0}
    dist = grade_distribution(students)
    total = len(students)
    return {category: round(count / total * 100, 2) for category, count in dist.items()}




def classroom_top_performer(classroom: Classroom) -> Student:
    return top_performing_student(classroom.students)


def classroom_lowest_performer(classroom: Classroom) -> Student:
    return lowest_performing_student(classroom.students)


def classroom_ranking(
    classroom: Classroom, descending: bool = True
) -> list[tuple[int, Student]]:
    return rank_students(classroom.students, descending=descending)


def classroom_grade_distribution(classroom: Classroom) -> dict[str, int]:
    return grade_distribution(classroom.students)



def display_ranking(ranked: list[tuple[int, Student]]):
    import pandas as pd
    rows = [
        {
            "Rank":       rank,
            "Name":       s.name,
            "Student ID": s.student_id,
            "Average":    f"{s.calculate_average():.2f}",
            "Category":   s.grade_category(),
        }
        for rank, s in ranked
    ]
    df = pd.DataFrame(rows)
    print(f"\n{df.to_string(index=False)}\n")


def display_grade_distribution(dist: dict[str, int], percentages: dict[str, float] = None):
    import pandas as pd
    rows = [
        {
            "Grade":      cat,
            "Count":      dist.get(cat, 0),
            "Percentage": f"{percentages[cat]:.1f}%" if percentages else "N/A",
        }
        for cat in ["A", "B", "C", "D", "F"]
    ]
    df = pd.DataFrame(rows)
    print(f"\n{df.to_string(index=False)}\n")
