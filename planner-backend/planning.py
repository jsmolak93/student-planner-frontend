# planning.py (Refactored)

from flask import Blueprint, request, jsonify
from db import db, find_student, find_course

planning_bp = Blueprint("planning", __name__)

# Add a course to a student's plan
@planning_bp.route("/api/students/<int:ssn>/plan", methods=["POST"])
def add_course_to_plan(ssn):
    data = request.json
    title = data.get("title")
    cno = data.get("cno")

    if not title or not cno:
        return jsonify({"error": "title and cno are required"}), 400

    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Find matching course
    course = db.course.find_one({
        "title": title.replace(" ", "_").lower(),
        "cno": int(cno)
    })

    if not course:
        return jsonify({"error": "Course not found"}), 404

    dcode = course["dcode"]

    # Check if already planned
    existing = db.student_plan.find_one({
        "ssn": ssn,
        "dcode": dcode,
        "cno": int(cno)
    })

    if existing:
        return jsonify({"error": "Course already planned"}), 400

    # Insert into student_plan
    db.student_plan.insert_one({
        "ssn": ssn,
        "dcode": dcode,
        "cno": int(cno)
    })

    return jsonify({"message": "Course added to plan!"})



# Get a student's planned courses
@planning_bp.route("/api/students/<int:ssn>/plan", methods=["GET"])
def get_planned_courses(ssn):
    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    planned_raw = list(db.student_plan.find({"ssn": ssn}))
    
    detailed_courses = []
    for item in planned_raw:
        course = find_course(item["dcode"], item["cno"])
        if course:
            detailed_courses.append({
                "dcode": item["dcode"],
                "cno": item["cno"],
                "title": course.get("title", "Unknown Title")
            })

    return jsonify(detailed_courses)


# Remove a course from a student's plan
@planning_bp.route("/api/students/<int:ssn>/plan/remove", methods=["POST"])
def remove_course_from_plan(ssn):
    data = request.json
    dcode = data.get("dcode")
    cno = data.get("cno")

    if not dcode or not cno:
        return jsonify({"error": "dcode and cno are required"}), 400

    result = db.student_plan.delete_one({
        "ssn": ssn,
        "dcode": dcode,
        "cno": int(cno)
    })

    if result.deleted_count == 0:
        return jsonify({"error": "Course not found in plan"}), 404

    return jsonify({"message": "Course removed from plan!"})
