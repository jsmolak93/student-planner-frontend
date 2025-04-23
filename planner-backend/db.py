from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["student_planner"]

students = db["students"]
courses = db["courses"]
degree_reqs = db["degree_requirements"]
faculty = db["faculty"]
enrollments = db["enrollments"]
semesters = db["semesters"]
recommendations = db["recommendations"]
