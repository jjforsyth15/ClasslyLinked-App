from student import Student
from pymongo import MongoClient

uri = "mongodb+srv://jjforsyth15:ClasslyLinked2025@classlylinked.bxbv8wy.mongodb.net/"
client = MongoClient(uri)

db = client["CLASSLYLINKED"]
courses = db["COURSES"]
students = db["STUDENTS"]

class Course:
    # Constructor for course
    def __init__(self, name, number):
        self.courseName = name
        self.courseNumber = number

        if courses.find_one({"courseName": name, "courseNumber": number}):
            print("Course already exists")
            self.valid = False
        else:
            courses.insert_one({
                "courseName": name,
                "courseNumber": number,
                "students": []
            })
            self.valid = True

    # to print course
    def __str__(self):
        return f"Course: {self.courseName}, #{self.courseNumber}"

    # Add a student to course
    def AddStudent(self, studentToAdd):
        
        if self.is_enrolled(studentToAdd) is True:
            print("Student already enrolled")
            return False
        else:
            courses.update_one(
                {"courseNumber": self.courseNumber},
                {"$addToSet": {"students": studentToAdd}}
            )
            return True

    # Remove a student from course
    def RemoveStudent(self, studentToRemove):
        if self.is_enrolled(studentToRemove) is False:
            print("Student is not enrolled in class")
            return False #could not complete action successfully
        else:
            courses.update_one(
                {"courseNumber": self.courseNumber},
                {"$pull": {"students": studentToRemove}}
            )
            return True # successfully removed student

    # Print all students in course
    def printStudents(self):
        course_doc = courses.find_one({"courseNumber": self.courseNumber})

        student_usernames = course_doc.get("students", [])
        num = 0
        for username in student_usernames:
            num += 1
            student_doc = students.find_one({"userName": username})
            print(num, ". ", student_doc["firstName"], student_doc["lastName"])


    # Helper method to check if a specific student is enrolled in course
    def is_enrolled(self, studentToCheck):
        course_doc = courses.find_one({"courseNumber": self.courseNumber})

        if studentToCheck in course_doc["students"]:
            return True
        else:
            return False
        
    # Static method to load a course from the COURSES database collection without creating new course
    @classmethod 
    def load_by_number(cls, course_num):
        course_doc = courses.find_one({"courseNumber": course_num})

        if not course_doc:
            return None

        course = cls.__new__(cls)
        course.courseName = course_doc["courseName"]
        course.courseNumber = course_doc["courseNumber"]

        return course