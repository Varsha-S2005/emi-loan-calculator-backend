from flask import Flask, request, jsonify, render_template
import math
import mysql.connector
import os

app = Flask(__name__)

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="loan_emi_db"
)

cursor = db.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS loan_emis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    principal_amount FLOAT NOT NULL,
    interest_rate FLOAT NOT NULL,
    tenure_years INT NOT NULL,
    emi FLOAT NOT NULL
)
""")
db.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate_emi', methods=['POST'])
def calculate_emi():
    try:
        data = request.get_json()
        principal = float(data['principal'])
        rate = float(data['rate'])
        tenure = int(data['tenure'])

        # Monthly interest rate
        monthly_rate = rate / (12 * 100)

        # Number of months
        tenure_months = tenure * 12

        # EMI calculation formula
        emi = (principal * monthly_rate * math.pow(1 + monthly_rate, tenure_months)) / (math.pow(1 + monthly_rate, tenure_months) - 1)

        # Save EMI data to database
        cursor.execute("INSERT INTO loan_emis (principal_amount, interest_rate, tenure_years, emi) VALUES (%s, %s, %s, %s)",
                       (principal, rate, tenure, emi))
        db.commit()

        return jsonify({"emi": round(emi, 2)})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
