from models.student import Student


class Classroom:
    def __init__(self, classroom_id: str, subject: str):
        self.__classroom_id = classroom_id
        self.__subject = subject
        self.__students: list[Student] = []

    @property
    def classroom_id(self) -> str:
        return self.__classroom_id

    @property
    def subject(self) -> str:
        return self.__subject

    @property
    def students(self) -> list[Student]:
        return list(self.__students)


    @staticmethod
    def validate_classroom_id(classroom_id: str) -> str:
        if not isinstance(classroom_id, str) or not classroom_id.strip():
            raise ValueError("Classroom ID must be a non-empty string.")
        if not classroom_id.strip().isalnum():
            raise ValueError(f"Classroom ID '{classroom_id}' must be alphanumeric.")
        return classroom_id.strip()

    @staticmethod
    def is_valid_subject(subject: str) -> bool:
        return isinstance(subject, str) and bool(subject.strip())


    @classmethod
    def from_student_list(cls, classroom_id: str, subject: str, students: "list[Student]") -> "Classroom":
        classroom = cls(classroom_id, subject)
        for student in students:
            classroom.add_student(student)
        return classroom

    def add_student(self, student: Student):
        if not isinstance(student, Student):
            raise TypeError("Only Student instances can be added.")
        if self.search_student(student.student_id):
            raise ValueError(f"Student with ID '{student.student_id}' is already enrolled.")
        self.__students.append(student)

    def remove_student(self, student_id: str) -> Student:
        student = self.search_student(student_id)
        if not student:
            raise ValueError(f"No student with ID '{student_id}' found in this classroom.")
        self.__students.remove(student)
        return student

    def search_student(self, student_id: str) -> Student | None:
        for student in self.__students:
            if student.student_id == student_id:
                return student
        return None

    def calculate_classroom_average(self) -> float:
        if not self.__students:
            return 0.0
        return sum(s.calculate_average() for s in self.__students) / len(self.__students)

    def __repr__(self) -> str:
        return (
            f"Classroom(id={self.__classroom_id!r}, "
            f"subject={self.__subject!r}, "
            f"students={len(self.__students)}, "
            f"average={self.calculate_classroom_average():.2f})"
        )
