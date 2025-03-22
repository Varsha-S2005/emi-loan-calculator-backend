from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        data = request.get_json()
        principal = float(data['principal'])
        rate = float(data['rate']) / 12 / 100
        time = float(data['time']) * 12

        # EMI calculation
        emi = (principal * rate * math.pow(1 + rate, time)) / (math.pow(1 + rate, time) - 1)
        emi = round(emi, 2)

        return jsonify({'emi': emi})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
