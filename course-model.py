import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Sample training data
# [GPA, number of completed courses, major_code]
X = [
    [3.8, 10, 0],  
    [2.5, 5, 0],
    [3.9, 12, 0],
    [2.7, 6, 1],  
    [3.1, 9, 1],
    [3.3, 8, 0],
    [2.9, 5, 1],
    [3.5, 7, 0],
    [2.4, 4, 1]
]

y = ["CS301", "CS302", "CS301", "OR204", "OR303", "CS302", "OR204", "CS301", "OR204"]

# Encode course labels as numbers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train model
model = RandomForestClassifier()
model.fit(X, y_encoded)

# Save model and label encoder
joblib.dump(model, "course_model.pkl")
joblib.dump(label_encoder, "course_label_encoder.pkl")