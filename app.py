from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3
import webbrowser

app = Flask(__name__)

conn = sqlite3.connect('form_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        p_date DATE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS stk_game (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        g_name TEXT NOT NULL,
        stock_id INTEGER,
        number INTEGER NOT NULL,
        unit INTEGER NOT NULL,
        unit_price INTEGER NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock_data(id)
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
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')

        current_date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO stock_data (p_date, first_name, last_name)
            VALUES (?, ?, ?)
        ''', (current_date, first_name, last_name))
        conn.commit()

        stock_data_id = cursor.lastrowid

        duplicate_games = request.form.getlist('gameName[]')
        duplicate_numbers = request.form.getlist('number[]')
        duplicate_units = request.form.getlist('unit[]')   
        duplicate_unit_prices = request.form.getlist('unitPrice[]')  

        for i in range(len(duplicate_games)):  
            cursor.execute('''
                INSERT INTO stk_game (g_name, stock_id, number, unit, unit_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (duplicate_games[i], stock_data_id, duplicate_numbers[i], duplicate_units[i], duplicate_unit_prices[i]))
            conn.commit()

        conn.close()
        return redirect('/client')

    return render_template('c_add.html')

@app.route('/client/view')
def view_client():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM stock_data ORDER BY p_date DESC')
    users = cursor.fetchall()

    users_with_games = []
    for user in users:
        cursor.execute('SELECT * FROM stk_game WHERE stock_id = ?', (user[0],))
        games = cursor.fetchall()

        user_with_games = {
            'id': user[0],
            'p_date': user[1],
            'first_name': user[2],
            'last_name': user[3],
            'games': games
        }

        users_with_games.append(user_with_games)

    conn.close()

    return render_template('c_view.html', users=users_with_games)

@app.route('/client/view/<int:id>')
def view_c_game(id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM stk_game WHERE stock_id = ?', (id,))
    games = cursor.fetchall()

    conn.close()

    return render_template('c_view_id.html', games=games)

@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/stock/add')
def add_stock():
    return render_template('s_add.html')

@app.route('/stock/view')
def view_stock():
    return render_template('s_view.html')



# webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    app.run(debug=True)
