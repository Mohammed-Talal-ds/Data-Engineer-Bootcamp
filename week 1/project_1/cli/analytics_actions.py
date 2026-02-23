
from models.classroom import Classroom
from utils.utils import display_student_report
from analytics.analytics import (
    classroom_top_performer,
    classroom_lowest_performer,
    classroom_ranking,
    classroom_grade_distribution,
    grade_distribution_percentage,
    display_ranking,
    display_grade_distribution,
)
from cli.helpers import header, pause, require_students


def action_top_student(classroom: Classroom) -> None:
    header("Top-Performing Student")
    if not require_students(classroom):
        pause()
        return
    display_student_report(classroom_top_performer(classroom))
    pause()


def action_lowest_student(classroom: Classroom) -> None:
    header("Lowest-Performing Student")
    if not require_students(classroom):
        pause()
        return
    display_student_report(classroom_lowest_performer(classroom))
    pause()


def action_rankings(classroom: Classroom) -> None:
    header("Student Rankings")
    if not require_students(classroom):
        pause()
        return
    ranked = classroom_ranking(classroom)
    display_ranking(ranked)
    pause()


def action_grade_distribution(classroom: Classroom) -> None:
    header("Grade Distribution")
    if not require_students(classroom):
        pause()
        return
    dist = classroom_grade_distribution(classroom)
    pct  = grade_distribution_percentage(classroom.students)
    display_grade_distribution(dist, pct)
    pause()
