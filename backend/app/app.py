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

if __name__ == "__main__":
    app.run(debug=True)

    