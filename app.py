from flask import Flask, request, jsonify
import math
import os

app = Flask(__name__)

def calculate_emi(principal, rate, tenure):
    monthly_rate = rate / (12 * 100)  # Convert annual rate to monthly
    tenure_months = tenure * 12  # Convert years to months
    emi = (principal * monthly_rate * math.pow(1 + monthly_rate, tenure_months)) / (math.pow(1 + monthly_rate, tenure_months) - 1)
    return round(emi, 2)

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi_route():
    data = request.get_json()
    try:
        principal = float(data.get('principal', 0))
        rate = float(data.get('rate', 0))
        tenure = int(data.get('tenure', 0))

        if principal <= 0 or rate <= 0 or tenure <= 0:
            return jsonify({'error': 'Invalid input values'}), 400

        emi = calculate_emi(principal, rate, tenure)
        return jsonify({'emi': emi})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
