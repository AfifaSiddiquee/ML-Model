# -*- coding: utf-8 -*-
"""app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H7LRThHMWQRrLQ3JmUOsiyfeHbGBIhBp
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Initialize scaler and model outside the if block to make them accessible later
scaler = StandardScaler()  # Initialize scaler here
model = RandomForestClassifier(n_estimators=100, random_state=42) # Initialize model here

# Upload dataset
st.title("Diabetes Prediction App")

# Preload the dataset from a fixed file (assuming it's in the same folder as app.py)
data = pd.read_csv("diabetes.csv")  # Replace with your dataset path if needed

# Splitting data
X = data.drop(columns=['Outcome'])
y = data['Outcome']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardizing features
X_train_scaled = scaler.fit_transform(X_train)  # Use the initialized scaler
X_test_scaled = scaler.transform(X_test)

# Training a model
model.fit(X_train_scaled, y_train)  # Use the initialized model

# Evaluate model
predictions = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, predictions)

# Save the model
with open('diabetes_model.pkl', 'wb') as file:
    pickle.dump((scaler, model), file)

# st.write(f"Model Accuracy: {accuracy * 100:.2f}%")

# User inputs
pregnancies = st.number_input("Pregnancies", 0, 20, 1)
glucose = st.number_input("Glucose Level", 0, 200, 100)
bp = st.number_input("Blood Pressure", 0, 150, 80)
skin_thickness = st.number_input("Skin Thickness", 0, 100, 20)
insulin = st.number_input("Insulin Level", 0, 900, 100)
bmi = st.number_input("BMI", 0.0, 50.0, 25.0)
dpf = st.number_input("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
age = st.number_input("Age", 0, 100, 30)

if st.button("Predict"):
    with open('diabetes_model.pkl', 'rb') as file:
        scaler, model = pickle.load(file)

    input_data = np.array([[pregnancies, glucose, bp, skin_thickness, insulin, bmi, dpf, age]])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    result = "Diabetic" if prediction[0] == 1 else "Not Diabetic"
    st.write(f"Prediction: {result}")

