from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        data = request.get_json()
        principal = float(data.get("principal", 0))
        rate = float(data.get("rate", 0)) / 12 / 100
        time = float(data.get("time", 0)) * 12

        if principal <= 0 or rate <= 0 or time <= 0:
            return jsonify({"error": "Invalid input values"}), 400

        emi = (principal * rate * (1 + rate) ** time) / ((1 + rate) ** time - 1)
        return jsonify({"emi": round(emi, 2)}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
