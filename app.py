from flask import Flask, request, jsonify
import math

app = Flask(__name__)

def calculate_emi(principal, rate, time):
    rate = rate / (12 * 100)  # Convert annual rate to monthly rate
    time = time * 12  # Convert years to months
    emi = (principal * rate * math.pow(1 + rate, time)) / (math.pow(1 + rate, time) - 1)
    return round(emi, 2)

def generate_amortization_schedule(principal, rate, time, emi):
    rate = rate / (12 * 100)  # Convert annual rate to monthly rate
    balance = principal
    schedule = []

    for month in range(1, time * 12 + 1):
        interest_payment = round(balance * rate, 2)
        principal_payment = round(emi - interest_payment, 2)
        balance = round(balance - principal_payment, 2)
        # Ensure balance never goes negative
        balance = max(balance, 0)

        schedule.append({
            "month": month,
            "emi": round(emi, 2),
            "interest_payment": interest_payment,
            "principal_payment": principal_payment,
            "balance": balance
        })

        # Stop schedule if the balance is zero to avoid unnecessary iterations
        if balance <= 0:
            break

    return schedule

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi_endpoint():
    try:
        data = request.get_json()
        if not all(key in data for key in ['principal', 'rate', 'time']):
            raise ValueError("Missing required data fields: principal, rate, or time")

        principal = float(data['principal'])
        rate = float(data['rate'])
        time = float(data['time'])  # Use float to avoid issues with decimal inputs

        if principal <= 0 or rate <= 0 or time <= 0:
            raise ValueError("Principal, rate, and time must be positive numbers")

        emi = calculate_emi(principal, rate, time)
        schedule = generate_amortization_schedule(principal, rate, int(time), emi)

        return jsonify({"emi": emi, "schedule": schedule})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
