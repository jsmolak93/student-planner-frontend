from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["student_planner"]
students = db["students"]
courses = db["courses"]
degree_reqs = db["degree_requirements"]
faculty = db["faculty"]
enrollments = db["enrollments"]
semesters = db["semesters"]
recommendations = db["recommendations"]

@app.route("/api/students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    student["_id"] = str(student["_id"])
    return jsonify(student)

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json
    data.setdefault("planned_courses", [])
    try:
        students.insert_one(data)
        return jsonify({"message": "Student added"})
    except DuplicateKeyError:
        return jsonify({"error": "Student ID already exists"}), 400

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json
    data.setdefault("planned_courses", [])
    students.insert_one(data)
    return jsonify({"message": "Student added"})

@app.route("/api/courses/search", methods=["POST"])
def search_course():
    data = request.json
    subject = data.get("subject")
    course_number = data.get("course_number")
    term = data.get("term", "TBD")
    course_id = f"{subject.upper()}{course_number}"

    # Look up course
    course = courses.find_one({"_id": course_id})
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Look up semester (term)
    semester = semesters.find_one({"_id": term})
    if not semester:
        return jsonify({"error": "Semester not found"}), 404

    # Check if course is available in that term
    if course_id not in semester.get("available_courses", []):
        return jsonify({"error": "Course not offered in this term"}), 400

    # Check if season matches (e.g., "Spring" in "Spring 2026")
    season = term.split()[0]
    if season not in course.get("offered_semesters", []):
        return jsonify({"error": "Course not available in this semester season"}), 400

    # Look up faculty for the course
    faculty_list = list(faculty.find({"courses_taught": course_id}, {"_id": 0, "name": 1}))
    instructor_names = [f["name"] for f in faculty_list]

    course_info = {
        "course_id": course_id,
        "subject": subject,
        "course_number": course_number,
        "term": term,
        "prerequisites": course.get("prerequisites", []),
        "instructors": instructor_names,
        "credits": course.get("credits")
    }

    return jsonify(course_info)


@app.route("/api/enrollments/count/<course_id>/<term>", methods=["GET"])
def get_enrollment_count(course_id, term):
    count = enrollments.count_documents({"course_id": course_id, "semester": term})
    return jsonify({"count": count})

@app.route("/api/semesters/<term>", methods=["GET"])
def get_semester_dates(term):
    semester = semesters.find_one({"_id": term})
    if not semester:
        return jsonify({"error": "Semester not found"}), 404
    return jsonify({
        "start_date": semester.get("start_date"),
        "end_date": semester.get("end_date")
    })

@app.route("/api/students/<student_id>/plan", methods=["POST"])
def add_course_to_plan(student_id):
    data = request.json
    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    subject = data.get("subject")
    course_number = data.get("course_number")
    term = data.get("term", "TBD")
    course_id = f"{subject}{course_number}"

    course = courses.find_one({"_id": course_id})
    if not course:
        return jsonify({"error": "Course not found"}), 404

    faculty_list = list(faculty.find({"courses_taught": course_id}, {"_id": 0, "name": 1}))
    instructor_names = [f["name"] for f in faculty_list]

    planned_entry = {
        "course_id": course_id,
        "subject": subject,
        "course_number": course_number,
        "term": term,
        "prerequisites": course.get("prerequisites", []),
        "instructors": instructor_names,
        "credits": course.get("credits")
    }

    students.update_one(
        {"_id": student_id},
        {"$addToSet": {"planned_courses": planned_entry}}
    )

    return jsonify(planned_entry)

@app.route("/api/students/<student_id>/plan", methods=["GET"])
def get_planned_courses(student_id):
    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"planned_courses": student.get("planned_courses", [])})

@app.route("/api/students/<student_id>/plan/remove", methods=["POST"])
def remove_course_from_plan(student_id):
    data = request.json
    course_id = data.get("course_id")

    result = students.update_one(
        {"_id": student_id},
        {"$pull": {"planned_courses": {"course_id": course_id}}}
    )

    if result.modified_count == 0:
        return jsonify({"error": "Course not removed"}), 400

    return jsonify({"message": "Course removed from plan"})
























##--------- Queries------------------##
def get_eligible_courses(student_id):
    student = students.find_one({ "_id": student_id })
    completed = set(student.get("completed_courses", []))

    eligible_courses = []
    for course in courses.find():
        prereqs = set(course.get("prerequisites", []))
        if prereqs.issubset(completed):
            eligible_courses.append(course["_id"])

    return eligible_courses


def get_degree_gaps(student_id):
    student = students.find_one({ "_id": student_id })
    completed = set(student.get("completed_courses", []))

    degree = degree_reqs.find_one({ "_id": student["major"] })
    core_needed = [c for c in degree["core_courses"] if c not in completed]
    electives_needed = [e for e in degree["electives"] if e not in completed]

    return {
        "needed_core": core_needed,
        "needed_electives": electives_needed
    }


def get_at_risk_students():
    risk_list = []
    for student in students.find():
        completed = student.get("completed_courses", [])
        gpa = student.get("gpa", 0)
        major = student.get("major")
        degree = degree_reqs.find_one({ "_id": major })

        total_credits = sum(courses.find_one({ "_id": cid })["credits"] for cid in completed)
        if total_credits < 0.6 * degree["total_credits_required"] or gpa < 2.5:
            risk_list.append({
                "id": student["_id"],
                "name": student["name"],
                "gpa": gpa
            })

    return risk_list

def get_course_order(major):
    degree = degree_reqs.find_one({ "_id": major })
    relevant = degree["core_courses"] + degree["electives"]
    
    graph = { course: set() for course in relevant }
    for course in relevant:
        prereqs = courses.find_one({ "_id": course }).get("prerequisites", [])
        graph[course] = set(prereqs)

    return topological_sort(graph)

if __name__ == "__main__":
    app.run(debug=True)
