# api/index.py
# This file contains the Flask application that serves as the backend for the ETL demonstration.
# It defines routes for extracting, transforming, and loading data.

from flask import Flask, jsonify, request
from flask_cors import CORS # Used to handle Cross-Origin Resource Sharing for frontend communication

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, allowing the frontend to make requests

# --- Global Data Store (for demonstration purposes only) ---
# In a real application, this would be a database or persistent storage.
# We'll use these lists to simulate data flow through the ETL process.
extracted_data = []
transformed_data = []
loaded_results = []

# --- Dummy Data Source ---
# This simulates raw data that would be extracted from an external system.
RAW_DATA_SOURCE = [
    {"id": 1, "name": "Alice", "age": 24, "city": "New York"},
    {"id": 2, "name": "Bob", "age": 30, "city": "London"},
    {"id": 3, "name": "Charlie", "age": 28, "city": "Paris"},
    {"id": 4, "name": "David", "age": 22, "city": "New York"},
    {"id": 5, "name": "Eve", "age": 35, "city": "Berlin"},
]

@app.route('/')
def home():
    """
    A simple home route to confirm the API is running.
    """
    return "ETL Demo API is running!"

@app.route('/extract', methods=['POST'])
def extract_data():
    """
    Simulates the data extraction phase.
    It "extracts" data from the RAW_DATA_SOURCE and stores it in extracted_data.
    """
    global extracted_data
    extracted_data = list(RAW_DATA_SOURCE) # Make a copy of the raw data
    print(f"Extracted: {extracted_data}") # Log to console for debugging
    return jsonify({
        "message": "Data extracted successfully!",
        "data": extracted_data
    })

@app.route('/transform', methods=['POST'])
def transform_data():
    """
    Simulates the data transformation phase.
    It takes the extracted_data, filters it (e.g., age > 25),
    and adds a new field ('status').
    """
    global transformed_data
    if not extracted_data:
        return jsonify({"message": "No data to transform. Please extract first."}), 400

    transformed_data = []
    for record in extracted_data:
        # Example transformation: Filter by age and add a status field
        if record['age'] > 25:
            new_record = record.copy() # Create a copy to avoid modifying original
            new_record['status'] = "Active"
            transformed_data.append(new_record)
    print(f"Transformed: {transformed_data}") # Log to console for debugging
    return jsonify({
        "message": "Data transformed successfully!",
        "data": transformed_data
    })

@app.route('/load', methods=['POST'])
def load_data():
    """
    Simulates the data loading phase.
    It takes the transformed_data and "loads" it.
    In a real scenario, this would involve writing to a database, file, or API.
    Here, we'll just store it in loaded_results and return it.
    """
    global loaded_results
    if not transformed_data:
        return jsonify({"message": "No data to load. Please transform first."}), 400

    loaded_results = list(transformed_data) # Simulate loading by copying
    print(f"Loaded: {loaded_results}") # Log to console for debugging
    return jsonify({
        "message": "Data loaded successfully!",
        "data": loaded_results
    })

@app.route('/reset', methods=['POST'])
def reset_pipeline():
    """
    Resets the pipeline by clearing all in-memory data.
    """
    global extracted_data, transformed_data, loaded_results
    extracted_data = []
    transformed_data = []
    loaded_results = []
    print("Pipeline reset.") # Log to console for debugging
    return jsonify({"message": "Pipeline reset successfully!"})

if __name__ == '__main__':
    # This block runs when you execute the script directly (e.g., python api/index.py)
    # It's useful for local testing. Vercel will handle running the app differently.
    app.run(debug=True, port=5000)
