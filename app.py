from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        data = request.get_json()
        principal = float(data['principal'])
        rate = float(data['rate']) / 12 / 100
        time = float(data['time']) * 12

        # EMI Calculation
        emi = (principal * rate * (1 + rate) ** time) / ((1 + rate) ** time - 1)
        
        return jsonify({"emi": round(emi, 2)})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Calculation failed"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
