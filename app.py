from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        data = request.get_json()
        principal = float(data.get('principal', 0))
        rate = float(data.get('rate', 0))
        tenure = int(data.get('tenure', 0))

        if principal <= 0 or rate <= 0 or tenure <= 0:
            return jsonify({'error': 'Invalid input values. Please enter positive numbers.'})

        monthly_rate = rate / (12 * 100)  # Convert annual rate to monthly and percentage to decimal
        tenure_months = tenure * 12

        emi = principal * monthly_rate * math.pow(1 + monthly_rate, tenure_months) / (math.pow(1 + monthly_rate, tenure_months) - 1)
        emi = round(emi, 2)  # Round to two decimal places

        return jsonify({'emi': emi})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
