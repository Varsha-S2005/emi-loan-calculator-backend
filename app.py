import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Welcome to the Loan EMI Calculator!"

# Loan EMI Calculation route
@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        data = request.get_json()
        principal = float(data.get('principal', 0))
        rate = float(data.get('rate', 0))
        time = int(data.get('time', 0))

        if principal <= 0 or rate <= 0 or time <= 0:
            return jsonify({"error": "Invalid input values"}), 400

        # Convert annual interest rate to monthly and time in months
        monthly_rate = rate / (12 * 100)
        time_in_months = time * 12

        # EMI calculation formula
        emi = (principal * monthly_rate * pow(1 + monthly_rate, time_in_months)) / (pow(1 + monthly_rate, time_in_months) - 1)
        emi = round(emi, 2)

        return jsonify({"emi": emi})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
