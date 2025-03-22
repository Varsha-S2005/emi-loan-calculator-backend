from flask import Flask, request, jsonify
import math

app = Flask(__name__)

def calculate_emi(principal, rate, time):
    rate = rate / (12 * 100)  # Monthly interest rate
    time = time * 12  # Loan tenure in months
    emi = (principal * rate * math.pow(1 + rate, time)) / (math.pow(1 + rate, time) - 1)
    return round(emi, 2)

def generate_amortization_schedule(principal, rate, time, emi):
    rate = rate / (12 * 100)  # Monthly interest rate
    balance = principal
    schedule = []

    for month in range(1, time * 12 + 1):
        interest_payment = round(balance * rate, 2)
        principal_payment = round(emi - interest_payment, 2)
        balance = round(balance - principal_payment, 2)

        schedule.append({
            "month": month,
            "emi": round(emi, 2),
            "interest_payment": interest_payment,
            "principal_payment": principal_payment,
            "balance": max(balance, 0)  # Ensure balance never goes negative
        })

    return schedule

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi_endpoint():
    try:
        data = request.get_json()
        principal = float(data['principal'])
        rate = float(data['rate'])
        time = int(data['time'])

        emi = calculate_emi(principal, rate, time)
        schedule = generate_amortization_schedule(principal, rate, time, emi)

        return jsonify({"emi": emi, "schedule": schedule})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
