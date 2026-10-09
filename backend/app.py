from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_predictions
from database import delete_predictions
from database import save_prediction
from database import init_db
from pathlib import Path
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# Load the trained model
BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(
    BASE_DIR / "student_performance_pipeline.pkl"
)
MODEL_VERSION = "1.0"
# The 19 features used during training
FEATURES = [
    "Hours_Studied",
    "Attendance",
    "Parental_Involvement",
    "Access_to_Resources",
    "Extracurricular_Activities",
    "Sleep_Hours",
    "Previous_Scores",
    "Motivation_Level",
    "Internet_Access",
    "Tutoring_Sessions",
    "Family_Income",
    "Teacher_Quality",
    "School_Type",
    "Peer_Influence",
    "Physical_Activity",
    "Learning_Disabilities",
    "Parental_Education_Level",
    "Distance_from_Home",
    "Gender"
]

NUMERIC_RANGES = {
    "Hours_Studied": (1, 44),
    "Attendance": (60, 100),
    "Sleep_Hours": (4, 10),
    "Previous_Scores": (50, 100),
    "Tutoring_Sessions": (0, 8),
    "Physical_Activity": (0, 6)
}

CATEGORIES = {
    "Parental_Involvement": ["Low", "Medium", "High"],
    "Access_to_Resources": ["Low", "Medium", "High"],
    "Extracurricular_Activities": ["Yes", "No"],
    "Motivation_Level": ["Low", "Medium", "High"],
    "Internet_Access": ["Yes", "No"],
    "Family_Income": ["Low", "Medium", "High"],
    "Teacher_Quality": ["Low", "Medium", "High"],
    "School_Type": ["Public", "Private"],
    "Peer_Influence": ["Positive", "Negative", "Neutral"],
    "Learning_Disabilities": ["Yes", "No"],
    "Parental_Education_Level": [
        "High School", "College", "Postgraduate"
    ],
    "Distance_from_Home": ["Near", "Moderate", "Far"],
    "Gender": ["Male", "Female"]
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Student Performance Prediction API is running"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "model_version": MODEL_VERSION
    }), 200

@app.route("/model-info", methods=["GET"])
def model_info():
    return jsonify({
        "model_version": MODEL_VERSION,
        "model_type": "Linear Regression",
        "target": "Exam_Score"
    }), 200

def get_performance(score):
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 60:
        return "Average"
    else:
        return "Needs Improvement"
    
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Please send a valid JSON object."
            }), 400

        # Check that every input is present
        missing = [
            field for field in FEATURES
            if field not in data
            or data[field] is None
            or data[field] == ""
        ]

        if missing:
            return jsonify({
                "error": "Missing fields: " + ", ".join(missing)
            }), 400

        cleaned = {}

        # Validate numerical inputs
        for field, (minimum, maximum) in NUMERIC_RANGES.items():
            try:
                value = float(data[field])
            except (TypeError, ValueError):
                return jsonify({
                    "error": f"{field} must be a number."
                }), 400

            if not minimum <= value <= maximum:
                return jsonify({
                    "error": (
                        f"{field} must be between "
                        f"{minimum} and {maximum}."
                    )
                }), 400

            cleaned[field] = value

        # Validate categorical inputs
        for field, allowed in CATEGORIES.items():
            if data[field] not in allowed:
                return jsonify({
                    "error": f"Invalid value for {field}."
                }), 400

            cleaned[field] = data[field]

        # Convert the inputs into a DataFrame
        input_df = pd.DataFrame(
            [cleaned],
            columns=FEATURES
        )

        # Predict the exam score
        predicted_score = float(
            model.predict(input_df)[0]
         )

        predicted_score = max(0, min(100, predicted_score))
        predicted_score = round(predicted_score, 2)

        performance = get_performance(predicted_score)

        save_prediction(
          predicted_score,
          performance
  )

        return jsonify({
         "predicted_score": predicted_score,
         "performance": performance,
         "model_version": MODEL_VERSION
})

    except Exception:
        app.logger.exception("Prediction failed")

        return jsonify({
            "error": "An internal prediction error occurred."
        }), 500

@app.route("/history", methods=["GET"])
def history():
    try:
        rows = get_predictions()

        predictions = [
          {
           "id": row[0],
            "predicted_score": row[1],
            "performance": row[2]
          }
          for row in rows
        ]
        return jsonify(predictions), 200

    except Exception:
        app.logger.exception("Failed to load history")

        return jsonify({
            "error": "Could not load prediction history"
        }), 500
@app.route("/history", methods=["DELETE"])
def clear_history():
    try:
        delete_predictions()

        return jsonify({
            "message": "Prediction history deleted successfully"
        }), 200

    except Exception:
        app.logger.exception("Failed to delete history")

        return jsonify({
            "error": "Could not delete prediction history"
        }), 500





if __name__ == "__main__":
    init_db()
    app.run(debug=False)
