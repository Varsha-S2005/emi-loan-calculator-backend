from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    data = request.get_json()
    principal = float(data.get('principal', 0))
    rate = float(data.get('rate', 0))
    tenure = float(data.get('tenure', 0))

    if principal <= 0 or rate <= 0 or tenure <= 0:
        return jsonify({'error': 'Invalid input values.'})

    monthly_rate = rate / (12 * 100)  # Annual rate to monthly
    months = tenure * 12  # Years to months

    try:
        emi = (principal * monthly_rate * pow(1 + monthly_rate, months)) / (pow(1 + monthly_rate, months) - 1)
        return jsonify({'emi': round(emi, 2)})
    except ZeroDivisionError:
        return jsonify({'error': 'Calculation error.'})

if __name__ == '__main__':
    app.run(debug=True)
