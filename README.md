# Student Performance Prediction System

A Machine Learning based web application that predicts a student's expected exam score based on academic, lifestyle, and environmental factors.

The project uses a **React frontend**, **Flask backend**, **Linear Regression Machine Learning model**, and **SQLite database**.

---

## 📌 Project Overview

The Student Performance Prediction System helps estimate a student's exam score using different factors such as:

- Hours Studied
- Attendance
- Previous Scores
- Tutoring Sessions
- Sleep Hours
- Physical Activity
- Parental Involvement
- Access to Resources
- Motivation Level
- Teacher Quality
- Family Income
- Peer Influence
- Extracurricular Activities
- Internet Access
- School Type
- Learning Disabilities
- Parental Education Level
- Distance from Home
- Gender

The system predicts the exam score on a scale of **0–100** and classifies the performance as:

- Excellent
- Good
- Average
- Needs Improvement

---

## 🚀 Features

- Student performance prediction
- Machine Learning based score prediction
- React-based user interface
- Flask REST API
- SQLite prediction history
- Dashboard statistics
- Input validation
- Prediction result with performance category
- Clear form functionality
- Reset prediction history
- Responsive design
- Score restricted between 0 and 100

---

## 🛠️ Technologies Used

### Frontend

- React.js
- JavaScript
- HTML
- CSS

### Backend

- Python
- Flask
- Flask-CORS

### Machine Learning

- Pandas
- NumPy
- Scikit-learn
- Joblib

### Database

- SQLite

---

## 🤖 Machine Learning

The project uses **Linear Regression** to predict the student's exam score.

Categorical features are converted into numerical form using **One-Hot Encoding**.

### Model Pipeline

```text
Student Data
     ↓
Data Preprocessing
     ↓
Categorical Encoding
     ↓
Train-Test Split
     ↓
Linear Regression
     ↓
Exam Score Prediction
     ↓
Performance Classification
```

---

## 📊 Dataset

The project uses the **Student Performance Factors** dataset from Kaggle.

Dataset source:

https://www.kaggle.com/datasets/lainguyn123/student-performance-factors

The dataset contains **6607 records and 20 columns**.

The target variable is:

```text
Exam_Score
```

---

## 📈 Model Performance

The Linear Regression model achieved the following results on the test data:

| Metric | Result |
|---|---:|
| MAE | 0.4524 |
| MSE | 3.2560 |
| RMSE | 1.8044 |
| R² Score | 0.7696 |

The Linear Regression model performed better than the Random Forest model tested during development.

---

## 📁 Project Structure

```text
Student Performance Prediction System/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── StudentPerformanceFactors.csv
│   ├── student_performance-model.pkl
│   └── student_performance_encoder.pkl
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   ├── package.json
│   └── ...
│
├── .gitignore
└── main.py
```

---

## ⚙️ How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/SarahRathore/Student-performance-prediction.git
```

### 2. Open the project

```bash
cd Student-performance-prediction
```

---

## 🐍 Run the Backend

Open a terminal and go to the backend folder:

```bash
cd backend
```

Install the required Python packages:

```bash
pip install flask flask-cors pandas numpy scikit-learn joblib
```

Start Flask:

```bash
python app.py
```

The backend will run at:

```text
http://127.0.0.1:5000
```

---

## ⚛️ Run the Frontend

Open another terminal.

Go to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

Open the URL shown by Vite in your browser.

---

## 🗄️ Database

The project uses SQLite to store prediction history.

Each prediction stores:

- Prediction ID
- Predicted Score
- Performance Category

The database is created automatically when the backend runs.

The SQLite database file is excluded from GitHub using `.gitignore`.

---

## 🔌 API Endpoints

### Home

```text
GET /
```

Checks whether the Flask API is running.

### Prediction

```text
POST /predict
```

Receives student information and returns the predicted exam score and performance category.

### Prediction History

```text
GET /history
```

Returns previous predictions.

### Delete History

```text
DELETE /history
```

Deletes all stored prediction history.

---

## 🔮 Future Scope

Possible future improvements include:

- User authentication
- Admin dashboard
- Student login system
- More Machine Learning models
- Model comparison
- Graphical performance analysis
- Individual student reports
- PDF report generation
- Cloud database integration
- Deployment to a cloud platform
- Improved prediction models

---

## 🎓 Academic Project

This project was developed as a **B.Tech Computer Science Engineering project** to demonstrate the integration of:

- Machine Learning
- Python
- React
- Flask
- SQL/Database
- Web Development

---

## 👩‍💻 Author

**Sarah Rathore**

B.Tech Computer Science Engineering

---

## ⭐ Acknowledgement

Dataset used in this project:

Student Performance Factors dataset available on Kaggle.
