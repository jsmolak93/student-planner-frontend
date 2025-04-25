from flask import Blueprint, request, jsonify
from db import find_student, COLLECTIONS

students_bp = Blueprint("students", __name__)

@students_bp.route("/api/students/<int:ssn>", methods=["GET"])
def get_student(ssn):
    student, _ = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)

@students_bp.route("/api/students", methods=["POST"])
def add_student():
    data = request.json
    ssn = data.get("ssn")

    existing_student, _ = find_student(ssn)
    if existing_student:
        return jsonify({"error": "Student already exists"}), 400

    COLLECTIONS[0].update_one({}, {"$push": {"tables.student": data}})
    return jsonify({"message": "Student added successfully!"}), 201

@students_bp.route("/api/students/<int:ssn>", methods=["PUT"])
def update_student(ssn):
    updates = request.json
    _, collection = find_student(ssn)
    if not collection:
        return jsonify({"error": "Student not found"}), 404

    collection.update_one(
        {"tables.student.ssn": ssn},
        {"$set": {f"tables.student.$.{key}": value for key, value in updates.items()}}
    )
    return jsonify({"message": "Student updated successfully!"})

@students_bp.route("/api/students/<int:ssn>", methods=["DELETE"])
def delete_student(ssn):
    _, collection = find_student(ssn)
    if not collection:
        return jsonify({"error": "Student not found"}), 404

    collection.update_one({}, {"$pull": {"tables.student": {"ssn": ssn}}})
    return jsonify({"message": "Student deleted successfully!"})
