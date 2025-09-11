from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from student import Student
from admin import Admin
from course import Course
from MatchEngine import getMatches
from mateRequest import mateRequest
import bcrypt 

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://jjforsyth15:ClasslyLinked2025@classlylinked.bxbv8wy.mongodb.net/")
db = client["CLASSLYLINKED"]
students = db["STUDENTS"]
courses = db["COURSES"]
mateRequests = db["MATE_REQUESTS"]

# Route function for signing up
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

# Route function for logging in
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
        return jsonify({"message": "Login successful. Welcome, ", 
                        "firstName": user["firstName"],
                        "isAdmin": user.get("isAdmin", False)
                        }), 200
    else:
        return jsonify({"message": "Incorrect password"}), 401
    
# Route function for creating a new course - for admin use only
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

# Route function to add a course - for all student use
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
    
    if students.find_one({"userName": username, "courses": courseNum}):
        return jsonify({"error": "Student is already added to course"}), 409
    
    student.add_course(courseNum)
    course.AddStudent(username)
    
    return jsonify({"message": "Course added successfully"}), 200

# Route function to remove a course - for all student use
@app.route("/remove_course", methods=["POST"])
def remove_course():
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
    
    if not students.find_one({"userName": username, "courses": courseNum}):
        return jsonify({"error": "Student is not already in course"}), 409
    
    student.remove_course(courseNum)
    course.RemoveStudent(username)

    return jsonify({"message": "Student removed from course successfully"}), 200

# Route function to promote student user to admin user - for admin use only
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

# Route fuunction for React front end to request a user's courses
@app.route("/get_courses", methods=["GET"])
def get_courses():
    
    username = request.args.get("userName")

    if not username:
        return jsonify({"error": "Missing username"}), 400
    
    student = students.find_one({"userName": username})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    courseNums = student.get("courses", [])
    courseDetails = []

    for number in courseNums:
        course = courses.find_one({"courseNumber": number})
        if course:
            courseDetails.append({
                "courseName": course["courseName"],
                "courseNumber": course["courseNumber"]
            })
    
    return jsonify({"courses": courseDetails}), 200

# Route function to search courses
@app.route("/search_courses", methods=["GET"])
def search_courses():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"courses": []})
    
    results = courses.find({
        "$or": [
            {"courseNumber": {"$regex": query, "$options": "i"}},
            {"courseName": {"$regex": query, "$options": "i"}}
        ]
    })
    courseList = []
    for course in results:
        courseList.append({
            "courseName": course["courseName"],
            "courseNumber": course["courseNumber"]
        })

    return jsonify({"courses": courseList}), 200

# Route function to search a student's courses
@app.route("/search_student_courses", methods=["GET"])
def search_student_courses():
    query = request.args.get("q", "").strip()
    username = request.args.get("username").strip()

    if not query:
        return jsonify({"courses": []})

    if not username:
        return jsonify({"error": "Missing username"}), 400
    
    student = students.find_one({"userName": username})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    student_courses = student.get("courses", [])

    if not student_courses:
        return jsonify({"courses": []})
    
    course_query = {
        "$and": [
            {"courseNumber": {"$in": student_courses}},
            {
                "$or": [
                    {"courseNumber": {"$regex": query, "$options": "i"}},
                    {"courseName": {"$regex": query, "$options": "i"}}
                ]
            } 
        ]
    }
    results = courses.find(course_query)

    course_list = []

    for course in results:
        course_list.append({
            "courseName": course["courseName"],
            "courseNumber": course["courseNumber"]
        })
    
    return jsonify({"courses": course_list}), 200


@app.route("/get_user_matches", methods=["GET"])
def get_user_matches():
    user = request.args.get("userName")
    if not user:
        return jsonify({"message": "userName query-param required"}), 400
    
    student_id = students.find_one({"userName": user})
    if not student_id:
        return jsonify({"error": "userName not found"}), 404
    
    user_matches = getMatches(user)

    all_nums = {str(c) for m in user_matches for c in (m.get("commonCourses") or [])}
    name_map = {
        d["courseNumber"]: f'{d.get("courseName", "")} ({d["courseNumber"]})'
        for d in courses.find(
            {"courseNumber": {"$in": list(all_nums)}},
            {"courseName": 1, "courseNumber": 1, "_id": 0}
        )
    }

    for m in user_matches:
        m["firstName"] = m.get("firstName", "") or ""
        m["lastName"] = m.get("lastName", "") or ""
        m["userName"] = m.get("userName", "") or ""
        m["commonCount"] = int(m.get("commonCount", 0) or 0)
        m["commonCourses"] = [name_map.get(str(c), str(c)) for c in (m.get("commonCourses") or [])]

    results = {
        "numMatches": len(user_matches),
        "matches": user_matches
    }

    return jsonify(results), 200
    
# classMate request app routes
def verify_users(self, sender, receiver):
    if not sender:
        return jsonify({"message": "Sender userName is required"}), 400
    elif not receiver:
        return jsonify({"message": "Receiver userName is required"}), 400

    if not students.find_one({"userName": sender}):
        return jsonify({"message": "Sender userName not found"}), 404
    elif not students.find_one({"userName": receiver}):
        return jsonify({"message": "Receiver userName not found"}), 404
    
    return True


@app.route("/send_mate_request", methods=["POST"])
def send_mate_request():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")

    if verify_users(sender, receiver) is not True:
        return jsonify({"message": "sender and receiver userNames culd not be verified"}), 400
    
    mate = mateRequest(sender, receiver)

    return jsonify({"message": "classMate request sent successfully"}), 200


@app.route("/accept_mate_request", methods=["POST"])
def accept_mate_request():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")

    if verify_users(sender, receiver) is not True:
        return jsonify({"message": "sender and receiver userNames culd not be verified"}), 400
    
    mate = mateRequest.load_request(sender, receiver)
    if mate is None:
        return jsonify({"message": "Could not find classMate request"}), 404
    mate = mate.accept_request(sender, receiver)

    if mate is not True:
        return jsonify({"message": "Could not accept classMate request"}), 401
    
    return jsonify({"message": "classMate request accepted successfully"}), 200

@app.route("/decline_mate_request", methods=["POST"])
def decline_mate_request():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")

    if verify_users(sender, receiver) is not True:
        return jsonify({"message": "Could not verify usernames"}), 400
    
    mate = mateRequest.load_request(sender, receiver)
    if mate is None:
        return jsonify({"message": "Could not find classMate request"}), 404
    
    mate = mate.decline_request(sender, receiver)

    if mate is not True:
        return jsonify({"message": "Could not decline classMate request"}), 401
    
    return jsonify({"message": "classMate request declined successfully"}), 200

@app.route("/cancel_mate_request", methods=["POST"])
def cancel_mate_request():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")

    if verify_users(sender, receiver) is not True:
        return jsonify({"message": "Could not verify usernames"}), 400
    
    mate = mateRequest.load_request(sender, receiver)
    if mate is None:
        return jsonify({"message": "Could not find classMate request"}), 404
    
    mate = mate.cancel_request(sender, receiver)

    if mate is not True:
        return jsonify({"message": "Could not cancel classMate request"}), 401
    
    return jsonify({"message": "classMate request canceled successfully"}), 200
    



if __name__ == "__main__":
    app.run(debug=True)

    