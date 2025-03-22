from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        data = request.get_json()
        principal = float(data['principal'])
        rate = float(data['rate'])
        time = float(data['time'])

        # Convert annual rate to monthly and calculate EMI
        monthly_rate = rate / (12 * 100)
        months = time * 12
        emi = (principal * monthly_rate * math.pow(1 + monthly_rate, months)) / (math.pow(1 + monthly_rate, months) - 1)

        return jsonify({"emi": round(emi, 2)})
    except Exception as e:
        return jsonify({"error": "Error calculating EMI: " + str(e)})

if __name__ == "__main__":
    app.run(debug=True)
