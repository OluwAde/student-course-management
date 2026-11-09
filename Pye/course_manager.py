"""
COS201 Programming I - Mid-Semester Lab Assessment
Student Course Management System (console version)

Features: add, view, search, total units, save to file, load from file.
Demonstrates: classes/objects, loops, recursion, string processing,
exception handling, and file reading/writing.
"""

import csv
import re

DEFAULT_FILE = "courses.csv"
CODE_PATTERN = re.compile(r"^[A-Z]{3}\d{3}$")  # e.g. COS201


class InvalidCourseError(Exception):
    """Raised when course details fail validation."""


class Course:
    """Represents a single course."""

    def __init__(self, code, title, units):
        self.code = code
        self.title = title
        self.units = units

    def __str__(self):
        return f"{self.code:<10}{self.title:<40}{self.units:>5}"


class CourseManager:
    """Stores courses and performs all operations on them."""

    def __init__(self):
        self.courses = []  # internal structure: a list of Course objects

    # ---------- validation / string processing ----------
    @staticmethod
    def clean_code(raw):
        """Trim, remove inner spaces, and uppercase a course code."""
        return raw.strip().replace(" ", "").upper()

    @staticmethod
    def clean_title(raw):
        """Trim, collapse repeated spaces, and title-case a course title."""
        return " ".join(raw.split()).title()

    def validate(self, code, title, units_text):
        code = self.clean_code(code)
        title = self.clean_title(title)

        if not CODE_PATTERN.match(code):
            raise InvalidCourseError(
                "Course code must be 3 letters followed by 3 digits (e.g. COS201)."
            )
        if not title:
            raise InvalidCourseError("Course title cannot be empty.")
        try:
            units = int(str(units_text).strip())
        except ValueError:
            raise InvalidCourseError("Units must be a whole number.")
        if not 1 <= units <= 10:
            raise InvalidCourseError("Units must be between 1 and 10.")
        return code, title, units

    # ---------- core operations ----------
    def add_course(self, code, title, units_text):
        code, title, units = self.validate(code, title, units_text)
        if self.find_course(code) is not None:
            raise InvalidCourseError(f"Course {code} has already been added.")
        self.courses.append(Course(code, title, units))
        return code

    def view_courses(self):
        if not self.courses:
            print("\nNo courses recorded yet.")
            return
        print(f"\n{'CODE':<10}{'TITLE':<40}{'UNITS':>5}")
        print("-" * 55)
        for course in self.courses:  # iteration
            print(course)

    def find_course(self, code, index=0):
        """Recursive search: checks one course, then calls itself on the next."""
        code = self.clean_code(code)
        if index >= len(self.courses):
            return None
        if self.courses[index].code == code:
            return self.courses[index]
        return self.find_course(code, index + 1)

    def total_units(self, index=0):
        """Recursive count: this course's units + the units of the rest."""
        if index >= len(self.courses):
            return 0
        return self.courses[index].units + self.total_units(index + 1)

    # ---------- file handling ----------
    def save_to_file(self, filename=DEFAULT_FILE):
        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for c in self.courses:
                    writer.writerow([c.code, c.title, c.units])
        except OSError as err:
            raise IOError(f"Could not save to '{filename}': {err}")
        return len(self.courses)

    def load_from_file(self, filename=DEFAULT_FILE):
        loaded = []
        try:
            with open(filename, "r", newline="", encoding="utf-8") as f:
                for line_no, row in enumerate(csv.reader(f), start=1):
                    if not row:
                        continue
                    if len(row) != 3:
                        raise InvalidCourseError(f"Line {line_no} is not in the expected format.")
                    code, title, units = self.validate(*row)
                    loaded.append(Course(code, title, units))
        except FileNotFoundError:
            raise IOError(f"File '{filename}' was not found. Save some courses first.")
        except OSError as err:
            raise IOError(f"Could not read '{filename}': {err}")
        self.courses = loaded  # only replace the list if the whole file was valid
        return len(loaded)


# ---------- console interface ----------
MENU = """
===== STUDENT COURSE MANAGEMENT SYSTEM =====
1. Add Course
2. View All Courses
3. Search Course by Code
4. Compute Total Units
5. Save to File
6. Load from File
7. Exit Program
"""


def main():
    manager = CourseManager()

    while True:  # iteration: the menu repeats until the user exits
        print(MENU)
        choice = input("Enter your choice (1-7): ").strip()

        try:
            if choice == "1":
                code = input("Course code (e.g. COS201): ")
                title = input("Course title: ")
                units = input("Credit units: ")
                saved_code = manager.add_course(code, title, units)
                print(f"Course {saved_code} added successfully.")

            elif choice == "2":
                manager.view_courses()

            elif choice == "3":
                code = input("Enter course code to search: ")
                course = manager.find_course(code)
                if course:
                    print("\nCourse found:")
                    print(f"{'CODE':<10}{'TITLE':<40}{'UNITS':>5}")
                    print(course)
                else:
                    print("No course found with that code.")

            elif choice == "4":
                print(f"Total units: {manager.total_units()}")

            elif choice == "5":
                count = manager.save_to_file()
                print(f"Saved {count} course(s) to {DEFAULT_FILE}.")

            elif choice == "6":
                count = manager.load_from_file()
                print(f"Loaded {count} course(s) from {DEFAULT_FILE}.")

            elif choice == "7":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 7.")

        except (InvalidCourseError, IOError) as err:
            print(f"Error: {err}")


if __name__ == "__main__":
    main()
