# db.py (Refactored and Fixed)

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["course_planner"]

# Student helper
def find_student(ssn):
    student = db.student.find_one({"ssn": ssn})
    return student

# Course helper
def find_course(dcode, cno):
    course = db.course.find_one({"dcode": dcode, "cno": cno})
    return course

# Department helper
def find_department(dcode):
    department = db.department.find_one({"dcode": dcode})
    return department

# Faculty helper
def find_faculty(ssn):
    faculty = db.faculty.find_one({"ssn": ssn})
    return faculty

# Class helper (fixed reserved keyword issue)
def find_class(class_id):
    course_class = db["class"].find_one({"class": class_id})
    return course_class

# Enrollment helper
def find_enrollment(class_id, ssn):
    enrollment = db.enrollment.find_one({"class": class_id, "ssn": ssn})
    return enrollment

# Prereq helper (multiple results possible)
def find_prereqs(dcode, cno):
    return list(db.prereq.find({"dcode": dcode, "cno": cno}))

# Transcript helper (multiple results possible)
def find_transcripts(ssn):
    return list(db.transcript.find({"ssn": ssn}))
