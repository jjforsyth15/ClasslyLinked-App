#import modules & MongoDB
from student import Student
from course import Course
from pymongo import MongoClient
import bcrypt
from TestAdmin import admin_dashboard

#Set up MongoDB for use
uri = "mongodb+srv://jjforsyth15:ClasslyLinked2025@classlylinked.bxbv8wy.mongodb.net/"
client = MongoClient(uri)

db = client["CLASSLYLINKED"]
students = db["STUDENTS"]
courses = db["COURSES"]

# SignUpTest
def SignUpTest(): 

    while True:
        print("=== Menu ===")
        print("1. Sign Up\n2. Login\n3. End Program")
        
        choice = input("Choose an option: ")
        
        # if user chooses 1 to sign up
        if choice == "1":
            print("Signing Up\n-------")
            # asks for new login information
            first_name = input("Enter first name: ")   
            last_name = input("Enter last name: ")
            user_name = input("Enter a username: ")

            # checks if username is already in use
            while True:
                if(students.find_one({"userName": user_name})):
                    user_name = input("Username already exists. Enter another username: ")
                else:
                    break

            # asks user to make a password
            password = input("Enter a password:")

            # creates new student to add to database with new login information
            new_student = Student(first_name, last_name, user_name, password)
            print("New student login created: ",
                  students.find_one({"userName": user_name})["userName"])
            print("Log in to access account")
            
        # if user chooses 2 to log in
        elif choice == "2": 
            print("Logging in\n-------")

            # asks for username, makes sure usernames exists
            user_name = input("Enter username: ")
            while True:
                if not (students.find_one({"userName": user_name})):
                    user_name = input("Username does not exist. Enter again: ")
                else:
                    break

            # accesses user password
            user = students.find_one({"userName": user_name})
            stored_hash = user["passwordHashed"]
            
            # asks for password
            password = input("Enter password: ")
            
            # makes sure password is correct
            while True: 
                if bcrypt.checkpw(password.encode(), stored_hash):
                    print("Login successful. Welcome, ", students.find_one({"userName": user_name},
                                                                        {"firstName": 1, "_id": 0})["firstName"])
                   
                    if user.get("isAdmin", False):
                        admin_dashboard(user_name)
                        break
                    else:
                        break
                else:
                    password = input("Incorrect password try again: ")

        # if user chooses 3 to end program
        elif choice == "3":
            print("Ending Program.")
            break
        
        # if user enters something that is not a listed option
        else:
            print("Invalid input. Try again.")


        
SignUpTest()

