from student import Student
from pymongo import MongoClient
from course import Course

uri = "mongodb+srv://jjforsyth15:ClassLink2025@cluster1.imnisby.mongodb.net/"
client = MongoClient(uri)

db = client["CLASSLINK"]
courses = db["COURSES"]
students = db["STUDENTS"]

class Admin(Student):
    def __init__(self, first, last, username, password):
        super().__init__(first, last, username, password, isAdmin=True)


    def CreateCourse(self, c_name, c_num):
        
        course = courses.find_one({"courseNumber": c_num})

        if course is not None:
            print("Course already exists")
            return False
        else:
            course = Course(c_name, c_num)
            print(f"Course '{c_name}' ({c_num}) created.")
            return True

    def RemoveStudentFrom_course(self, studentToRemove, courseToRemoveFrom):
        student = students.find_one({"userName":studentToRemove})
        course = courses.find_one({"courseNumber": courseToRemoveFrom})

        if studentToRemove not in course["students"]:
            print("Student not in course")
            return False
        else:
            students.update_one(
                {"userName": student["userName"]},
                {"$pull": {"courses": courseToRemoveFrom}}
            )

            courses.update_one(
                {"courseNumber": course["courseNumber"]},
                {"$pull": {"students": studentToRemove}}
            )
            return True

    def RemoveStudentFrom_STUDENTS(self, studentToRemove):

        student = students.find_one({"userName": studentToRemove})

        if student is None:
            print("Student does not exist")
            return False
        else:
            students.delete_one({"userName": studentToRemove})
            courses.update_many({}, {"$pull": {"students": studentToRemove}})
            return True
        

    def PrintCourses(self):
        for i, course in enumerate(courses.find(), 1):
            enrolled = len(course.get("students", []))
            print(i, ". Course: ", course["courseName"], " | Number: ", course["courseNumber"], " | Number of Students: ", enrolled)


    def PrintStudentsIn_STUDENTS(self):
        for i, student in enumerate(students.find(), 1):
            num_courses = len(student.get("courses", []))
            
            if student["isAdmin"] is True:
                print(i, ". Name: ", student["firstName"], " ", student["lastName"], " | Username:", student["userName"], " | Admin")
            else:
                print(i, ". Name: ", student["firstName"], " ", student["lastName"], " | Username:", student["userName"])

    def PromoteToAdmin(self, student_to_promote):
        admin = students.find_one({"userName": student_to_promote})

        if admin["isAdmin"] is True:
            print("Student is already admin")
            return False
        else:
            students.update_one(
                {"userName": student_to_promote},
                {"$set": {"isAdmin": True}}
                )
            return True
        
    def PrintStudentsIn_course(self, course_to_check):
        course = courses.find_one({"courseNumber": course_to_check})
        
        for i, username in enumerate(course["students"], 1):
            student = students.find_one({"userName": username})
            name = student["firstName"] + " " + student["lastName"]
            
            if student["isAdmin"] is True:
                print(i, ". Name: ", name, " | Username: ", username, " | Admin")
            else:
                print(i, ". Name: ", name, " | Username: ", username)
            

    # methods to create:

    # Added:
        #   CreateCourse - Add new course to COURSES
        #   RemoveStudentFrom_course - Remove student from a course
        #   RemoveStudentFrom_STUDENTS - Remove student from STUDENTS
        #   PrintCourses - Print list of courses
        #   PrintStudentsIn_STUDENTS -Print list of students
        #   PromoteAdmin - Promote student to admin
        #   PrintStudentsIn_course - List students in a course