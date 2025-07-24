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


    while True:
        print("\n--- Admin Dashboard ---")
        print("1. Create New Course")
        print("2. View All Courses")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            course_name = input("Enter course name: ")
            course_num = input("Enter course number: ")
            Course(course_name, course_num)
        elif choice == "2":
            all_courses = courses.find()
            for course in all_courses:
                print(f"{course['courseName']} | #{course['courseNumber']}")
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid option. Try again.")
