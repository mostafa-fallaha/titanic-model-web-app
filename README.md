# Titanic Web App

a model that predicts if a person on the Titanic has survived or not, based on the Age, Passenger Class and the Gender.

# Building the Model

in buildingModel/buildingModel.py, here is where im loading the data from the remote storage (Google Drive), and training the model on this data.<br>
And then im registering and versioning the model with it's metrics and artifacts using ML Flow.

# Backend

in backend/app.py, here im loading the trained model from ML Flow.<br>
and using _flask_ to create the API upon this model.

# Frontend

React + TypeScript + ChakraUI
