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
        enrollments = list(db.enrollment.find({"ssn": ssn})) 

        # Risky if they have any F or null grades
        risk_courses = [t for t in transcripts if t.get("grade") in ["F", None]]

        # Extra risk: if not currently enrolled in any class
        currently_enrolled = len(enrollments) == 0

        if len(risk_courses) >= 1 or currently_enrolled:
            risk_list.append({
                "ssn": ssn,
                "name": student.get("name", "Unknown"),
                "major": student.get("major", "Unknown"),
                "risk_courses": len(risk_courses),
                "currently_enrolled": not currently_enrolled 
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

# Query 5: Instructor Workload Analysis (Courses Taught by Each Instructor)
@analytics_bp.route("/api/instructor-workload", methods=["GET"])
def instructor_course_load():
    classes = list(db["class"].find())
    faculty = {f["ssn"]: f["name"] for f in db.faculty.find()}
    course_map = {(c["dcode"], c["cno"]): c["title"] for c in db.course.find()}

    instructor_data = defaultdict(lambda: {"courses": [], "courses_taught": 0})

    for cls in classes:
        instr_ssn = cls.get("instr")
        course_title = course_map.get((cls["dcode"], cls["cno"]), "Unknown Course")
        if instr_ssn is not None:
            instructor_data[instr_ssn]["courses"].append(course_title)
            instructor_data[instr_ssn]["courses_taught"] += 1

    result = [
        {
            "name": faculty.get(ssn, f"Instructor {ssn}"),
            "courses_taught": data["courses_taught"],
            "courses": data["courses"]
        }
        for ssn, data in instructor_data.items()
    ]

    return jsonify(result)



# Query 6: Units Taken Per Student (Completed Courses Only)
@analytics_bp.route("/api/student-units", methods=["GET"])
def student_units():
    students = {s["ssn"]: s["name"] for s in db.student.find()}
    transcripts = list(db.transcript.find())
    courses = {(c["dcode"], c["cno"]): c.get("units", 0) for c in db.course.find()}

    units_by_student = defaultdict(int)

    for t in transcripts:
        if t.get("grade") not in ["F", None]:
            key = (t["dcode"], t["cno"])
            units = courses.get(key, 0)
            units_by_student[t["ssn"]] += units

    result = [
        {
            "name": students.get(ssn, f"Student {ssn}"),
            "ssn": ssn,
            "units": units
        }
        for ssn, units in units_by_student.items()
    ]

    return jsonify(result)


#------------------------------------------------------------------------------#

# --- Students per Major Chart ---
@analytics_bp.route("/api/charts/students-by-major", methods=["GET"])
def students_by_major():
    students = list(db.student.find())
    departments = {d["dcode"]: d["dname"] for d in db.department.find()}
    
    counts = {}
    for student in students:
        major_code = student.get("major")
        major_name = departments.get(major_code, major_code)
        counts[major_name] = counts.get(major_name, 0) + 1

    return jsonify(counts)

# --- Courses per Department Chart ---
@analytics_bp.route("/api/charts/courses-by-department", methods=["GET"])
def courses_by_department():
    courses = list(db.course.find())
    departments = {d["dcode"]: d["dname"] for d in db.department.find()}

    counts = {}
    for course in courses:
        dcode = course.get("dcode")
        dname = departments.get(dcode, dcode)
        counts[dname] = counts.get(dname, 0) + 1

    return jsonify(counts)

# --- At-Risk Students per Major Chart ---
@analytics_bp.route("/api/charts/at-risk-by-major", methods=["GET"])
def at_risk_by_major():
    students = list(db.student.find())
    departments = {d["dcode"]: d["dname"] for d in db.department.find()}

    counts = {}
    for student in students:
        ssn = student["ssn"]
        transcripts = find_transcripts(ssn)
        active_courses = [t for t in transcripts if not t.get("grade") or t["grade"] in ["F", None]]
        if len(active_courses) >= 2:
            major_code = student.get("major")
            major_name = departments.get(major_code, major_code)
            counts[major_name] = counts.get(major_name, 0) + 1

    return jsonify(counts)

# Chart: Instructor Workload by Name
@analytics_bp.route("/api/charts/instructor-workload", methods=["GET"])
def chart_instructor_workload():
    classes = list(db["class"].find())
    faculty = {f["ssn"]: f["name"] for f in db.faculty.find()}

    counts = defaultdict(int)
    for cls in classes:
        instr = cls.get("instr")
        if instr is not None:
            counts[faculty.get(instr, f"Instructor {instr}")] += 1

    return jsonify(dict(counts))


# Chart: Student Units Completed
@analytics_bp.route("/api/charts/student-units", methods=["GET"])
def chart_student_units():
    students = {s["ssn"]: s["name"] for s in db.student.find()}
    transcripts = list(db.transcript.find())
    courses = {(c["dcode"], c["cno"]): c.get("units", 0) for c in db.course.find()}

    units_by_student = defaultdict(int)
    for t in transcripts:
        if t.get("grade") not in ["F", None]:
            key = (t["dcode"], t["cno"])
            units_by_student[t["ssn"]] += courses.get(key, 0)

    result = {students.get(ssn, f"Student {ssn}"): units for ssn, units in units_by_student.items()}
    return jsonify(result)

