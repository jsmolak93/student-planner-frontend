from flask import Blueprint, request, jsonify
from db import students, courses, faculty, enrollments, semesters

planning_bp = Blueprint("planning", __name__)

@planning_bp.route("/api/students/<student_id>/plan", methods=["POST"])
def add_course_to_plan(student_id):
    data = request.json
    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    subject = data.get("subject")
    course_number = data.get("course_number")
    term = data.get("term", "TBD")
    course_id = f"{subject}{course_number}"

    course = courses.find_one({"_id": course_id})
    if not course:
        return jsonify({"error": "Course not found"}), 404

    faculty_list = list(faculty.find({"courses_taught": course_id}, {"_id": 0, "name": 1}))
    instructor_names = [f["name"] for f in faculty_list]

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

@planning_bp.route("/api/students/<student_id>/plan", methods=["GET"])
def get_planned_courses(student_id):
    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"planned_courses": student.get("planned_courses", [])})

@planning_bp.route("/api/students/<student_id>/plan/remove", methods=["POST"])
def remove_course_from_plan(student_id):
    data = request.json
    course_id = data.get("course_id")
    result = students.update_one(
        {"_id": student_id},
        {"$pull": {"planned_courses": {"course_id": course_id}}}
    )
    if result.modified_count == 0:
        return jsonify({"error": "Course not removed"}), 400
    return jsonify({"message": "Course removed from plan"})
