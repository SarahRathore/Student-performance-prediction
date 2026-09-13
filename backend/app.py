from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
from database import sqlite3
import sqlite3
from database import save_prediction

app = Flask(__name__)
CORS(app)

# Load trained model and encoder
model = joblib.load("student_performance-model.pkl")
encoder = joblib.load("student_performance_encoder.pkl")

df = pd.read_csv("StudentPerformanceFactors.csv")

# Separate input columns
X = df.drop("Exam_Score", axis=1)

# Identify categorical and numerical columns
categorical_columns = X.select_dtypes(include="object").columns
numerical_columns = X.select_dtypes(exclude="object").columns


@app.route("/")
def home():
    return "Student Performance Prediction API is running"


@app.route("/predict", methods=["POST"])
def predict():

    # Get data sent from React
    data = request.get_json()

    # Convert received data into DataFrame
    student_df = pd.DataFrame([data])

    # Convert numerical values from strings to numbers
    for column in numerical_columns:
        student_df[column] = pd.to_numeric(student_df[column])

    # Encode categorical data
    student_encoded = encoder.transform(
        student_df[categorical_columns]
    )

    # Get numerical data
    student_numeric = student_df[numerical_columns].values

    # Combine numerical + encoded categorical data
    student_final = np.hstack(
        (student_numeric, student_encoded)
    )

    # Make prediction
    prediction = model.predict(student_final)

    predicted_score = round(
    max(0, min(100, float(prediction[0]))),
    2
)
    

    # Performance category
    if predicted_score >= 90:
        performance = "Excellent"
    elif predicted_score >= 75:
        performance = "Good"
    elif predicted_score >= 60:
        performance = "Average"
    else:
        performance = "Needs Improvement"

    save_prediction(predicted_score, performance)
    
    return jsonify({
        "predicted_score": predicted_score,
        "performance": performance
    })


@app.route("/history", methods=["GET"])
def history():

    connection = sqlite3.connect(
        "student_predictions.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM predictions ORDER BY id DESC"
    )

    records = cursor.fetchall()

    connection.close()

    return jsonify(records)


@app.route("/history", methods=["DELETE"])
def delete_history():

    connection = sqlite3.connect(
        "student_predictions.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM predictions"
    )

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Prediction history deleted successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)