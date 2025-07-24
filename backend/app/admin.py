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


    def createCourse(self, c_name, c_num):
        
        course = courses.find_one({"courseNumber": c_num})

        if course is not None:
            print("Course already exists")
            return False
        else:
            course = Course(c_name, c_num)
            print(f"Course '{c_name}' ({c_num}) created.")
            return True

    def removeStudentFrom_course(self, studentToRemove, courseToRemoveFrom):
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

    
        

    # methods to create:
    
    #   Remove student from STUDENTS
    #   Print list of courses
    #   Print list of students
    #   Promote student to admin
    #   List students in a course

    # Added:
        #   Add new course to COURSES
        #   Remove student from a course