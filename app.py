from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="loan_emi_db"
)

# Route to calculate EMI
@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        # Print headers and incoming data for debugging
        print("Headers:", request.headers)
        print("Data:", request.data)
        print("JSON Data:", request.get_json())

        # Check if the request content type is JSON
        if request.content_type != 'application/json':
            return jsonify({"error": f"Unsupported Media Type: {request.content_type}. Content-Type must be 'application/json'."}), 415

        # Get JSON data from request
        data = request.get_json()
        
        # Check if the data is None (invalid or empty JSON)
        if data is None:
            return jsonify({"error": "Invalid or empty JSON payload."}), 400

        # Validate required fields
        if not all(key in data for key in ('principal', 'rate', 'time')):
            return jsonify({"error": "Missing required parameters: 'principal', 'rate', or 'time'."}), 400

        # Parse and validate input values
        try:
            principal = float(data['principal'])
            rate = float(data['rate']) / 12 / 100  # Convert annual rate to monthly and percentage to decimal
            time = int(data['time']) * 12  # Convert years to months
        except ValueError:
            return jsonify({"error": "Invalid data type for 'principal', 'rate', or 'time'."}), 400

        # EMI calculation formula
        emi = (principal * rate * math.pow(1 + rate, time)) / (math.pow(1 + rate, time) - 1)

        # Save the EMI calculation to the database
        cursor = db.cursor()
        query = "INSERT INTO emi_records (principal, rate, time, emi) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (principal, rate * 12 * 100, time // 12, emi))
        db.commit()

        return jsonify({"principal": principal, "rate": rate * 12 * 100, "time": time // 12, "emi": round(emi, 2)})

    except Exception as e:
        print(f"Error: {str(e)}")  # Print the error for debugging
        return jsonify({"error": str(e)}), 500

# Route to get all EMI records
@app.route('/emi_records', methods=['GET'])
def get_emi_records():
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM emi_records"
        cursor.execute(query)
        records = cursor.fetchall()
        return jsonify(records)

    except Exception as e:
        print(f"Error: {str(e)}")  # Print the error for debugging
        return jsonify({"error": str(e)}), 500

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
