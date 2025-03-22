from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        data = request.get_json()
        principal = float(data.get('principal', 0))
        rate = float(data.get('rate', 0))
        time = float(data.get('time', 0))

        if principal <= 0 or rate <= 0 or time <= 0:
            return jsonify({"error": "Invalid input values"}), 400

        monthly_rate = rate / (12 * 100)  # Monthly interest rate
        tenure_months = time * 12  # Convert years to months

        emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
              ((1 + monthly_rate) ** tenure_months - 1)

        return jsonify({"emi": round(emi, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
