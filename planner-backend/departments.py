# In courses.py or a new departments.py
from flask import Blueprint, jsonify
from db import db

departments_bp = Blueprint("departments", __name__)

@departments_bp.route("/api/departments", methods=["GET"])
def get_departments():
    departments = list(db.department.find())
    return jsonify(departments)
