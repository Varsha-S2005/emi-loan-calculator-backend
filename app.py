from flask import Flask, request, jsonify
import math

app = Flask(__name__)

# Function to calculate EMI
def calculate_emi(principal, rate, time):
    try:
        rate = rate / (12 * 100)  # Monthly interest rate
        time = time * 12  # Loan tenure in months
        emi = (principal * rate * math.pow(1 + rate, time)) / (math.pow(1 + rate, time) - 1)
        return round(emi, 2)
    except Exception as e:
        print(f"Error in EMI calculation: {str(e)}")
        return None

# Function to generate the amortization schedule
def generate_amortization_schedule(principal, rate, time, emi):
    try:
        rate = rate / (12 * 100)  # Monthly interest rate
        balance = principal
        schedule = []

        for month in range(1, time * 12 + 1):
            interest_payment = round(balance * rate, 2)
            principal_payment = round(emi - interest_payment, 2)
            balance = round(balance - principal_payment, 2)
            balance = max(balance, 0)  # Ensure balance never goes negative

            schedule.append({
                "month": month,
                "emi": round(emi, 2),
                "interest_payment": interest_payment,
                "principal_payment": principal_payment,
                "balance": balance
            })

        return schedule
    except Exception as e:
        print(f"Error in amortization schedule calculation: {str(e)}")
        return []

# Endpoint to calculate EMI and schedule
@app.route('/calculate_emi', methods=['POST'])
def calculate_emi_endpoint():
    try:
        data = request.get_json()
        print("Received data:", data)

        # Validate input
        principal = float(data.get('principal', 0))
        rate = float(data.get('rate', 0))
        time = float(data.get('time', 0))

        if principal <= 0 or rate <= 0 or time <= 0:
            return jsonify({"error": "Principal, rate, and time must be positive numbers"}), 400

        emi = calculate_emi(principal, rate, time)
        if emi is None:
            return jsonify({"error": "Error in calculating EMI"}), 400

        schedule = generate_amortization_schedule(principal, rate, int(time), emi)
        return jsonify({"emi": emi, "schedule": schedule})

    except Exception as e:
        print(f"Error in endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
