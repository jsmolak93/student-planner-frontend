# students.py (Refactored)

from flask import Blueprint, request, jsonify
from db import db, find_student

students_bp = Blueprint("students", __name__)

# Get a student
@students_bp.route("/api/students/<int:ssn>", methods=["GET"])
def get_student(ssn):
    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student["_id"] = str(student["_id"])  # Make ObjectId JSON serializable
    return jsonify(student)


# Add a new student
@students_bp.route("/api/students", methods=["POST"])
def add_student():
    data = request.json
    ssn = data.get("ssn")

    existing_student = find_student(ssn)
    if existing_student:
        return jsonify({"error": "Student already exists"}), 400

    db.student.insert_one(data)
    return jsonify({"message": "Student added successfully!"})

# Update a student's info
@students_bp.route("/api/students/<int:ssn>", methods=["PUT"])
def update_student(ssn):
    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    updates = request.json
    db.student.update_one({"ssn": ssn}, {"$set": updates})

    return jsonify({"message": "Student updated successfully!"})

# Delete a student
@students_bp.route("/api/students/<int:ssn>", methods=["DELETE"])
def delete_student(ssn):
    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    db.student.delete_one({"ssn": ssn})
    return jsonify({"message": "Student deleted successfully!"})
