class Student:
    def __init__(self, name: str, student_id: str, grades: list[float] = None, classroom_id: str = ""):
        self.__name = name
        self.__student_id = student_id
        self.__grades = grades if grades is not None else []
        self.__classroom_id = classroom_id 

    @property
    def classroom_id(self) -> str:
        return self.__classroom_id

    @classroom_id.setter
    def classroom_id(self, value: str):
        self.__classroom_id = str(value)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def student_id(self) -> str:
        return self.__student_id

    @property
    def grades(self) -> list[float]:
        return list(self.__grades)

    @name.setter
    def name(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string.")
        self.__name = value

    @grades.setter
    def grades(self, value: list[float]):
        if not isinstance(value, list):
            raise ValueError("Grades must be a list.")
        self.__grades = value


    @staticmethod
    def validate_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if not all(c.isalpha() or c.isspace() for c in name):
            raise ValueError(f"Name '{name}' contains invalid characters.")
        return name.strip()

    @staticmethod
    def validate_student_id(student_id: str) -> str:
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Student ID must be a non-empty string.")
        if not student_id.strip().isalnum():
            raise ValueError(f"Student ID '{student_id}' must be alphanumeric.")
        return student_id.strip()

    @staticmethod
    def validate_grade(grade) -> float:
        try:
            grade = float(grade)
        except (TypeError, ValueError):
            raise ValueError(f"Grade '{grade}' is not a valid number.")
        if not (0.0 <= grade <= 100.0):
            raise ValueError(f"Grade {grade} is out of range (0–100).")
        return grade

    @staticmethod
    def validate_grades_list(grades: list) -> list[float]:
        if not isinstance(grades, list):
            raise TypeError("Grades must be provided as a list.")
        return [Student.validate_grade(g) for g in grades]


    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        name         = cls.validate_name(data["name"])
        student_id   = cls.validate_student_id(data["student_id"])
        grades       = cls.validate_grades_list(data.get("grades", []))
        classroom_id = str(data.get("classroom_id", ""))
        return cls(name, student_id, grades, classroom_id)

    @classmethod
    def from_csv_row(cls, row: dict, classroom_id: str = "") -> "Student":
        name       = cls.validate_name(row["name"])
        student_id = cls.validate_student_id(row["student_id"])
        raw        = [g.strip() for g in row.get("grades", "").split(",") if g.strip()]
        grades     = cls.validate_grades_list(raw)
        cid        = row.get("classroom_id", "") or classroom_id
        return cls(name, student_id, grades, cid)

    def add_grade(self, grade: float):
        if not isinstance(grade, (int, float)):
            raise ValueError("Grade must be a numeric value.")
        if not (0 <= grade <= 100):
            raise ValueError("Grade must be between 0 and 100.")
        self.__grades.append(float(grade))

    def calculate_average(self) -> float:
        if not self.__grades:
            return 0.0
        return sum(self.__grades) / len(self.__grades)

    def grade_category(self) -> str:
        average = self.calculate_average()
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"

    def __repr__(self) -> str:
        return (
            f"Student(name={self.__name!r}, "
            f"student_id={self.__student_id!r}, "
            f"classroom_id={self.__classroom_id!r}, "
            f"average={self.calculate_average():.2f}, "
            f"category={self.grade_category()!r})"
        )
