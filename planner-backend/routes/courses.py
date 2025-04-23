from flask import Blueprint, request, jsonify
from db import courses, semesters, faculty

courses_bp = Blueprint("courses", __name__)

@courses_bp.route("/api/courses/search", methods=["POST"])
def search_course():
    data = request.json
    subject = data.get("subject")
    course_number = data.get("course_number")
    term = data.get("term", "TBD")
    course_id = f"{subject.upper()}{course_number}"

    course = courses.find_one({"_id": course_id})
    if not course:
        return jsonify({"error": "Course not found"}), 404

    semester = semesters.find_one({"_id": term})
    if not semester:
        return jsonify({"error": "Semester not found"}), 404

    if course_id not in semester.get("available_courses", []):
        return jsonify({"error": "Course not offered in this term"}), 400

    season = term.split()[0]
    if season not in course.get("offered_semesters", []):
        return jsonify({"error": "Course not available in this semester season"}), 400

    faculty_list = list(faculty.find({"courses_taught": course_id}, {"_id": 0, "name": 1}))
    instructor_names = [f["name"] for f in faculty_list]

    return jsonify({
        "course_id": course_id,
        "subject": subject,
        "course_number": course_number,
        "term": term,
        "prerequisites": course.get("prerequisites", []),
        "instructors": instructor_names,
        "credits": course.get("credits")
    })
