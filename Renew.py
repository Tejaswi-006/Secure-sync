from flask import Flask, jsonify
import numpy as np
import time
import threading
from flask_cors import CORS
import os

app = Flask(_name_)
CORS(app)  # Enable CORS if necessary

# Environment variables for configuration
DATA_GENERATION_INTERVAL = int(os.environ.get('DATA_GENERATION_INTERVAL', 10))

# Thread lock for safe data access
data_lock = threading.Lock()

# Placeholder for real-time data
renewable_energy_data = {'Weather': [], 'HistoricalProduction': [], 'GridConditions': [], 'RenewableEnergyAvailability': []}
carbon_emission_data = {'EnergySources': [], 'ConsumptionPatterns': [], 'GridConditions': [], 'CarbonFootprint': []}

def generate_synthetic_data(iterations=50):
    for _ in range(iterations):
        with data_lock:
            # Generate synthetic data for Renewable Energy
            weather = np.random.uniform(0, 1)
            historical_production = np.random.uniform(0, 1)
            grid_conditions = np.random.uniform(0, 1)
            renewable_energy_availability = weather * 0.4 + historical_production * 0.3 + grid_conditions * 0.3

            renewable_energy_data['Weather'].append(weather)
            renewable_energy_data['HistoricalProduction'].append(historical_production)
            renewable_energy_data['GridConditions'].append(grid_conditions)
            renewable_energy_data['RenewableEnergyAvailability'].append(renewable_energy_availability)

            # Generate synthetic data for Carbon Emission
            energy_sources = np.random.uniform(0, 1)
            consumption_patterns = np.random.uniform(0, 1)
            grid_conditions = np.random.uniform(0, 1)
            carbon_footprint = energy_sources * 0.4 + consumption_patterns * 0.3 + grid_conditions * 0.3

            carbon_emission_data['EnergySources'].append(energy_sources)
            carbon_emission_data['ConsumptionPatterns'].append(consumption_patterns)
            carbon_emission_data['GridConditions'].append(grid_conditions)
            carbon_emission_data['CarbonFootprint'].append(carbon_footprint)

        time.sleep(DATA_GENERATION_INTERVAL)

# Start generating synthetic data in a separate thread
thread = threading.Thread(target=generate_synthetic_data)
thread.daemon = True  # Ensures that the thread will be killed when the main process dies
thread.start()

@app.route('/renewable_energy_data', methods=['GET'])
def get_renewable_energy_data():
    with data_lock:
        return jsonify(renewable_energy_data)

@app.route('/carbon_emission_data', methods=['GET'])
def get_carbon_emission_data():
    with data_lock:
        return jsonify(carbon_emission_data)

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=os.environ.get('FLASK_DEBUG', 'False') == 'True')
