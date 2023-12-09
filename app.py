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
        payment INTEGER NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock_data(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS your_table_name (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        MM_super_st INTEGER NOT NULL,
        MM_super_e INTEGER NOT NULL,
        MM_super_so INTEGER NOT NULL,
        MM_Fardeaux_st INTEGER NOT NULL,
        MM_Fardeaux_e INTEGER NOT NULL,
        MM_Fardeaux_so INTEGER NOT NULL,
        GMM_st INTEGER NOT NULL,
        GMM_e INTEGER NOT NULL,
        GMM_so INTEGER NOT NULL,
        GMM_x25_st INTEGER NOT NULL,
        GMM_x25_e INTEGER NOT NULL,
        GMM_x25_so INTEGER NOT NULL,
        GMM_x30_st INTEGER NOT NULL,
        GMM_x30_e INTEGER NOT NULL,
        GMM_x30_so INTEGER NOT NULL,
        MM_IMP_MANTOUDJ_st INTEGER NOT NULL,
        MM_IMP_MANTOUDJ_e INTEGER NOT NULL,
        MM_IMP_MANTOUDJ_so INTEGER NOT NULL,
        PM_st INTEGER NOT NULL,
        PM_e INTEGER NOT NULL,
        PM_so INTEGER NOT NULL,
        GM_IMP_st INTEGER NOT NULL,
        GM_IMP_e INTEGER NOT NULL,
        GM_IMP_so INTEGER NOT NULL,
        GM_IMP_x20_st INTEGER NOT NULL,
        GM_IMP_x20_e INTEGER NOT NULL,
        GM_IMP_x20_so INTEGER NOT NULL,
        PAIN_st INTEGER NOT NULL,
        PAIN_e INTEGER NOT NULL,
        PAIN_so INTEGER NOT NULL,
        POUBELLE_BASE_st INTEGER NOT NULL,
        POUBELLE_BASE_e INTEGER NOT NULL,
        POUBELLE_BASE_so INTEGER NOT NULL,
        GGM_st INTEGER NOT NULL,
        GGM_e INTEGER NOT NULL,
        GGM_so INTEGER NOT NULL,
        WELCOME_st INTEGER NOT NULL,
        WELCOME_e INTEGER NOT NULL,
        WELCOME_so INTEGER NOT NULL
    )
''')

conn.commit()
conn.close()

def insert_daily_data():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute('SELECT COUNT(*) FROM your_table_name WHERE date = ?', (current_date,))
    count = cursor.fetchone()[0]

    if count == 0:

        cursor.execute('''
            SELECT MM_super_st, MM_super_e, MM_super_so, MM_Fardeaux_st, MM_Fardeaux_e, MM_Fardeaux_so,
                   GMM_st, GMM_e, GMM_so, GMM_x25_st, GMM_x25_e, GMM_x25_so, GMM_x30_st, GMM_x30_e, GMM_x30_so,
                   MM_IMP_MANTOUDJ_st, MM_IMP_MANTOUDJ_e, MM_IMP_MANTOUDJ_so, PM_st, PM_e, PM_so, GM_IMP_st, GM_IMP_e,
                   GM_IMP_so, GM_IMP_x20_st, GM_IMP_x20_e, GM_IMP_x20_so, PAIN_st, PAIN_e, PAIN_so, POUBELLE_BASE_st,
                   POUBELLE_BASE_e, POUBELLE_BASE_so, GGM_st, GGM_e, GGM_so, WELCOME_st, WELCOME_e, WELCOME_so
            FROM your_table_name
            WHERE date = (SELECT MAX(date) FROM your_table_name)
        ''')

        last_day_values = cursor.fetchone()

        if last_day_values:

            MM_super_st = last_day_values[0] + last_day_values[1] - last_day_values[2]
            MM_Fardeaux_st = last_day_values[3] + last_day_values[4] - last_day_values[5]
            GMM_st = last_day_values[6] + last_day_values[7] - last_day_values[8]
            GMM_x25_st = last_day_values[9] + last_day_values[10] - last_day_values[11]
            GMM_x30_st = last_day_values[12] + last_day_values[13] - last_day_values[14]
            MM_IMP_MANTOUDJ_st = last_day_values[15] + last_day_values[16] - last_day_values[17]
            PM_st = last_day_values[18] + last_day_values[19] - last_day_values[20]
            GM_IMP_st = last_day_values[21] + last_day_values[22] - last_day_values[23]
            GM_IMP_x20_st = last_day_values[24] + last_day_values[25] - last_day_values[26]
            PAIN_st = last_day_values[27] + last_day_values[28] - last_day_values[29]
            POUBELLE_BASE_st = last_day_values[30] + last_day_values[31] - last_day_values[32]
            GGM_st = last_day_values[33] + last_day_values[34] - last_day_values[35]
            WELCOME_st = last_day_values[36] + last_day_values[37] - last_day_values[38]


            cursor.execute('''
                INSERT INTO your_table_name (date, MM_super_st, MM_super_e, MM_super_so, MM_Fardeaux_st, MM_Fardeaux_e, MM_Fardeaux_so,
                   GMM_st, GMM_e, GMM_so, GMM_x25_st, GMM_x25_e, GMM_x25_so, GMM_x30_st, GMM_x30_e, GMM_x30_so,
                   MM_IMP_MANTOUDJ_st, MM_IMP_MANTOUDJ_e, MM_IMP_MANTOUDJ_so, PM_st, PM_e, PM_so, GM_IMP_st, GM_IMP_e,
                   GM_IMP_so, GM_IMP_x20_st, GM_IMP_x20_e, GM_IMP_x20_so, PAIN_st, PAIN_e, PAIN_so, POUBELLE_BASE_st,
                   POUBELLE_BASE_e, POUBELLE_BASE_so, GGM_st, GGM_e, GGM_so, WELCOME_st, WELCOME_e, WELCOME_so)
                VALUES (?, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0,
                        ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0)
            ''', (current_date, MM_super_st, MM_Fardeaux_st, GMM_st, GMM_x25_st, GMM_x30_st, MM_IMP_MANTOUDJ_st, PM_st, GM_IMP_st, GM_IMP_x20_st, PAIN_st, POUBELLE_BASE_st, GGM_st, WELCOME_st))

            conn.commit()

    conn.close()

insert_daily_data()

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
                INSERT INTO stk_game (g_name, stock_id, number, unit, unit_price, payment)
                VALUES (?, ?, ?, ?, ?, 0)
            ''', (duplicate_games[i], stock_data_id, duplicate_numbers[i], duplicate_units[i], duplicate_unit_prices[i]))
            conn.commit()

            updated_game = duplicate_games[i].replace(' ', '_') + '_so'
            cursor.execute(f"SELECT {updated_game} FROM your_table_name WHERE date = ?", (current_date,))
            old_v = cursor.fetchone()
            
            if old_v:
                new_v = old_v[0] + int(duplicate_numbers[i])
                cursor.execute(f"UPDATE your_table_name SET {updated_game} = ? WHERE date = ?", (new_v, current_date))
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
        sold = 0
        total = 0
        for game in games:
            total = total + (game[3]*game[4]*game[5])
            sold = sold + game[6]

        sold = total - sold

        user_with_games = {
            'id': user[0],
            'p_date': user[1],
            'first_name': user[2],
            'last_name': user[3],
            'sold': sold,
            'total': total
        }

        users_with_games.append(user_with_games)

    conn.close()

    return render_template('c_view.html', users=users_with_games)

