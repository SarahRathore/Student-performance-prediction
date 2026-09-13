import pandas as pd   
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.ensemble import RandomForestRegressor
import joblib
df=pd.read_csv("StudentPerformanceFactors.csv")
# print("First 5 rows\n",df.head())
# print("Shape:\n",df.shape)
# print("Columns:\n",df.columns)
# print("Last 5 rows\n",df.tail())
# print("Information\n",df.info())
# print("Statistics\n",df.describe())
# print("Missing Values\n",df.isnull().sum())
# print("Duplicate rows\n",df.duplicated().sum())
# print("Exam Score\n",df['Exam_Score'].value_counts().sort_index())
# print("Correlations\n",df.corr(numeric_only=True)["Exam_Score"].sort_values(ascending=False))
# print("Categorical Values",df.select_dtypes(include="object").nunique())
# for column in df.select_dtypes(include="object").columns:
#   print(df[column].unique())
# print("Teacher Quality Mode:",df["Teacher_Quality"].mode()[0])
# print("Parental Education Mode:",df["Parental_Education_Level"].mode()[0])
# print("Distance from Home:",df["Distance_from_Home"].mode()[0])

df['Teacher_Quality']=df["Teacher_Quality"].fillna("Medium")
df["Parental_Education_Level"]=df["Parental_Education_Level"].fillna("High School")
df["Distance_from_Home"]=df["Distance_from_Home"].fillna("Near")

print(df.isnull().sum())

x=df.drop("Exam_Score",axis=1)
y=df["Exam_Score"]
print("x shape",x.shape)
print("y shape",y.shape)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

print("X_train:", x_train.shape)
print("X_test:", x_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)

categorical_columns=x.select_dtypes(include="object").columns
print("categorical columns:",categorical_columns)

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

x_train_encoded=encoder.fit_transform(x_train[categorical_columns])
x_test_encoded=encoder.fit_transform(x_test[categorical_columns])
print("Encoded X_train shape:", x_train_encoded.shape)
print("Encoded X_test shape:", x_test_encoded.shape)

numerical_columns = x.select_dtypes(exclude="object").columns
print("Numerical columns:",numerical_columns)

x_train_numeric=x_train[numerical_columns].values
x_test_numeric=x_test[numerical_columns].values

x_train_final=np.hstack((x_train_numeric,x_train_encoded))
x_test_final=np.hstack((x_test_numeric,x_test_encoded))
print("final x_train shape:",x_train_final.shape)
print("final x_test shape:",x_test_final.shape)

model=LinearRegression()
model.fit(x_train_final,y_train)
print("model training completed")

y_pred=model.predict(x_test_final)
print("predicted score:",y_pred[:10])
print("actual score",y_test.iloc[:10].values)

mae=mean_absolute_error(y_test,y_pred)
mse=mean_squared_error(y_test,y_pred)
rmse=mse**0.5
r2=r2_score(y_test,y_pred)
print("\nModel Evaluation:")
print("MAE:", mae)
print("MSE:", mse)
print("RMSE:", rmse)
print("R2 Score:", r2)

rf_model=RandomForestRegressor(
    n_estimators=100,random_state=42
)
rf_model.fit(x_train_final,y_train)
rf_pred=rf_model.predict(x_test_final)
print("random forestpredictions",rf_pred[:10])

rf_mae = mean_absolute_error(y_test, rf_pred)
rf_mse = mean_squared_error(y_test, rf_pred)
rf_rmse = rf_mse ** 0.5
rf_r2 = r2_score(y_test, rf_pred)

print("\nRandom Forest Evaluation:")
print("MAE:", rf_mae)
print("MSE:", rf_mse)
print("RMSE:", rf_rmse)
print("R2 Score:", rf_r2)

joblib.dump(model,"student_performance-model.pkl")
print("best model saved")

feature_importance=pd.Series(
  model.coef_,
  index =numerical_columns.tolist()+list(encoder.get_feature_names_out(categorical_columns))
)
print("feature importance",feature_importance.sort_values(ascending=False))

import matplotlib.pyplot as plt 
plt.scatter(y_test, y_pred)
plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    linestyle="--"
)
plt.xlabel("Actual Exam Score")
plt.ylabel("Predicted Exam Score")
plt.title("Actual vs Predicted Exam Score")
plt.show()

joblib.dump(encoder, "student_performance_encoder.pkl")
print("Encoder saved successfully!")

new_student = {
    "Hours_Studied": 6,
    "Attendance": 90,
    "Parental_Involvement": "High",
    "Access_to_Resources": "High",
    "Extracurricular_Activities": "Yes",
    "Sleep_Hours": 7,
    "Previous_Scores": 75,
    "Motivation_Level": "High",
    "Internet_Access": "Yes",
    "Tutoring_Sessions": 2,
    "Family_Income": "Medium",
    "Teacher_Quality": "High",
    "School_Type": "Public",
    "Peer_Influence": "Positive",
    "Physical_Activity": 4,
    "Learning_Disabilities": "No",
    "Parental_Education_Level": "College",
    "Distance_from_Home": "Near",
    "Gender": "Female"
}

new_student_df = pd.DataFrame([new_student])

print("\nNew Student:")
print(new_student_df)

new_student_encoded=encoder.transform(
    new_student_df[categorical_columns]
)
new_student_numeric=new_student_df[numerical_columns].values
new_student_final=np.hstack((new_student_numeric,new_student_encoded))
print("new student data prepared for prediction",new_student_final.shape)

new_prediction=model.predict(new_student_final)
predicted_score = round(new_prediction[0], 2)
print("predicted exam score",new_prediction[0])

if predicted_score>=90:
    performance="excellent"
elif predicted_score>=75:
    performance="good"
elif predicted_score>=60:
    performance="average"
else:
    performance="needs improvement"
print("performance level:",performance)