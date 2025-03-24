from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        data = request.get_json()
        principal = float(data['principal'])
        rate = float(data['rate'])
        tenure = float(data['tenure'])

        # Convert annual rate to monthly and calculate tenure in months
        monthly_rate = rate / (12 * 100)
        months = tenure * 12

        # EMI formula
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        emi = round(emi, 2)

        return jsonify({'emi': emi})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
