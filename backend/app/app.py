from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from student import Student
from admin import Admin
from course import Course
import bcrypt 

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://jjforsyth15:ClasslyLinked2025@classlylinked.bxbv8wy.mongodb.net/")
db = client["CLASSLYLINKED"]
students = db["STUDENTS"]
courses = db["COURSES"]

@app.route("/signup", methods=["POST"])
def signUp():
    data = request.json

    first = data.get("firstName")
    last = data.get("lastName")
    user = data.get("userName") 
    password = data.get("password") 

    if not all([first, last, user, password]):
        return jsonify({"message": "Missing field(s)"}), 400
    if students.find_one({"userName": user}):
        return jsonify({"message": "Username already exists"}), 409

    new_student = Student(first, last, user, password)

    return jsonify({"message": "Student log in created successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = data.get("userName")
    password = data.get("password")

    if not user:
        return jsonify({"message": "Username is required"}), 400
    elif not students.find_one({"userName": user}):
        return jsonify({"message": "Username not found"}), 404
    user = students.find_one({"userName": user})
    
    if bcrypt.checkpw(password.encode(), user["passwordHashed"]):
        return jsonify({"message": "Login successful. Welcome, ", "firstName": user["firstName"]}), 200
    else:
        return jsonify({"message": "Incorrect password"}), 401
    

@app.route("/create_course", methods=["POST"])
def create_course():
    data = request.json

    course_name = data.get("courseName")
    course_number = data.get("courseNumber")
    username = data.get("userName")
    password = data.get("password")

    if not course_name:
        return jsonify({"error": "Missing courseName"}), 400
    if not course_number:
        return jsonify({"error": "Missing courseNumber"}), 400
    if not username:
        return jsonify({"error": "Missing username"}), 400
    if not password:
        return jsonify({"error": "Missing password"}), 400
    
    user = students.find_one({"userName": username})

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    hashed = user["passwordHashed"]
    
    if not bcrypt.checkpw(password.encode(), hashed):
        return jsonify({"error": "Incorrect password"}), 401
    
    if not user["isAdmin"]:
        return jsonify({"error": "User not admin. Page only accessible to admin users"}), 403

    if courses.find_one({"courseNumber": course_number}):
        return jsonify({"error": "Course already exists"}), 409
    
    Course(course_name, course_number)
    return jsonify({"message": "Course created successfully"}), 201

@app.route("/add_course", methods=["POST"]) 
def add_course():
    data = request.json

    username = data.get("userName")
    courseNum = data.get("course")

    if not username:
        return jsonify({"error": "Missing username"}), 400
    if not courseNum:
        return jsonify({"error": "Missing course number"}), 400
    
    student = Student.load_by_username(username)
    course = Course.load_by_number(courseNum)

    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    if students.find_one({"userName": username, "courses.courseNumber": courseNum}):
        return jsonify({"error": "Student is already added to course"}), 409
    
    student.add_course(courseNum)
    course.AddStudent(username)
    
    return jsonify({"message": "Course added successfully"}), 200


@app.route("/remove_course", methods=["POST"])
def remove_course():
    data = request.json

    username = data.get("userName")
    courseNum = data.get("courseNumber")

    if not username:
        return jsonify({"error": "Missing username"}), 400
    if not courseNum:
        return jsonify({"error": "Missing course number"}), 400
    
    student = Student.load_by_username(username)
    course = Course.load_by_number(courseNum)

    if not student:
        return jsonify({"error": "Student not found"}), 404
    if not course:
        return jsonify({"error": "Course not found"}), 404
    
    if not students.find_one({"userName": username, "courses.courseNumber": courseNum}):
        return jsonify({"error": "Student is not already in course"}), 409
    
    student.remove_course(courseNum)
    course.RemoveStudent(username)

    return jsonify({"message": "Student removed from course successfully"}), 200

@app.route("/promote_to_admin", methods=["POST"])
def promote_to_admin():
    data = request.json

    username = data.get("userName")
    adminUser = data.get("adminUser")

    if not username:
        return jsonify({"error": "Missing username"}), 400
    if not adminUser:
        return jsonify({"error": "Missing admin"}), 400
    
    student = Student.load_by_username(username)
    admin = Admin.load_by_username(adminUser)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    if not admin:
        return jsonify({"error": "Admin not found"}), 404
    
    if not students.find_one({"userName": adminUser, "isAdmin": True}):
        return jsonify({"error": "Admin user does not have admin authorization"}), 409
    
    if students.find_one({"userName": username, "isAdmin": True}):
        return jsonify({"error": "Student is already admin"}), 409

    promoted = admin.PromoteToAdmin(username)

    if not promoted:
        return jsonify({"error": "Error occured, could not promote student to admin"}), 409
    else:
        return jsonify({"message": "Student promoted to admin successfully"}), 200
    
@app.route("/get_courses", methods=["GET"])
def get_courses():
    
    username = request.args.get("userName")

    if not username:
        return jsonify({"error": "Missing username"}), 400
    
    student = students.find_one({"userName": username})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    return jsonify({"courses": student.get("courses", [])})

if __name__ == "__main__":
    app.run(debug=True)

    