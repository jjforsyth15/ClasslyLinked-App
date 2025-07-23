from student import Student
from pymongo import MongoClient

uri = "mongodb+srv://jjforsyth15:ClassLink2025@cluster1.imnisby.mongodb.net/"
client = MongoClient(uri)

db = client["CLASSLINK"]
courses = db["COURSES"]


class Course:
    def __init__(self, name, number):
        self.courseName = name
        self.courseNumber = number
        self.students = []

        if courses.find_one({"courseName": name, "courseNumber": number}):
            print("Course already exists")
        else:
            courses.insert_one({
                "courseName": name,
                "courseNumber": number
            })

    def __str__(self):
        return f"Course: {self.courseName}, #{self.courseNumber}"

    def AddStudent(self, studentToAdd):
        self.students.append(studentToAdd)


    def printStudents(self):
        print(self.students)


    