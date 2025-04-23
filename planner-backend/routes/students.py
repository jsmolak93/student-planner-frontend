from flask import Blueprint, request, jsonify
from pymongo.errors import DuplicateKeyError
from db import students

students_bp = Blueprint("students", __name__)

@students_bp.route("/api/students/<student_id>", methods=["GET"])
def get_student(student_id):
    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    student["_id"] = str(student["_id"])
    return jsonify(student)

@students_bp.route("/api/students", methods=["POST"])
def add_student():
    data = request.json
    data.setdefault("planned_courses", [])
    try:
        students.insert_one(data)
        return jsonify({"message": "Student added"})
    except DuplicateKeyError:
        return jsonify({"error": "Student ID already exists"}), 400
