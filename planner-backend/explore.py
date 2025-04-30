from flask import Blueprint, jsonify
from db import db, find_student, find_transcripts, find_prereqs

explore_bp = Blueprint("explore", __name__)

@explore_bp.route("/api/explore-courses/<int:ssn>", methods=["GET"])
def explore_courses_outside_major(ssn):
    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    major = student.get("major")
    completed = {(t["dcode"], t["cno"]) for t in find_transcripts(ssn) if t.get("grade") and t["grade"] not in ["F", None]}

    all_courses = list(db.course.find())
    unique_courses = set()
    recommendations = []

    for course in all_courses:
        if course["dcode"] == major:
            continue  # Skip courses from student's major

        course_key = (course["dcode"], course["cno"])
        if course_key in completed or course_key in unique_courses:
            continue  # Skip already completed or duplicate courses

        prereqs = find_prereqs(course["dcode"], course["cno"])
        if all((p["pcode"], p["pno"]) in completed for p in prereqs):
            unique_courses.add(course_key)
            recommendations.append({
                "dcode": course["dcode"],
                "cno": course["cno"],
                "title": course["title"].replace("_", " ").title(),
                "prereq_count": len(prereqs)  # For optional sorting
            })

    # Optional: sort by fewest prerequisites, then by department
    recommendations.sort(key=lambda c: (c["prereq_count"], c["dcode"], c["cno"]))

    # Limit to top 5 recommendations
    return jsonify(recommendations[:5])
