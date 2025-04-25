from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["student_planner"]

COLLECTION_NAMES = ["univDB1", "univDB2", "univDB3", "univDB4", "univDB5"]
COLLECTIONS = [db[name] for name in COLLECTION_NAMES]

# Find helper function
def find_in_tables(table, query):
    for collection in COLLECTIONS:
        doc = collection.find_one(
            {f"tables.{table}": {"$elemMatch": query}},
            {f"tables.{table}.$": 1}
        )
        if doc and "tables" in doc and table in doc["tables"]:
            return doc["tables"][table][0], collection
    return None, None

# Student helper
def find_student(ssn):
    return find_in_tables("student", {"ssn": ssn})

# Course helper
def find_course(dcode, cno):
    return find_in_tables("course", {"dcode": dcode, "cno": cno})

# Department helper
def find_department(dcode):
    return find_in_tables("department", {"dcode": dcode})

# Faculty helper
def find_faculty(ssn):
    return find_in_tables("faculty", {"ssn": ssn})

# Class helper
def find_class(class_id):
    return find_in_tables("class", {"class": class_id})

# Enrollment helper
def find_enrollment(class_id, ssn):
    return find_in_tables("enrollment", {"class": class_id, "ssn": ssn})

# Prereq helper (multiple results possible)
def find_prereqs(dcode, cno):
    prereqs = []
    for collection in COLLECTIONS:
        doc = collection.find_one({"tables.prereq": {"$elemMatch": {"dcode": dcode, "cno": cno}}}, {"tables.prereq": 1})
        if doc and "tables" in doc and "prereq" in doc["tables"]:
            prereqs.extend([p for p in doc["tables"]["prereq"] if p["dcode"] == dcode and p["cno"] == cno])
    return prereqs

# Transcript helper (multiple results possible)
def find_transcripts(ssn):
    transcripts = []
    for collection in COLLECTIONS:
        doc = collection.find_one({"tables.transcript": {"$elemMatch": {"ssn": ssn}}}, {"tables.transcript": 1})
        if doc and "tables" in doc and "transcript" in doc["tables"]:
            transcripts.extend([t for t in doc["tables"]["transcript"] if t["ssn"] == ssn])
    return transcripts
