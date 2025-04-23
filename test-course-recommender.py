from ml_utils import predict_top_courses

# Example input
gpa = 3.3
completed_courses_count = 8
major_code = 0  # 0 = Computer Science

recommendations = predict_top_courses(gpa, completed_courses_count, major_code)
print("Top 3 recommended courses:", recommendations)
