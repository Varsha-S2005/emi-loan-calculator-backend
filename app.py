from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Route to calculate EMI
@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Validate required fields
        if not all(key in data for key in ('principal', 'rate', 'time')):
            return jsonify({"error": "Missing required parameters: 'principal', 'rate', or 'time'."}), 400

        # Parse and validate input values
        principal = float(data['principal'])
        rate = float(data['rate']) / 12 / 100  # Convert annual rate to monthly and percentage to decimal
        time = int(data['time']) * 12  # Convert years to months

        # EMI calculation formula
        emi = (principal * rate * math.pow(1 + rate, time)) / (math.pow(1 + rate, time) - 1)

        return jsonify({"principal": principal, "rate": rate * 12 * 100, "time": time // 12, "emi": round(emi, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
