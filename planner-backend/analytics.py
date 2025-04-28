from flask import Blueprint, request, jsonify
from collections import defaultdict, deque
from db import db, find_student, find_course, find_department, find_prereqs, find_transcripts

analytics_bp = Blueprint("analytics", __name__)

# For general course recommendations
@analytics_bp.route("/api/recommend-courses/<int:ssn>", methods=["GET"])
def recommend_courses_for_student(ssn):
    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    major = student.get("major")
    if not major:
        return jsonify({"error": "Student major not found"}), 404

    # Get all courses required for the major
    major_courses = list(db.course.find({"dcode": major}))

    # Get all courses the student already completed
    completed_courses = set()
    transcripts = find_transcripts(ssn)
    for t in transcripts:
        if t.get("grade") and t["grade"] not in ["F", None]:
            completed_courses.add((t["dcode"], t["cno"]))

    # Recommend any courses in the major not already completed
    recommended = []
    for course in major_courses:
        if (course["dcode"], course["cno"]) not in completed_courses:
            recommended.append({
                "dcode": course["dcode"],
                "cno": course["cno"],
                "title": course["title"]
            })

    return jsonify(recommended)

# ------------------------------------------------------

# Query 1: Find eligible courses a student can take based on completed prerequisites
@analytics_bp.route("/api/eligible-courses/<int:ssn>", methods=["GET"])
def get_eligible_courses(ssn):
    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    completed_courses = set()
    transcripts = find_transcripts(ssn)
    for t in transcripts:
        if t.get("grade") and t["grade"] not in ["F", None]:
            completed_courses.add((t["dcode"], t["cno"]))

    eligible_courses = []
    all_courses = list(db.course.find())

    for course in all_courses:
        course_key = (course["dcode"], course["cno"])

        # NEW: Skip if student already completed the course
        if course_key in completed_courses:
            continue

        prereqs = find_prereqs(course["dcode"], course["cno"])

        if all((p["pcode"], p["pno"]) in completed_courses for p in prereqs):
            eligible_courses.append({
                "dcode": course["dcode"],
                "cno": course["cno"],
                "title": course["title"]
            })

    return jsonify({
    "major": student.get("major"),
    "courses": eligible_courses
})


# Query 2: Recommend courses needed to fulfill degree requirements
@analytics_bp.route("/api/degree-requirements/<int:ssn>", methods=["GET"])
def recommend_degree_courses(ssn):
    student = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    major = student.get("major")
    if not major:
        return jsonify({"error": "Student major not found"}), 404

    major_courses = list(db.course.find({"dcode": major}))
    completed = {(t["dcode"], t["cno"]) for t in find_transcripts(ssn) if t.get("grade") and t["grade"] not in ["F", None]}

    recommended = []
    for course in major_courses:
        if (course["dcode"], course["cno"]) not in completed:
            recommended.append({"dcode": course["dcode"], "cno": course["cno"], "title": course["title"]})

    return jsonify(recommended)

# Query 3: List students at risk of delayed graduation
@analytics_bp.route("/api/at-risk-students", methods=["GET"])
def at_risk_students():
    risk_list = []
    students = list(db.student.find())

    for student in students:
        ssn = student["ssn"]
        transcripts = find_transcripts(ssn)

        # Count risky courses: either F or missing grade
        risk_courses = [t for t in transcripts if t.get("grade") in ["F", None]]

        if len(risk_courses) >= 1: 
            risk_list.append({
                "ssn": ssn,
                "name": student.get("name", "Unknown"),
                "major": student.get("major", "Unknown"),
                "risk_courses": len(risk_courses)
            })

    return jsonify(risk_list)


# Query 4: Show course dependency for a selected major
@analytics_bp.route("/api/course-dependency/<string:dcode>", methods=["GET"])
def get_course_dependency(dcode):
    graph = defaultdict(list)
    all_courses = set()
    department = find_department(dcode)
    department_name = department.get("dname") if department else None

    prereqs = list(db.prereq.find({"dcode": dcode}))
    for prereq in prereqs:
        graph[(prereq["pcode"], prereq["pno"])].append((prereq["dcode"], prereq["cno"]))
        all_courses.add((prereq["pcode"], prereq["pno"]))
        all_courses.add((prereq["dcode"], prereq["cno"]))

    in_degree = defaultdict(int)
    for prereqs_list in graph.values():
        for course in prereqs_list:
            in_degree[course] += 1

    queue = deque([c for c in all_courses if in_degree[c] == 0])
    order = []

    while queue:
        curr = queue.popleft()
        order.append(curr)
        for neighbor in graph[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    course_order_with_titles = []
    for d, c in order:
        course = find_course(d, c)  
        title = course["title"] if course else "Unknown"
        course_order_with_titles.append({
            "dcode": d,
            "cno": c,
            "title": title
        })

    return jsonify({
        "major": {"dcode": dcode, "dname": department_name},
        "course_order": course_order_with_titles
    })
