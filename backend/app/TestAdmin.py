from admin import Admin
from student import Student
from pymongo import MongoClient
from course import Course

uri = "mongodb+srv://jjforsyth15:ClasslyLinked2025@classlylinked.bxbv8wy.mongodb.net/"
client = MongoClient(uri)

db = client["CLASSLYLINKED"]
courses = db["COURSES"]
students = db["STUDENTS"]

def admin_dashboard(user_name):
    print(f"\nWelcome, Admin {user_name}!")

    input("Press Enter to continue to dashboard...")

    while True:
        print("\n--- Admin Dashboard ---")
        print("1. Create New Course")
        print("2. Remove Student from STUDENTS")
        print("3. View All Courses")
        print("4. View All Students")
        print("5. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            course_name = input("Enter course name: ").strip()
            course_num = input("Enter course number: ").strip()
            Course(course_name, course_num)
        elif choice == "2":
            username = input("Enter username of student to remove: ").strip()
            admin = Student.load_by_username("admin")
            if admin.RemoveStudentFrom_STUDENTS(username) is True:
                print("Successfully removed student: " + username)
            else:
                print("Could not remove student")

        elif choice == "3":
            all_courses = courses.find()
            for course in all_courses:
                print(f"{course['courseName']} | #{course['courseNumber']}")

        elif choice == "4":
            all_students = students.find()
            for student in all_students:
                print(f"{student['firstName']} {student['lastName']} | {student['userName']}")
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")
