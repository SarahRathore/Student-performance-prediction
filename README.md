# Student Performance Prediction System

A machine learning web application that predicts students' exam scores based on academic, personal, and lifestyle-related factors. The project combines a Python-based machine learning pipeline with a Flask backend and a React frontend to provide an interactive prediction experience.

## Project Overview

The Student Performance Prediction System uses machine learning to estimate a student's exam score from input features such as study hours, attendance, previous scores, tutoring sessions, sleep hours, and other factors.

The application allows users to enter student information, generate a predicted exam score, and view prediction history.

## Features

- **Exam Score Prediction:** Predicts student exam scores using a trained machine learning model.
- **Interactive User Interface:** React-based frontend for entering student information.
- **REST API:** Flask backend processes prediction requests.
- **Data Preprocessing:** Handles missing values and converts categorical features into numerical representations.
- **Machine Learning Pipeline:** Combines preprocessing and prediction into a reusable pipeline.
- **Prediction History:** Stores and retrieves previous predictions using SQLite.
- **Model Persistence:** Saves the trained model using Joblib so it can be loaded without retraining on every request.

## Tech Stack

| Component | Technologies |
|---|---|
| Frontend | React, JavaScript, CSS |
| Backend | Python, Flask |
| Machine Learning | Pandas, NumPy, Scikit-learn |
| Model Persistence | Joblib |
| Database | SQLite |
| API Communication | REST API, JSON |

## Project Structure

```text
Student-performance-prediction/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── train_model.py
│   └── student_performance_pipeline.pkl
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
└── README.md
```

*Note: The structure above shows the main project files. Other files may exist in your repository.*

## Dataset

The project uses a student performance dataset containing academic, family, school, and lifestyle-related features.

**Target variable:** `Exam_Score`

Examples of input features include:

- Hours studied
- Attendance
- Previous scores
- Tutoring sessions
- Sleep hours
- Parental involvement
- Access to resources
- Motivation level
- Teacher quality
- School type

The target variable is separated from the input features during model training.

## Machine Learning Workflow

1. **Data Loading:** Load the dataset using Pandas.
2. **Data Cleaning:** Identify and handle missing values.
3. **Feature Selection:** Separate input features from the target variable.
4. **Preprocessing:** Impute missing values and encode categorical features.
5. **Train-Test Split:** Divide the dataset into training and testing sets.
6. **Model Training:** Train the selected regression model.
7. **Evaluation:** Evaluate performance using MAE, RMSE, and R².
8. **Model Saving:** Save the trained preprocessing and prediction pipeline using Joblib.
9. **Prediction:** Load the saved pipeline in Flask and generate predictions from frontend inputs.

## Model Evaluation

The following results were obtained during model evaluation in the development version of this project.

| Metric | Result |
|---|---:|
| Mean Absolute Error (MAE) | 0.4524 |
| Root Mean Squared Error (RMSE) | 1.8044 |
| R² Score | 0.7696 |

These results are from the evaluated model version and may change if the dataset, preprocessing, or training procedure changes.

### What the metrics mean

- **MAE:** Measures the average absolute difference between actual and predicted exam scores.
- **RMSE:** Measures prediction error while penalizing larger errors more strongly.
- **R² Score:** Measures how much of the variation in exam scores is explained by the model.

## Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.10 or a compatible version
- Node.js and npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/SarahRathore/Student-performance-prediction.git
cd Student-performance-prediction
```

### 2. Set up the Python backend

Open a terminal in the project directory:

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required Python packages:

```bash
pip install flask flask-cors pandas numpy scikit-learn joblib
```

If the project includes a `requirements.txt`, use this instead:

```bash
pip install -r requirements.txt
```

Make sure the trained model file `student_performance_pipeline.pkl` exists in the backend directory.

Start the Flask server:

```bash
python app.py
```

The backend should start at the address configured in `app.py`, commonly `http://127.0.0.1:5000`.

### 3. Set up the React frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite, commonly `http://localhost:5173`.

Ensure the frontend API URL matches the address and port of your Flask backend.

## How to Use

1. Start the Flask backend.
2. Start the React frontend.
3. Open the frontend in your browser.
4. Enter the required student information.
5. Submit the form to generate a predicted exam score.
6. View the result and prediction history, if available in the application.

## API Endpoints

The Flask application provides the following endpoints, as implemented in the backend.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/predict` | Generates a student exam score prediction. |
| GET | `/history` | Retrieves saved prediction history. |

The `/predict` endpoint accepts input data in JSON format. Refer to `backend/app.py` for the exact request fields and response structure.

## Database

SQLite is used to store prediction history. Database operations are managed in `backend/database.py`.

The database can store information such as predicted scores and performance categories, depending on the current implementation.

The database file is generated or initialized by the application's database setup code.

## Future Improvements

- Add more detailed visualizations and student performance analytics.
- Improve model accuracy through model comparison and hyperparameter tuning.
- Add input validation and clearer error messages.
- Introduce user authentication and role-based access.
- Deploy the application online.
- Add automated tests for the API and frontend.

## Limitations

- Predictions are estimates and are not guaranteed to match actual exam scores.
- Model performance depends on the quality and representativeness of the training dataset.
- Relationships in the dataset do not necessarily imply causation.
- Predictions should support educational analysis rather than determine a student's potential or future.

## Author

**Sarah Rathore**

B.Tech Computer Science and Engineering

GitHub: [@SarahRathore](https://github.com/SarahRathore)

## License

This project is available for educational and learning purposes. Add a formal license file if you intend to specify permissions for reuse and distribution.
