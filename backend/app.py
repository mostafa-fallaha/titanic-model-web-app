# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import mlflow
import mlflow.sklearn
import pandas as pd
import joblib

# ======================= Initialize the Flask application ===========================================
app = Flask(__name__)
CORS(app)

# ======================= Load the trained model and scaler from MLflow ===============================
mlflow.set_tracking_uri("http://127.0.0.1:5000")
model = mlflow.sklearn.load_model("runs:/9de1cbb2b2b047b6abd509eb0aeb82d8/model")
# model_name = "titanic_model_final"
# model_version = 9
# model = mlflow.sklearn.load_model(model_uri=f"models:/{model_name}/{model_version}")

mean = joblib.load(mlflow.artifacts.download_artifacts("runs:/9de1cbb2b2b047b6abd509eb0aeb82d8/mean.pkl"))
std = joblib.load(mlflow.artifacts.download_artifacts("runs:/9de1cbb2b2b047b6abd509eb0aeb82d8/std.pkl"))

# ======================= Define a route for the default URL ============================================
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    age = (data['Age'] - mean) / std
    pclass_2nd = data['PClass_2nd']
    pclass_3rd = data['PClass_3rd']
    sex_male = data['Sex_male']

    input_data = pd.DataFrame(
        [[age, pclass_2nd, pclass_3rd, sex_male]],
        columns=["Age", "PClass_2nd", "PClass_3rd", "Sex_male"]
    )

    prediction = model.predict(input_data)
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
