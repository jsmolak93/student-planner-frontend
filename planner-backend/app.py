from flask import Flask
from flask_cors import CORS

from students import students_bp
from courses import courses_bp
from planning import planning_bp
from analytics import analytics_bp
from departments import departments_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(students_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(planning_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(departments_bp)


if __name__ == "__main__":
    app.run(debug=True)
