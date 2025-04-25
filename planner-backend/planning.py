from flask import Blueprint, request, jsonify
from db import find_student, find_course, COLLECTIONS

planning_bp = Blueprint("planning", __name__)

# Add a course to a student's plan
@planning_bp.route("/api/students/<int:ssn>/plan", methods=["POST"])
def add_course_to_plan(ssn):
    data = request.json
    dcode = data.get("dcode")
    cno = data.get("cno")

    if not dcode or not cno:
        return jsonify({"error": "dcode and cno are required"}), 400

    student, student_db = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    course, _ = find_course(dcode, int(cno))
    if not course:
        return jsonify({"error": "Course not found"}), 404

    planned_course = {"dcode": dcode, "cno": int(cno)}
    existing_plan = student.get("planned_courses", [])

    if planned_course in existing_plan:
        return jsonify({"error": "Course already planned"}), 400

    student_db.update_one(
        {"tables.student.ssn": ssn},
        {"$push": {"tables.student.$.planned_courses": planned_course}}
    )

    return jsonify({"message": "Course added to plan!"})

# Get planned courses for a student
@planning_bp.route("/api/students/<int:ssn>/plan", methods=["GET"])
def get_planned_courses(ssn):
    student, _ = find_student(ssn)
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

    for collection in COLLECTIONS:
        result = collection.update_one(
            {},
            {"$pull": {"tables.student.$[student].planned_courses": {"dcode": dcode, "cno": int(cno)}}},
            array_filters=[{"student.ssn": ssn}]
        )
        if result.modified_count > 0:
            return jsonify({"message": "Course removed from plan!"})

    return jsonify({"error": "Course not found in plan"}), 404
