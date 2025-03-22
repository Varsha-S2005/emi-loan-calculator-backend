from flask import Flask, request, jsonify
import math

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate_emi():
    data = request.get_json()
    principal = float(data['principal'])
    rate = float(data['rate']) / 12 / 100
    time = int(data['time']) * 12

    emi = (principal * rate * math.pow(1 + rate, time)) / (math.pow(1 + rate, time) - 1)
    total_payment = emi * time
    total_interest = total_payment - principal

    # Amortization Schedule
    balance = principal
    amortization_schedule = []

    for month in range(1, time + 1):
        interest_payment = balance * rate
        principal_payment = emi - interest_payment
        balance -= principal_payment
        amortization_schedule.append({
            "month": month,
            "emi": round(emi, 2),
            "interest_payment": round(interest_payment, 2),
            "principal_payment": round(principal_payment, 2),
            "balance": round(balance, 2)
        })

    return jsonify({
        "emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "amortization_schedule": amortization_schedule
    })

if __name__ == '__main__':
    app.run(debug=True)
