from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Loan EMI Calculator!"

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract the principal, rate, and time from the JSON data
        principal = float(data.get('principal'))
        rate = float(data.get('rate')) / 100 / 12  # Annual rate to monthly rate
        time = float(data.get('time')) * 12  # Years to months

        # EMI calculation formula
        emi = (principal * rate * (1 + rate)**time) / ((1 + rate)**time - 1)

        # Return the EMI as a JSON response
        return jsonify({"emi": round(emi, 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
