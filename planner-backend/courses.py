# courses.py (Refactored)

from flask import Blueprint, request, jsonify
from db import db, find_course

courses_bp = Blueprint("courses", __name__)

# Get a course by dcode and cno
@courses_bp.route("/api/courses/<string:dcode>/<int:cno>", methods=["GET"])
def get_course(dcode, cno):
    course = find_course(dcode, cno)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    course["_id"] = str(course["_id"])  # Make ObjectId JSON serializable
    return jsonify(course)

# Get all courses
@courses_bp.route("/api/courses", methods=["GET"])
def get_all_courses():
    courses = list(db.course.find())
    for course in courses:
        course["_id"] = str(course["_id"])  # Make ObjectId JSON serializable
    return jsonify(courses)

# Add a new course
@courses_bp.route("/api/courses", methods=["POST"])
def add_course():
    data = request.json
    dcode = data.get("dcode")
    cno = data.get("cno")

    existing_course = find_course(dcode, cno)
    if existing_course:
        return jsonify({"error": "Course already exists"}), 400

    db.course.insert_one(data)
    return jsonify({"message": "Course added successfully!"})

# Update a course
@courses_bp.route("/api/courses/<string:dcode>/<int:cno>", methods=["PUT"])
def update_course(dcode, cno):
    course = find_course(dcode, cno)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    updates = request.json
    db.course.update_one({"dcode": dcode, "cno": cno}, {"$set": updates})
    return jsonify({"message": "Course updated successfully!"})

# Delete a course
@courses_bp.route("/api/courses/<string:dcode>/<int:cno>", methods=["DELETE"])
def delete_course(dcode, cno):
    course = find_course(dcode, cno)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    db.course.delete_one({"dcode": dcode, "cno": cno})
    return jsonify({"message": "Course deleted successfully!"})
