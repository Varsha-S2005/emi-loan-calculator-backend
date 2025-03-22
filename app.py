from flask import Flask, request, jsonify
import math

app = Flask(__name__)

def calculate_emi(principal, rate, time):
    try:
        rate = rate / (12 * 100)  # Monthly interest rate
        time = time * 12  # Loan tenure in months
        emi = (principal * rate * math.pow(1 + rate, time)) / (math.pow(1 + rate, time) - 1)
        return round(emi, 2)
    except Exception as e:
        print(f"Error calculating EMI: {str(e)}")
        raise

def generate_amortization_schedule(principal, rate, time, emi):
    try:
        rate = rate / (12 * 100)  # Monthly interest rate
        balance = principal
        schedule = []

        for month in range(1, time * 12 + 1):
            interest_payment = round(balance * rate, 2)
            principal_payment = round(emi - interest_payment, 2)
            balance = round(balance - principal_payment, 2)

            if balance < 0:
                balance = 0

            schedule.append({
                "month": month,
                "emi": round(emi, 2),
                "interest_payment": interest_payment,
                "principal_payment": principal_payment,
                "balance": balance
            })

        return schedule
    except Exception as e:
        print(f"Error generating amortization schedule: {str(e)}")
        raise

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi_endpoint():
    try:
        data = request.get_json()
        print("Received data:", data)  # Log received data

        # Ensure all necessary keys are present
        if not all(key in data for key in ['principal', 'rate', 'time']):
            raise ValueError("Missing required fields: principal, rate, or time")

        # Parse the input data
        principal = float(data.get('principal', 0))
        rate = float(data.get('rate', 0))
        time = float(data.get('time', 0))

        # Validate input values
        if principal <= 0 or rate <= 0 or time <= 0:
            raise ValueError("Principal, rate, and time must be positive numbers")

        # Calculate EMI and schedule
        emi = calculate_emi(principal, rate, time)
        schedule = generate_amortization_schedule(principal, rate, int(time), emi)

        print(f"EMI: {emi}, Schedule Length: {len(schedule)}")  # Log calculated results
        return jsonify({"emi": emi, "schedule": schedule})

    except Exception as e:
        print(f"Error in calculate_emi_endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
