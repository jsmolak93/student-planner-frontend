from flask import Blueprint, jsonify
from ..db import students, courses, degree_reqs

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics/eligible-courses/<student_id>', methods=['GET'])
def get_eligible_courses(student_id):
    student = students.find_one({"_id": student_id})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    completed = set(student.get("completed_courses", []))
    eligible = []

    for course in courses.find():
        prereqs = set(course.get("prerequisites", []))
        if prereqs.issubset(completed):
            eligible.append(course["_id"])

    return jsonify({"eligible_courses": eligible})


@analytics_bp.route('/api/analytics/degree-gaps/<student_id>', methods=['GET'])
def get_degree_gaps(student_id):
    student = students.find_one({"_id": student_id})
    completed = set(student.get("completed_courses", []))
    major = student.get("major")

    degree = degree_reqs.find_one({"_id": major})
    if not degree:
        return jsonify({"error": "Degree requirements not found"}), 404

    needed_core = [c for c in degree["core_courses"] if c not in completed]
    needed_electives = [e for e in degree["electives"] if e not in completed]

    return jsonify({
        "needed_core": needed_core,
        "needed_electives": needed_electives
    })


@analytics_bp.route('/api/analytics/at-risk-students', methods=['GET'])
def get_at_risk_students():
    result = []
    for student in students.find():
        completed = student.get("completed_courses", [])
        gpa = student.get("gpa", 0)
        major = student.get("major")

        degree = degree_reqs.find_one({"_id": major})
        total_required = degree.get("total_credits_required", 0)
        earned = sum(courses.find_one({"_id": cid}).get("credits", 0) for cid in completed)

        if gpa < 2.5 or earned < 0.6 * total_required:
            result.append({
                "id": student["_id"],
                "name": student["name"],
                "gpa": gpa
            })

    return jsonify({"at_risk_students": result})
