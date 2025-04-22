from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Allow Vue frontend to connect

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["student_planner"]
students = db["students"]
courses = db["courses"]
degree_reqs = db["degree_requirements"]
recommendations = db["recommendations"]

@app.route("/api/students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    student["_id"] = str(student["_id"])  # ensure ID is JSON-serializable
    return jsonify(student)

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json
    students.insert_one(data)
    return jsonify({"message": "Student added"})

@app.route("/api/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    students.update_one({"_id": student_id}, {"$set": data})
    return jsonify({"message": "Student updated"})

@app.route("/api/recommendations/<student_id>", methods=["GET"])
def get_recommendations(student_id):
    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    major = student.get("major")
    completed = set(student.get("completed_courses", []))

    degree = degree_reqs.find_one({"degree_name": {"$regex": major, "$options": "i"}})
    if not degree:
        return jsonify({"recommended_courses": []})

    all_courses = set(degree.get("core_courses", []) + degree.get("electives", []))
    missing_courses = all_courses - completed

    eligible_courses = []
    for course_id in missing_courses:
        course = courses.find_one({"_id": course_id})
        if not course:
            continue
        prereqs = course.get("prerequisites", [])
        if all(pr in completed for pr in prereqs):
            eligible_courses.append(course_id)

    return jsonify({"recommended_courses": eligible_courses})

if __name__ == "__main__":
    app.run(debug=True)
