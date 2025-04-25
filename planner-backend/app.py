from flask import Flask
from flask_cors import CORS

from routes.students import students_bp
from routes.courses import courses_bp
from routes.planning import planning_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(students_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(planning_bp)

if __name__ == "__main__":
    app.run(debug=True)
