from flask import Blueprint, request, jsonify
from db import find_student, find_prereqs, find_transcripts, COLLECTIONS

analytics_bp = Blueprint("analytics", __name__)

# Query 1: Find eligible courses a student can take based on completed prerequisites
@analytics_bp.route("/api/eligible-courses/<int:ssn>", methods=["GET"])
def get_eligible_courses(ssn):
    student, _ = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    completed = {(t['dcode'], t['cno']) for t in find_transcripts(ssn) if t.get("grade") and t['grade'] not in ["F", None]}
    eligible = []

    for collection in COLLECTIONS:
        doc = collection.find_one({}, {"tables.course": 1, "tables.prereq": 1})
        if not doc or "tables" not in doc:
            continue

        courses = doc["tables"].get("course", [])
        for course in courses:
            dcode, cno = course["dcode"], course["cno"]
            prereqs = find_prereqs(dcode, cno)
            if all((p["pcode"], p["pno"]) in completed for p in prereqs):
                eligible.append(course)

    return jsonify(eligible)

# Query 2: Recommend courses needed to fulfill degree requirements
@analytics_bp.route("/api/degree-requirements/<int:ssn>", methods=["GET"])
def get_degree_requirements(ssn):
    student, _ = find_student(ssn)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    major = student.get("major")
    completed = {(t['dcode'], t['cno']) for t in find_transcripts(ssn)}
    required = set()

    for collection in COLLECTIONS:
        doc = collection.find_one({}, {"tables.course": 1})
        if not doc:
            continue
        for course in doc["tables"]["course"]:
            if course["dcode"] == major:
                key = (course["dcode"], course["cno"])
                if key not in completed:
                    required.add(key)

    results = [
        {"dcode": d, "cno": c} for (d, c) in required
    ]
    return jsonify(results)

@analytics_bp.route("/api/at-risk-students", methods=["GET"])
def get_at_risk_students():
    risk_list = []

    for collection in COLLECTIONS:
        doc = collection.find_one({}, {"tables.student": 1, "tables.transcript": 1, "tables.enrollment": 1})
        if not doc:
            continue

        students = doc["tables"].get("student", [])
        transcripts = doc["tables"].get("transcript", [])
        enrollments = doc["tables"].get("enrollment", [])

        # Calculate completed courses
        student_course_count = {}
        for t in transcripts:
            if t.get("grade") and t["grade"] not in ["F", None]:
                student_course_count[t["ssn"]] = student_course_count.get(t["ssn"], 0) + 1

        # Also check enrolled classes (current semester load)
        student_enrollment_count = {}
        for e in enrollments:
            student_enrollment_count[e["ssn"]] = student_enrollment_count.get(e["ssn"], 0) + 1

        for s in students:
            ssn = s["ssn"]
            completed = student_course_count.get(ssn, 0)
            enrolled = student_enrollment_count.get(ssn, 0)
            total_courses = completed + enrolled

            semesters = 2
            avg_courses_per_term = total_courses / semesters

            if avg_courses_per_term < 2:
                risk_list.append({
                    "ssn": ssn,
                    "name": s["name"],
                    "avg_courses_per_term": avg_courses_per_term
                })

    return jsonify(risk_list)

@analytics_bp.route("/api/course-dependency/<string:dcode>", methods=["GET"])
def get_course_dependency(dcode):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    all_courses = set()
    department_name = None

    for collection in COLLECTIONS:
        doc = collection.find_one({}, {"tables.course": 1, "tables.prereq": 1, "tables.department": 1})
        if not doc:
            continue

        for dept in doc["tables"].get("department", []):
            if dept["dcode"] == dcode:
                department_name = dept.get("dname")

      
        for prereq in doc["tables"].get("prereq", []):
            if prereq["dcode"] == dcode:
                graph[(prereq["pcode"], prereq["pno"])].append((prereq["dcode"], prereq["cno"]))
                all_courses.add((prereq["pcode"], prereq["pno"]))
                all_courses.add((prereq["dcode"], prereq["cno"]))


    in_degree = defaultdict(int)
    for prereqs in graph.values():
        for course in prereqs:
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

    return jsonify({
        "major": {"dcode": dcode, "dname": department_name},
        "course_order": [{"dcode": d, "cno": c} for d, c in order]
    })
