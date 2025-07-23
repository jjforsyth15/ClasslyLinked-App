from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from student import Student
import bcrypt 

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://jjforsyth15:ClassLink2025@cluster1.imnisby.mongodb.net/")
db = client["CLASSLINK"]
students = db["STUDENTS"]

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
    

if __name__ == "__main__":
    app.run(debug=True)

    