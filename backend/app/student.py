from pymongo import MongoClient
import bcrypt

uri = "mongodb+srv://jjforsyth15:ClassLink2025@cluster1.imnisby.mongodb.net/"
client = MongoClient(uri)

db = client["CLASSLINK"]
students = db["STUDENTS"]
courses = db["COURSES"]

class Student: 
    # constructor for Student class. Takes in first name, last name, username, and password
    def __init__(self, first, last, username, password):
        self.firstName = first
        self.lastName = last
        # self.myCourses = course if courses is not None else []  -- will add later
        self.userName = username

        #hashes passworf
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
                # "courses": course
            })

    # how Student is displayed -- will need to update to look better
    def __str__(self):
        return f"Student: {self.firstName} {self.lastName}, Courses: {', '.join(self.myCoursesourses)}"
    
    # def to_dict(self):
    #     return {
    #         "firstName": self.firstName,
    #         "lastName": self.lastName,
    #         "courses": self.myCourses
    #     }
    
    # method to add a course to Student
    def add_course(self, courseToAdd):
        from course import Course   
        self.myCourses.append(courseToAdd)
        result = students.update_one(
            {"firstName": self.firstName, "lastName": self.lastName},
            {"$push": {"courses": courseToAdd}}
        )
        print("Added course: ")
        print(courseToAdd)


    # method to remove a course from Student
    # def remove_course(self, courseToRemove):
    #     from course import Course
    #     #need to complete

