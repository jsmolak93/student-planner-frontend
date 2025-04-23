from ml_utils import predict_top_courses
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

    # Add default empty lists if not provided
    data.setdefault("completed_courses", [])
    data.setdefault("current_courses", [])

    students.insert_one(data)
    return jsonify({"message": "Student added"})


@app.route("/api/students/<student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    students.update_one({"_id": student_id}, {"$set": data})
    return jsonify({"message": "Student updated"})

@app.route("/api/ml/recommend-courses/<student_id>")
def ml_recommend_courses(student_id):
    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    gpa = student.get("gpa", 0)
    completed = len(student.get("completed_courses", []))

    # Map major to numeric code for your model
    major_map = {"Computer Science": 0, "Operations Research": 1}
    major_code = major_map.get(student.get("major", ""), -1)
    if major_code == -1:
        return jsonify({"error": "Unknown major"}), 400

    recommendations = predict_top_courses(gpa, completed, major_code)
    return jsonify({"recommended_courses": recommendations})

if __name__ == "__main__":
    app.run(debug=True)
