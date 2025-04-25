from flask import Blueprint, request, jsonify
from db import find_course, COLLECTIONS

courses_bp = Blueprint("courses", __name__)

# Get a specific course
@courses_bp.route("/api/courses/<string:dcode>/<int:cno>", methods=["GET"])
def get_course(dcode, cno):
    course, _ = find_course(dcode, cno)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course)

# Add a new course
@courses_bp.route("/api/courses", methods=["POST"])
def add_course():
    data = request.json
    dcode = data.get("dcode")
    cno = data.get("cno")

    existing_course, _ = find_course(dcode, cno)
    if existing_course:
        return jsonify({"error": "Course already exists"}), 400

    COLLECTIONS[0].update_one({}, {"$push": {"tables.course": data}})
    return jsonify({"message": "Course added successfully!"}), 201

# Update an existing course
@courses_bp.route("/api/courses/<string:dcode>/<int:cno>", methods=["PUT"])
def update_course(dcode, cno):
    updates = request.json
    _, collection = find_course(dcode, cno)
    if not collection:
        return jsonify({"error": "Course not found"}), 404

    collection.update_one(
        {"tables.course": {"$elemMatch": {"dcode": dcode, "cno": cno}}},
        {"$set": {f"tables.course.$.{key}": value for key, value in updates.items()}}
    )
    return jsonify({"message": "Course updated successfully!"})

# Delete a course
@courses_bp.route("/api/courses/<string:dcode>/<int:cno>", methods=["DELETE"])
def delete_course(dcode, cno):
    _, collection = find_course(dcode, cno)
    if not collection:
        return jsonify({"error": "Course not found"}), 404

    collection.update_one({}, {"$pull": {"tables.course": {"dcode": dcode, "cno": cno}}})
    return jsonify({"message": "Course deleted successfully!"})