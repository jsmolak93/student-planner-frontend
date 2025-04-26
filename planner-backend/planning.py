# planning.py (Refactored)

from flask import Blueprint, request, jsonify
from db import db, find_student, find_course

planning_bp = Blueprint("planning", __name__)

# Add a course to a student's plan
@planning_bp.route("/api/students/<int:ssn>/plan", methods=["POST"])
def add_course_to_plan(ssn):
    data = request.json
    dcode = data.get("dcode")
    cno = data.get("cno")

    if not dcode or not cno:
        return jsonify({"error": "dcode and cno are required"}), 400

    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    course = find_course(dcode, int(cno))
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Initialize planned_courses if not present
    if "planned_courses" not in student:
        student["planned_courses"] = []

    planned_course = {"dcode": dcode, "cno": int(cno)}

    if planned_course in student["planned_courses"]:
        return jsonify({"error": "Course already planned"}), 400

    db.student.update_one(
        {"ssn": ssn},
        {"$push": {"planned_courses": planned_course}}
    )

    return jsonify({"message": "Course added to plan!"})

# Get a student's planned courses
@planning_bp.route("/api/students/<int:ssn>/plan", methods=["GET"])
def get_planned_courses(ssn):
    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    planned_courses = student.get("planned_courses", [])
    return jsonify(planned_courses)

# Remove a course from a student's plan
@planning_bp.route("/api/students/<int:ssn>/plan/remove", methods=["POST"])
def remove_course_from_plan(ssn):
    data = request.json
    dcode = data.get("dcode")
    cno = data.get("cno")

    if not dcode or not cno:
        return jsonify({"error": "dcode and cno are required"}), 400

    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    result = db.student.update_one(
        {"ssn": ssn},
        {"$pull": {"planned_courses": {"dcode": dcode, "cno": int(cno)}}}
    )

    if result.modified_count == 0:
        return jsonify({"error": "Course not found in plan"}), 404

    return jsonify({"message": "Course removed from plan!"})
