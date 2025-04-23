from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["student_planner"]
students = db["students"]
courses = db["courses"]
degree_reqs = db["degree_requirements"]
recommendations = db["recommendations"]
faculty = db["faculty"]

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
    students.insert_one(data)
    return jsonify({"message": "Student added"})

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

    # Lookup course info
    course = courses.find_one({"_id": course_id})
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Lookup faculty teaching this course
    faculty_list = list(faculty.find({"courses_taught": course_id}, {"_id": 0, "name": 1}))
    instructor_names = [f["name"] for f in faculty_list]

    # Save course selection to student record with full detail
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

@app.route("/api/students/<student_id>/plan/<term>", methods=["GET"])
def get_planned_courses_by_term(student_id, term):
    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    planned = student.get("planned_courses", [])
    filtered = [c for c in planned if c.get("term") == term]
    return jsonify({"planned_courses": filtered})

@app.route("/api/students/<student_id>/plan/delete", methods=["POST"])
def delete_course_from_plan(student_id):
    data = request.json
    course_id = data.get("course_id")

    result = students.update_one(
        {"_id": student_id},
        {"$pull": {"planned_courses": {"course_id": course_id}}}
    )
    return jsonify({"message": "Course removed"})

@app.route("/api/students/<student_id>/plan/update", methods=["PUT"])
def update_course_term(student_id):
    data = request.json
    course_id = data.get("course_id")
    new_term = data.get("new_term")

    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    updated = False
    for course in student.get("planned_courses", []):
        if course.get("course_id") == course_id:
            course["term"] = new_term
            updated = True

    if updated:
        students.update_one(
            {"_id": student_id},
            {"$set": {"planned_courses": student["planned_courses"]}}
        )
        return jsonify({"message": "Course term updated"})
    else:
        return jsonify({"error": "Course not found in plan"}), 404

if __name__ == "__main__":
    app.run(debug=True)