@app.route('/client/view/<int:id>')
def view_c_game(id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT first_name, last_name, p_date FROM stock_data WHERE id = ?', (id,))
    user_data = cursor.fetchone()

    cursor.execute('SELECT * FROM stk_game WHERE stock_id = ?', (id,))
    games = cursor.fetchall()

    conn.close()

    return render_template('c_view_id.html', user_data=user_data, games=games)

@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/stock/add', methods=['POST', 'GET'])
def add_stock():
    if request.method == 'POST':
        current_date = datetime.now().strftime("%Y-%m-%d")

        duplicate_games = request.form.getlist('gameName[]')
        duplicate_numbers = request.form.getlist('number[]')

        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        for i in range(len(duplicate_games)):  
            updated_game = duplicate_games[i].replace(' ', '_') + '_e'
            cursor.execute(f"SELECT {updated_game} FROM your_table_name WHERE date = ?", (current_date,))
            old_v = cursor.fetchone()
            
            if old_v:
                new_v = old_v[0] + int(duplicate_numbers[i])
                cursor.execute(f"UPDATE your_table_name SET {updated_game} = ? WHERE date = ?", (new_v, current_date))
                conn.commit()

        conn.close()
        return redirect('/stock')

    return render_template('s_add.html')

@app.route('/stock/view')
def view_stock():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    today_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute('SELECT * FROM your_table_name WHERE date = ?', (today_date,))
    stock_data = cursor.fetchone()

    conn.close()

    return render_template('s_view.html', stock_data=stock_data)






# webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    app.run(debug=True)
