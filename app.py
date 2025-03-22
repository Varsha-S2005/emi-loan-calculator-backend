from flask import Flask, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate_emi():
    data = request.get_json()
    principal = float(data['principal'])
    rate = float(data['rate'])
    time = int(data['time'])

    emi = (principal * rate * math.pow(1 + rate, time)) / (math.pow(1 + rate, time) - 1)
    total_payment = emi * time
    total_interest = total_payment - principal

    schedule = []
    balance = principal
    for month in range(1, time + 1):
        interest = balance * rate
        principal_paid = emi - interest
        balance -= principal_paid
        schedule.append({
            "principal": principal_paid,
            "interest": interest,
            "balance": max(0, balance)
        })

    return jsonify({"emi": emi, "totalInterest": total_interest, "schedule": schedule})

if __name__ == '__main__':
    app.run(debug=True)
