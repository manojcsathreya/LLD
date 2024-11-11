from datetime import datetime
from typing import List, Dict


# Course Class
class Course:
    def __init__(self, code: str, name: str, instructor: str, max_capacity: int, enrolled_students: int):
        self.code = code
        self.name = name
        self.instructor = instructor
        self.max_capacity = max_capacity
        self.enrolled_students = enrolled_students

    def set_enrolled_students(self, enrolled_students: int):
        self.enrolled_students = enrolled_students

    def get_code(self) -> str:
        return self.code

    def get_name(self) -> str:
        return self.name

    def get_instructor(self) -> str:
        return self.instructor

    def get_max_capacity(self) -> int:
        return self.max_capacity

    def get_enrolled_students(self) -> int:
        return self.enrolled_students


# Student Class
class Student:
    def __init__(self, student_id: int, name: str, email: str, registered_courses: List[Course]):
        self.id = student_id
        self.name = name
        self.email = email
        self.registered_courses = registered_courses

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_registered_courses(self) -> List[Course]:
        return self.registered_courses


# Registration Class
class Registration:
    def __init__(self, student: Student, course: Course, registration_time: datetime):
        self.student = student
        self.course = course
        self.registration_time = registration_time


# Course Registration System
class CourseRegistrationSystem:
    instance = None
    courses: Dict[str, Course] = {}
    students: Dict[int, Student] = {}
    registrations: List[Registration] = []

    @staticmethod
    def get_instance():
        if CourseRegistrationSystem.instance is None:
            CourseRegistrationSystem.instance = CourseRegistrationSystem()
        return CourseRegistrationSystem.instance

    def add_course(self, course: Course):
        self.courses[course.get_code()] = course

    def add_student(self, student: Student):
        self.students[student.get_id()] = student

    def search_courses(self, query: str) -> List[Course]:
        result = []
        for course in self.courses.values():
            if query in course.get_code() or query in course.get_name():
                result.append(course)
        return result

    def register_course(self, student: Student, course: Course) -> bool:
        if course.get_enrolled_students() < course.get_max_capacity():
            registration = Registration(student, course, datetime.now())
            self.registrations.append(registration)
            student.get_registered_courses().append(course)
            course.set_enrolled_students(course.get_enrolled_students() + 1)
            self._notify_observers(course)
            return True
        return False

    def get_registered_courses(self, student: Student) -> List[Course]:
        return student.get_registered_courses()

    def _notify_observers(self, course: Course):
        # Notify observers (e.g., UI) about the updated course enrollment
        # Placeholder for notification logic
        pass


# Course Registration Demo
class CourseRegistrationDemo:
    @staticmethod
    def run():
        registration_system = CourseRegistrationSystem.get_instance()

        # Create courses
        course1 = Course("CS101", "Introduction to Programming", "John Doe", 50, 0)
        course2 = Course("CS201", "Data Structures and Algorithms", "Jane Smith", 30, 0)
        registration_system.add_course(course1)
        registration_system.add_course(course2)

        # Create students
        student1 = Student(1, "Alice", "alice@example.com", [])
        student2 = Student(2, "Bob", "bob@example.com", [])
        registration_system.add_student(student1)
        registration_system.add_student(student2)

        # Search for courses
        search_results = registration_system.search_courses("CS")
        print("Search Results:")
        for course in search_results:
            print(f"{course.get_code()} - {course.get_name()}")

        # Register courses for students
        registered1 = registration_system.register_course(student1, course1)
        registered2 = registration_system.register_course(student2, course1)
        registered3 = registration_system.register_course(student1, course2)

        print("Registration Results:")
        print(f"Student 1 - Course 1: {registered1}")
        print(f"Student 2 - Course 1: {registered2}")
        print(f"Student 1 - Course 2: {registered3}")

        # Get registered courses for a student
        registered_courses = registration_system.get_registered_courses(student1)
        print("Registered Courses for Student 1:")
        for course in registered_courses:
            print(f"{course.get_code()} - {course.get_name()}")


# Run the demo
if __name__ == "__main__":
    CourseRegistrationDemo.run()
