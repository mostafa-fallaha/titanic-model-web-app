from datetime import datetime
import io
import dvc.api
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import mlflow
import mlflow.sklearn
import os

# ============================== Trainig the model ============================================================
url = "https://github.com/mostafa-fallaha/titanic-dvc"
data = dvc.api.read("data/Titanic.csv", repo=url)
df = pd.read_csv(io.StringIO(data))

mean = df.Age.mean()
std = df.Age.std()

scaler = StandardScaler()
df['Age'] = scaler.fit_transform(df[['Age']])

X = df[["Age", "PClass_2nd", "PClass_3rd", "Sex_male"]]
y = df.Survived

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

model_1 = DecisionTreeClassifier(max_depth=3, min_samples_leaf=40, min_samples_split=80)

model_1.fit(X_train, y_train)
predictions = model_1.predict(X_test)

mc = pd.DataFrame(confusion_matrix(y_test, predictions),
                    columns=['pred_died', 'pred_survived'],
                    index=['obs_died', 'obs_survived'])
# print(mc)

accuracy = accuracy_score(y_test, predictions)

precision_1 = precision_score(y_test, predictions, average='binary', pos_label=1)
precision_0 = precision_score(y_test, predictions, average='binary', pos_label=0)
precision_macro = precision_score(y_test, predictions, average='macro')

recall_1 = recall_score(y_test, predictions, average='binary', pos_label=1)
recall_0 = recall_score(y_test, predictions, average='binary', pos_label=0)
recall_macro = recall_score(y_test, predictions, average='macro')

f1score = f1_score(y_test, predictions)


# ============================== Logging the model with MLFlow============================================================
script_path = os.path.abspath(__file__)
runname = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

# Start MLflow run
mlflow.set_experiment('titanic_experiment1')
with mlflow.start_run(run_name=runname) as mlflow_run:
    run_id = mlflow_run.info.run_id

    # Log model parameters
    mlflow.log_param("max_depth", 3)
    mlflow.log_param("min_samples_leaf", 40)
    mlflow.log_param("min_samples_split", 80)

    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision_1", precision_1)
    mlflow.log_metric("precision_0", precision_0)
    mlflow.log_metric("precision_macro", precision_macro)
    mlflow.log_metric("recall_1", recall_1)
    mlflow.log_metric("recall_0", recall_0)
    mlflow.log_metric("recall_macro", recall_macro)
    mlflow.log_metric("f1_score", f1score)

    # Log the model
    mlflow.sklearn.log_model(model_1, "model")

    # Register the model
    model_uri = f"runs:/{run_id}/model"
    mlflow.register_model(model_uri=model_uri, name="titanic_model_final")
    
    # Log artifacts
    mlflow.log_artifact(script_path)
    mlflow.log_artifact('mean.pkl')
    mlflow.log_artifact('std.pkl')

