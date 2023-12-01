from flask import Flask, render_template, request, redirect
import sqlite3
import webbrowser

app = Flask(__name__)

# Create SQLite database and table
conn = sqlite3.connect('form_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        game TEXT NOT NULL,
        number INTEGER NOT NULL,
        unit INTEGER NOT NULL,
        unit_price INTEGER NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        password = request.form.get('pass')
        if password == 'admin':
            return redirect('/main')
    return render_template('login.html')
        
@app.route('/main')
def homepage():
    return render_template('main.html')

@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/client/add', methods=['POST', 'GET'])
def add_client():
    if request.method == 'POST':
        # Handle form submission
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        game = request.form.get('game')
        number = int(request.form.get('number'))
        unit = int(request.form.get('unit'))
        unit_price = int(request.form.get('unitPrice'))

        # Insert form data into the database
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO stock_data (first_name, last_name, game, number, unit, unit_price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, game, number, unit, unit_price))
        conn.commit()
        conn.close()
        return redirect('/client')

    return render_template('c_add.html')

@app.route('/client/view')
def view_client():
    return render_template('c_view.html')


# webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    app.run(debug=True)
