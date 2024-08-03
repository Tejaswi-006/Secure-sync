import streamlit as st
import requests
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class SimpleModel(nn.Module):
    def _init_(self, input_size):
        super(SimpleModel, self)._init_()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

def train_model(X_train, y_train, input_size):
    model = SimpleModel(input_size)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)

    for _ in range(10):
        outputs = model(X_train_tensor)
        loss = criterion(outputs, y_train_tensor)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return model

def make_predictions(model, X_test_tensor):
    with torch.no_grad():
        predictions = model(X_test_tensor)
    return predictions.numpy()

def fetch_data():
    flask_app_url = 'http://127.0.0.1:5000'
    response = requests.get(f'{flask_app_url}/carbon_emission_data')
    return response.json()

def train_and_predict(data):
    features = pd.DataFrame(data, columns=['EnergySources', 'ConsumptionPatterns', 'GridConditions'])
    target = pd.Series(data['CarbonFootprint'])
    if len(features) < 5:
        return None, None, None

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.1, random_state=42)
    input_size = len(features.columns)
    model = train_model(X_train, y_train, input_size)
    X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
    predictions = make_predictions(model, X_test_tensor)
    mse = mean_squared_error(y_test, predictions.flatten())
    return X_test, predictions, mse

st.title('Carbon Emission Prediction')

while True:
    data = fetch_data()
    if data and len(data['EnergySources']) > 5:
        X_test, predictions, mse = train_and_predict(data)
        if predictions is not None:
            st.subheader("Input Data for Prediction:")
            st.write(X_test)
            st.subheader("Predictions for Carbon Footprint:")
            for i, pred in enumerate(predictions.flatten(), 1):
                st.write(f"Prediction {i}: {pred:.4f} (normalized value)")
            st.subheader(f'Mean Squared Error of Predictions: {mse:.4f}')
    else:
        st.error("Not enough data to make predictions.")
    time.sleep(60)
