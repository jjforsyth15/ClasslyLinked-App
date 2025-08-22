from pymongo import MongoClient
import bcrypt

uri = "mongodb+srv://jjforsyth15:ClasslyLinked2025@classlylinked.bxbv8wy.mongodb.net/"
client = MongoClient(uri)

db = client["CLASSLYLINKED"]
students = db["STUDENTS"]
courses = db["COURSES"]

class Student: 
    # constructor for Student class. Takes in first name, last name, username, and password
    def __init__(self, first, last, username, password, isAdmin=False):
        self.firstName = first
        self.lastName = last
        # self.myCourses = course if courses is not None else []  -- will add later
        self.userName = username
        self.isAdmin = isAdmin

        #hashes password
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        password = "" # erases password in Student class for security - still exists in database
        
        # checks if student already exists - might not need later
        if students.find_one({"firstName": first, "lastName": last}):
            print("Student already exists")
        else:
            students.insert_one({
                "firstName": first,
                "lastName": last,
                "userName": username,
                "passwordHashed": hashed,
                "isAdmin": isAdmin,
                "courses": [],
                "interests": [],
                "mates": []
            })
    
    # get methods
    # set methods






    # how Student is displayed -- will need to update to look better
    def __str__(self):
        return f"Student: {self.firstName} {self.lastName}, Courses: {', '.join(self.myCourses)}"
    
    # def to_dict(self):
    #     return {
    #         "firstName": self.firstName,
    #         "lastName": self.lastName,
    #         "courses": self.myCourses
    #     }
    
    # method to add a course to Student
    def add_course(self, courseToAdd):
        from course import Course   

        if self.is_enrolled(courseToAdd):
            print("Already enrolled in this course")
            return False
        else:
            students.update_one(
                {"userName": self.userName},
                {"$push": {"courses": courseToAdd}}
            )
            return True


    # method to remove a course from Student
    def remove_course(self, courseToRemove):
        from course import Course

        if not self.is_enrolled(courseToRemove):
            print("Student not enrolled in course")
            return False # could not complete action successfully
        else:
            students.update_one(
                {"userName": self.userName},
                {"$pull": {"courses": courseToRemove}}
            )
            return True # successfully removed course
    
    # Helper method to check if student is enrolled in a specific course
    def is_enrolled(self, courseToCheck):
        student_doc = students.find_one({"userName": self.userName})

        if courseToCheck in student_doc["courses"]:
            return True
        else:
            return False
        
    # static method to allow a student to be loaded from the STUDENTS database collection without creating new student
    @classmethod
    def load_by_username(cls, user_name):
        student_doc = students.find_one({"userName": user_name})

        if not student_doc:
            return None
        
        if student_doc["isAdmin"] is True:
            from admin import Admin
            student = Admin.__new__(Admin)
        else:
            student = cls.__new__(cls)
        
        student.firstName = student_doc["firstName"]
        student.lastName = student_doc["lastName"]
        student.userName = student_doc["userName"]
        student.isAdmin = student_doc["isAdmin"]

        return student