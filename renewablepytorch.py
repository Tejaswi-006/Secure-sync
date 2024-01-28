

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import requests
import pandas as pd
import time

# Load synthetic dataset from Flask app
flask_app_url = 'http://localhost:5001'  # Change to the correct Flask app URL
response = requests.get(f'{flask_app_url}/renewable_energy_data')

# Print the response to check if it contains the expected data
print("Flask App Response:")
print(response.json())

data = response.json()

# Check the data structure
features = pd.DataFrame(data, columns=['Weather', 'HistoricalProduction', 'GridConditions'])
target = pd.Series(data['RenewableEnergyAvailability'])

# Print the features and target to check the data structure
print("\nFeatures:")
print(features.head())
print("\nTarget:")
print(target.head())



# Adjust test_size to 0.2 for a more balanced split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Ensure the dataset size is sufficient
if len(X_train) < 2 or len(X_test) < 2:
    raise ValueError("Dataset size is too small. Ensure you have enough data before training the model.")

# Define a simple PyTorch model
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

# Create an instance of the model
input_size = len(features.columns)  # Number of input features
model = SimpleModel(input_size)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32)

# Train the model
for epoch in range(10):
    # Forward pass
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor.view(-1, 1))

    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    print(f'Epoch {epoch+1}/{10}, Loss: {loss.item()}')

# Convert test data to PyTorch tensor
X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)

# Make predictions on the test set
with torch.no_grad():
    predictions = model(X_test_tensor)

# Convert predictions to NumPy array
predictions_np = predictions.numpy()

# Evaluate the model
mse = mean_squared_error(y_test, predictions_np)
print(f'Mean Squared Error: {mse}')

# Wait for more data

time.sleep(15)  # Adjust the interval as needed
