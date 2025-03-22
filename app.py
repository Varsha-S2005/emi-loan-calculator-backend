from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    data = request.get_json()
    principal = data.get("principal")
    rate = data.get("rate")
    years = data.get("years")

    try:
        rate = rate / (12 * 100)
        months = years * 12
        emi = (principal * rate * (1 + rate)**months) / (((1 + rate)**months) - 1)
        return jsonify({"emi": round(emi, 2)})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
