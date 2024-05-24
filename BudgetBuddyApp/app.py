from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulasi data pengguna
transactions = []

@app.route('/')
def index():
    total_income = sum(item['amount'] for item in transactions if item['type'] == 'income')
    total_expense = sum(item['amount'] for item in transactions if item['type'] == 'expense')
    balance = total_income - total_expense
    return render_template('index.html', transactions=transactions, balance=balance)

@app.route('/add', methods=['POST'])
def add_transaction():
    type_ = request.form['type']
    amount = float(request.form['amount'])
    description = request.form['description']
    transactions.append({'type': type_, 'amount': amount, 'description': description})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
