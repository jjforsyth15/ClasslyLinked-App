from pymongo import MongoClient

client = MongoClient("mongodb+srv://jjforsyth15:ClasslyLinked2025@classlylinked.bxbv8wy.mongodb.net/")
db = client["CLASSLYLINKED"]
students = db["STUDENTS"]
courses = db["COURSES"]

def getMatches(student_user, top_n = 7):

    me = students.find_one({"userName": student_user})

    if not me:
        print("Could not find user from userName.")
        return []
    
    my_courses = set(me.get("courses"))
    if not my_courses:
        return []
    
    name_map = {
        d["courseNumber"]: f'{d.get("courseName", "")} ({d["courseNumber"]})'

        for d in courses.find( 
            {"courseNumber": {"$in": list(my_courses)}},
            {"courseName": 1, "courseNumber": 1, "_id": 0}
        )
    }

    cursor = students.find(
        {
            "userName": {"$ne": student_user},
            "courses": {"$in": list(my_courses)},
        },
        {"firstName": 1, "lastName": 1, "userName": 1, "courses": 1}
    )

    matches = []
    totals_by_user = {}

    for cand in cursor:
        cand_courses = set(cand.get("courses") or [])
        common = list(my_courses & cand_courses)
        common_count = len(common)

        if common:
            common_pretty = [name_map.get(c, str(c)) for c in common]
            matches.append({
                "firstName": cand.get("firstName", ""),
                "lastName": cand.get("lastName", ""),
                "userName": cand.get("userName", ""),
                "commonCourses": common,
                "commonCount": common_count,
            })
        
        totals_by_user[cand.get("userName", "")] = common_count

    return matches#, totals_by_user
    

