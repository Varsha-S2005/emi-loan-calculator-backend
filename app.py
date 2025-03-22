from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate-emi', methods=['POST'])
def calculate_emi():
    data = request.get_json()
    principal = float(data['principal'])
    rate = float(data['rate']) / 12 / 100
    tenure = int(data['tenure'])

    # EMI formula
    emi = (principal * rate * (1 + rate) ** tenure) / ((1 + rate) ** tenure - 1)

    return jsonify({'emi': round(emi, 2)})

if __name__ == '__main__':
    app.run(debug=True)
