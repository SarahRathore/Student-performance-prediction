import { useState, useEffect } from "react"
import "./App.css"

function App() {

  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])
  const totalPredictions = history.length

  const averageScore =
    history.length > 0
      ? (
        history.reduce(
          (sum, record) => sum + Number(record[1]),
          0
        ) / history.length
      ).toFixed(2)
      : 0

  const highestScore =
    history.length > 0
      ? Math.max(...history.map(record => Number(record[1])))
      : 0

  const lowestScore =
    history.length > 0
      ? Math.min(...history.map(record => Number(record[1])))
      : 0
  const [formData, setFormData] = useState({
    Hours_Studied: "",
    Attendance: "",
    Previous_Scores: "",
    Tutoring_Sessions: "",
    Sleep_Hours: "",
    Physical_Activity: "",

    Parental_Involvement: "Medium",
    Access_to_Resources: "Medium",
    Motivation_Level: "Medium",
    Teacher_Quality: "Medium",
    Family_Income: "Medium",
    Peer_Influence: "Neutral",

    Extracurricular_Activities: "No",
    Internet_Access: "Yes",
    School_Type: "Public",
    Learning_Disabilities: "No",

    Parental_Education_Level: "College",
    Distance_from_Home: "Near",
    Gender: "Female"
  })


  // Load prediction history when page opens
  useEffect(() => {

    fetch("http://127.0.0.1:5000/history")
      .then(response => response.json())
      .then(data => {
        setHistory(data)
      })
      .catch(error => {
        console.log(error)
      })

  }, [])


  // Handle input changes
  const handleChange = (event) => {

    const { name, value } = event.target

    setFormData({
      ...formData,
      [name]: value
    })
  }


  // Predict exam score
  const handlePredict = async () => {

    const requiredFields = [
      "Hours_Studied",
      "Attendance",
      "Previous_Scores",
      "Tutoring_Sessions",
      "Sleep_Hours",
      "Physical_Activity"
    ]


    // Check empty fields
    for (let field of requiredFields) {

      if (formData[field] === "") {

        alert("Please fill all numerical fields.")

        return
      }
    }


    // Attendance validation
    if (
      formData.Attendance < 0 ||
      formData.Attendance > 100
    ) {

      alert("Attendance must be between 0 and 100.")

      return
    }


    // Previous score validation
    if (
      formData.Previous_Scores < 0 ||
      formData.Previous_Scores > 100
    ) {

      alert("Previous Score must be between 0 and 100.")

      return
    }


    // Hours studied validation
    if (formData.Hours_Studied < 0) {

      alert("Hours Studied cannot be negative.")

      return
    }


    // Tutoring validation
    if (formData.Tutoring_Sessions < 0) {

      alert("Tutoring Sessions cannot be negative.")

      return
    }


    // Sleep validation
    if (
      formData.Sleep_Hours < 0 ||
      formData.Sleep_Hours > 24
    ) {

      alert("Sleep Hours must be between 0 and 24.")

      return
    }


    // Physical activity validation
    if (
      formData.Physical_Activity < 0 ||
      formData.Physical_Activity > 24
    ) {

      alert("Physical Activity must be between 0 and 24.")

      return
    }


    try {

      setLoading(true)


      const response = await fetch(
        "http://127.0.0.1:5000/predict",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify(formData)
        }
      )


      if (!response.ok) {

        throw new Error("Prediction failed")
      }


      const result = await response.json()


      // Show prediction result
      setPrediction(result)


      // Refresh prediction history
      const historyResponse = await fetch(
        "http://127.0.0.1:5000/history"
      )


      const historyData =
        await historyResponse.json()


      setHistory(historyData)


      setLoading(false)

    } catch (error) {

      console.log(error)

      setLoading(false)

      alert(
        "Unable to connect to Flask backend."
      )
    }
  }


  // Clear form
  const handleClear = () => {

    setFormData({
      Hours_Studied: "",
      Attendance: "",
      Previous_Scores: "",
      Tutoring_Sessions: "",
      Sleep_Hours: "",
      Physical_Activity: "",

      Parental_Involvement: "Medium",
      Access_to_Resources: "Medium",
      Motivation_Level: "Medium",
      Teacher_Quality: "Medium",
      Family_Income: "Medium",
      Peer_Influence: "Neutral",

      Extracurricular_Activities: "No",
      Internet_Access: "Yes",
      School_Type: "Public",
      Learning_Disabilities: "No",

      Parental_Education_Level: "College",
      Distance_from_Home: "Near",
      Gender: "Female"
    })

    setPrediction(null)
  }


  // Reset prediction history
  const handleResetHistory = async () => {

    const confirmDelete = window.confirm(
      "Are you sure you want to delete all prediction history?"
    )


    if (!confirmDelete) {
      return
    }


    try {

      const response = await fetch(
        "http://127.0.0.1:5000/history",
        {
          method: "DELETE"
        }
      )


      if (response.ok) {

        setHistory([])

        alert(
          "Prediction history deleted successfully."
        )
      }

    } catch (error) {

      console.log(error)

      alert(
        "Unable to delete prediction history."
      )
    }
  }


  return (

    <div className="app">

      <h1>
        Student Performance Prediction System
      </h1>


      <p className="app-description">
        Predict a student's exam score based on
        academic, lifestyle, and environmental factors.
      </p>


      <div className="form-container">

        <h2>
          Student Information
        </h2>


        {/* Academic Information */}

        <h3 className="section-title">
          Academic Information
        </h3>


        <label>
          Hours Studied
        </label>

        <input
          type="number"
          name="Hours_Studied"
          value={formData.Hours_Studied}
          onChange={handleChange}
          min="0"
        />


        <label>
          Attendance (%)
        </label>

        <input
          type="number"
          name="Attendance"
          value={formData.Attendance}
          onChange={handleChange}
          min="0"
          max="100"
        />


        <label>
          Previous Scores
        </label>

        <input
          type="number"
          name="Previous_Scores"
          value={formData.Previous_Scores}
          onChange={handleChange}
          min="0"
          max="100"
        />


        <label>
          Tutoring Sessions
        </label>

        <input
          type="number"
          name="Tutoring_Sessions"
          value={formData.Tutoring_Sessions}
          onChange={handleChange}
          min="0"
        />


        {/* Student Lifestyle */}

        <h3 className="section-title">
          Student Lifestyle
        </h3>


        <label>
          Sleep Hours
        </label>

        <input
          type="number"
          name="Sleep_Hours"
          value={formData.Sleep_Hours}
          onChange={handleChange}
          min="0"
          max="24"
        />


        <label>
          Physical Activity
        </label>

        <input
          type="number"
          name="Physical_Activity"
          value={formData.Physical_Activity}
          onChange={handleChange}
          min="0"
          max="24"
        />


        {/* Environment and Support */}

        <h3 className="section-title">
          Environment & Support
        </h3>


        <label>
          Parental Involvement
        </label>

        <select
          name="Parental_Involvement"
          value={formData.Parental_Involvement}
          onChange={handleChange}
        >
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
        </select>


        <label>
          Access to Resources
        </label>

        <select
          name="Access_to_Resources"
          value={formData.Access_to_Resources}
          onChange={handleChange}
        >
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
        </select>


        <label>
          Motivation Level
        </label>

        <select
          name="Motivation_Level"
          value={formData.Motivation_Level}
          onChange={handleChange}
        >
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
        </select>


        <label>
          Teacher Quality
        </label>

        <select
          name="Teacher_Quality"
          value={formData.Teacher_Quality}
          onChange={handleChange}
        >
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
        </select>


        <label>
          Family Income
        </label>

        <select
          name="Family_Income"
          value={formData.Family_Income}
          onChange={handleChange}
        >
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
        </select>


        <label>
          Peer Influence
        </label>

        <select
          name="Peer_Influence"
          value={formData.Peer_Influence}
          onChange={handleChange}
        >
          <option>Negative</option>
          <option>Neutral</option>
          <option>Positive</option>
        </select>


        <label>
          Extracurricular Activities
        </label>

        <select
          name="Extracurricular_Activities"
          value={formData.Extracurricular_Activities}
          onChange={handleChange}
        >
          <option>Yes</option>
          <option>No</option>
        </select>


        <label>
          Internet Access
        </label>

        <select
          name="Internet_Access"
          value={formData.Internet_Access}
          onChange={handleChange}
        >
          <option>Yes</option>
          <option>No</option>
        </select>


        <label>
          School Type
        </label>

        <select
          name="School_Type"
          value={formData.School_Type}
          onChange={handleChange}
        >
          <option>Public</option>
          <option>Private</option>
        </select>


        <label>
          Learning Disabilities
        </label>

        <select
          name="Learning_Disabilities"
          value={formData.Learning_Disabilities}
          onChange={handleChange}
        >
          <option>Yes</option>
          <option>No</option>
        </select>


        <label>
          Parental Education Level
        </label>

        <select
          name="Parental_Education_Level"
          value={formData.Parental_Education_Level}
          onChange={handleChange}
        >
          <option>High School</option>
          <option>College</option>
          <option>Postgraduate</option>
        </select>


        <label>
          Distance from Home
        </label>

        <select
          name="Distance_from_Home"
          value={formData.Distance_from_Home}
          onChange={handleChange}
        >
          <option>Near</option>
          <option>Moderate</option>
          <option>Far</option>
        </select>


        <label>
          Gender
        </label>

        <select
          name="Gender"
          value={formData.Gender}
          onChange={handleChange}
        >
          <option>Female</option>
          <option>Male</option>
        </select>


        {/* Buttons */}

        <button
          className="predict-btn"
          onClick={handlePredict}
          disabled={loading}
        >
          {loading
            ? "Predicting..."
            : "Predict Exam Score"}
        </button>


        <button
          className="clear-btn"
          onClick={handleClear}
        >
          Clear
        </button>


        {/* Prediction Result */}

        {prediction && (

          <div
            className={`prediction-result ${prediction.performance
              .toLowerCase()
              .replaceAll(" ", "-")
              }`}
          >

            <h2>
              Prediction Result
            </h2>


            <div className="score-display">

              <span>
                Predicted Exam Score
              </span>

              <strong>
                {prediction.predicted_score} / 100
              </strong>

            </div>


            <div className="performance-display">

              <span>
                Performance
              </span>

              <strong>
                {prediction.performance}
              </strong>

            </div>


            <p className="prediction-message">
              {prediction.performance === "Excellent" &&
                "Excellent performance! Keep up the great work."}

              {prediction.performance === "Good" &&
                "Good performance! With a little more effort, you can improve further."}

              {prediction.performance === "Average" &&
                "Your performance is average. Focus on regular study and attendance to improve."}

              {prediction.performance === "Needs Improvement" &&
                "Your score needs improvement. Try increasing your study hours and maintaining regular attendance."}
            </p>

          </div>
        )}

      </div>


      {/* Prediction History */}

      <div className="history-section">
        <div className="stats-container">

          <div className="stat-card">
            <h3>Total Predictions</h3>
            <strong>{totalPredictions}</strong>
          </div>

          <div className="stat-card">
            <h3>Average Score</h3>
            <strong>{averageScore}</strong>
          </div>

          <div className="stat-card">
            <h3>Highest Score</h3>
            <strong>{highestScore}</strong>
          </div>

          <div className="stat-card">
            <h3>Lowest Score</h3>
            <strong>{lowestScore}</strong>
          </div>

        </div>
        <h2>
          Prediction History
        </h2>


        {history.length === 0 ? (

          <p className="no-history">
            No predictions yet.
          </p>

        ) : (

          <>

            <table className="history-table">

              <thead>

                <tr>

                  <th>
                    ID
                  </th>

                  <th>
                    Predicted Score
                  </th>

                  <th>
                    Performance
                  </th>

                </tr>

              </thead>


              <tbody>

                {history.map((record) => (

                  <tr key={record[0]}>

                    <td>
                      {record[0]}
                    </td>

                    <td>
                      {record[1]}
                    </td>

                    <td>
                      {record[2]}
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>


            <button
              className="reset-history-btn"
              onClick={handleResetHistory}
            >
              Reset History
            </button>

          </>

        )}

      </div>


      {/* Footer */}

      <footer className="footer">

        <p>
          Student Performance Prediction System
        </p>

        <p>
          Built with React, Flask and Machine Learning
        </p>

      </footer>

    </div>
  )
}

export default App