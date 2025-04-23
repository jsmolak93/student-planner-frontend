import joblib
import numpy as np

# Load course recommendation model and label encoder
course_model = joblib.load("course_model.pkl")
course_label_encoder = joblib.load("course_label_encoder.pkl")

def predict_top_courses(gpa, completed_courses_count, major_code):
    features = np.array([[gpa, completed_courses_count, major_code]])
    proba = course_model.predict_proba(features)[0]
    top_indices = np.argsort(proba)[-3:][::-1]
    top_courses = course_label_encoder.inverse_transform(top_indices)
    return top_courses.tolist()