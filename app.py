from flask import Flask, render_template, request, redirect, jsonify, Response
from fpdf import FPDF
from datetime import datetime, timedelta
import webview
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('form_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        p_date DATE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        payment REAL NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS client (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        p_date TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS client_games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        game_name TEXT NOT NULL,
        number INTEGER NOT NULL,
        unit REAL NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (client_id) REFERENCES client(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS worker (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS game (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        unit REAL NOT NULL,
        unitPrice REAL NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS w_time (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER,
        t_type TEXT NOT NULL,
        date TEXT NOT NULL,
        entree_time TEXT NOT NULL,
        exit_time TEXT NOT NULL,
        emargement TEXT,
        observation TEXT,
        FOREIGN KEY (worker_id) REFERENCES worker(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS stk_game (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        g_name TEXT NOT NULL,
        stock_id INTEGER,
        number INTEGER NOT NULL,
        unit INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES stock_data(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS payment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        date TEXT NOT NULL,
        pay REAL NOT NULL,
        FOREIGN KEY (client_id) REFERENCES client(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS stv (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
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
        POUBELLE_st INTEGER NOT NULL,
        POUBELLE_e INTEGER NOT NULL,
        POUBELLE_so INTEGER NOT NULL,
        CONGELATION_st INTEGER NOT NULL,
        CONGELATION_e INTEGER NOT NULL,
        CONGELATION_so INTEGER NOT NULL,
        GGM_st INTEGER NOT NULL,
        GGM_e INTEGER NOT NULL,
        GGM_so INTEGER NOT NULL,
        WELCOME_st INTEGER NOT NULL,
        WELCOME_e INTEGER NOT NULL,
        WELCOME_so INTEGER NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS upt (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        num INTEGER NOT NULL,
        u INTEGER NOT NULL,
        up REAL NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS d_mat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        t_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        p_num INTEGER NOT NULL,
        nember_d_m INTEGER,
        poid_udm REAL,
        poid_f REAL,
        number_f_r REAL,
        poid_feb REAL,
        poid_be REAL,
        poid_bu REAL,
        stock INTEGER,
        unit REAL,
        p_unit REAL
    )
''')

conn.commit()
conn.close()

def insert_daily_data():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('SELECT * FROM stv')
    test = cursor.fetchone()

    if test is None:
        cursor.execute('''
            INSERT INTO stv (
                date,
                MM_super_st, MM_super_e, MM_super_so,
                MM_Fardeaux_st, MM_Fardeaux_e, MM_Fardeaux_so,
                GMM_st, GMM_e, GMM_so,
                GMM_x25_st, GMM_x25_e, GMM_x25_so,
                GMM_x30_st, GMM_x30_e, GMM_x30_so,
                MM_IMP_MANTOUDJ_st, MM_IMP_MANTOUDJ_e, MM_IMP_MANTOUDJ_so,
                PM_st, PM_e, PM_so,
                GM_IMP_st, GM_IMP_e, GM_IMP_so,
                GM_IMP_x20_st, GM_IMP_x20_e, GM_IMP_x20_so,
                PAIN_st, PAIN_e, PAIN_so,
                POUBELLE_BASE_st, POUBELLE_BASE_e, POUBELLE_BASE_so,
                POUBELLE_st, POUBELLE_e, POUBELLE_so,
                CONGELATION_st, CONGELATION_e, CONGELATION_so,
                GGM_st, GGM_e, GGM_so,
                WELCOME_st, WELCOME_e, WELCOME_so
            ) VALUES (?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        ''', ( current_date,))
        
        for i in range(15):
            cursor.execute('''
                INSERT INTO upt (date, num, u, up)
                VALUES (?, ?, 0, 0)
            ''',(current_date, i))

    cursor.execute('SELECT COUNT(*) FROM stv WHERE date = ?', (current_date,))
    count = cursor.fetchone()[0]

    if count == 0:

        cursor.execute('''
            SELECT MM_super_st, MM_super_e, MM_super_so, MM_Fardeaux_st, MM_Fardeaux_e, MM_Fardeaux_so,
                   GMM_st, GMM_e, GMM_so, GMM_x25_st, GMM_x25_e, GMM_x25_so, GMM_x30_st, GMM_x30_e, GMM_x30_so,
                   MM_IMP_MANTOUDJ_st, MM_IMP_MANTOUDJ_e, MM_IMP_MANTOUDJ_so, PM_st, PM_e, PM_so, GM_IMP_st, GM_IMP_e,
                   GM_IMP_so, GM_IMP_x20_st, GM_IMP_x20_e, GM_IMP_x20_so, PAIN_st, PAIN_e, PAIN_so, POUBELLE_BASE_st,
                   POUBELLE_BASE_e, POUBELLE_BASE_so, POUBELLE_st, POUBELLE_e, POUBELLE_so, CONGELATION_st, CONGELATION_e,
                   CONGELATION_so, GGM_st, GGM_e, GGM_so, WELCOME_st, WELCOME_e, WELCOME_so
            FROM stv
            WHERE date = (SELECT MAX(date) FROM stv)
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
            POUBELLE_st = last_day_values[33] + last_day_values[34] - last_day_values[35]
            CONGELATION_st = last_day_values[36] + last_day_values[37] - last_day_values[38]
            GGM_st = last_day_values[39] + last_day_values[40] - last_day_values[41]
            WELCOME_st = last_day_values[42] + last_day_values[43] - last_day_values[44]


            cursor.execute('''
                INSERT INTO stv (date, MM_super_st, MM_super_e, MM_super_so, MM_Fardeaux_st, MM_Fardeaux_e, MM_Fardeaux_so,
                   GMM_st, GMM_e, GMM_so, GMM_x25_st, GMM_x25_e, GMM_x25_so, GMM_x30_st, GMM_x30_e, GMM_x30_so,
                   MM_IMP_MANTOUDJ_st, MM_IMP_MANTOUDJ_e, MM_IMP_MANTOUDJ_so, PM_st, PM_e, PM_so, GM_IMP_st, GM_IMP_e,
                   GM_IMP_so, GM_IMP_x20_st, GM_IMP_x20_e, GM_IMP_x20_so, PAIN_st, PAIN_e, PAIN_so, POUBELLE_BASE_st,
                   POUBELLE_BASE_e, POUBELLE_BASE_so, POUBELLE_st, POUBELLE_e, POUBELLE_so, CONGELATION_st, CONGELATION_e,
                   CONGELATION_so, GGM_st, GGM_e, GGM_so, WELCOME_st, WELCOME_e, WELCOME_so)
                VALUES (?, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0,
                        ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0, ?, 0, 0)
            ''', (current_date, MM_super_st, MM_Fardeaux_st, GMM_st, GMM_x25_st, GMM_x30_st, MM_IMP_MANTOUDJ_st, PM_st, GM_IMP_st, GM_IMP_x20_st, PAIN_st, POUBELLE_BASE_st, POUBELLE_st, CONGELATION_st, GGM_st, WELCOME_st))


    cursor.execute('SELECT COUNT(*) FROM upt WHERE date = ?', (current_date,))
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('''
            SELECT u, up FROM upt WHERE date = (SELECT MAX(date) FROM upt)
        ''')

        last_day_values = cursor.fetchall()

        if last_day_values:
            for i in range(15):
                cursor.execute('''
                    INSERT INTO upt (date, num, u, up)
                    VALUES (?, ?, ?, ?)
                ''',(current_date, i, last_day_values[i][0], last_day_values[i][1]))


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

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/game/add', methods=['POST', 'GET'])
def add_game():
    if request.method == 'POST':
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO game(name, unit, unitPrice) VALUES(?, ?, ?)', (request.form.get('name'), request.form.get('unite'), request.form.get('punit')))
        conn.commit()
        conn.close()
        return redirect('/game')
    return render_template('g_add.html')

@app.route('/game/edit')
def edit_game():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM game')
    data_f = cursor.fetchall()
    games = []

    for data in data_f:
        game = {
            'id': data[0],
            'name': data[1],
            'unit': data[2],
            'price': data[3],
        }
        games.append(game)

    conn.close()
    return render_template('g_edit.html', games=games)

@app.route('/game/edit/<int:id>', methods=['POST', 'GET'])
def edit_game_id(id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        cursor.execute('UPDATE game set name = ?, unit = ?, unitPrice = ? WHERE id = ?', (request.form.get('name'), request.form.get('unite'), request.form.get('punit'), id))
        conn.commit()
        conn.close()
        return redirect('/game')

    cursor.execute('SELECT * FROM game WHERE id = ?', (id, ))
    data_f = cursor.fetchone()
    game = {
        'id': data_f[0],
        'name': data_f[1],
        'unit': data_f[2],
        'price': data_f[3],
    }

    conn.close()
    return render_template('g_modify.html', id=data_f[0], game=game)

@app.route('/game/remove')
def remove_game():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM game')
    data_f = cursor.fetchall()
    games = []

    for data in data_f:
        game = {
            'id': data[0],
            'name': data[1],
            'unit': data[2],
            'price': data[3],
        }
        games.append(game)

    conn.close()
    return render_template('g_remove.html', games=games)

@app.route('/game/remove/<int:id>')
def remove_game_id(id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM game WHERE id = ?', (id, ))
    conn.commit()
    conn.close()

    return redirect('/game')

@app.route('/main')
def homepage():
    return render_template('main.html')

@app.route('/game/view')
def view_game():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM game')
    data_f = cursor.fetchall()
    games = []

    for data in data_f:
        game = {
            'id': data[0],
            'name': data[1],
            'unit': data[2],
            'price': data[3],
        }
        games.append(game)

    conn.close()
    return render_template('g_view.html', games=games)

    ### client ### 

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
            INSERT INTO client (p_date, first_name, last_name)
            VALUES (?, ?, ?)
        ''', (current_date, first_name, last_name))
        conn.commit()

        client_id = cursor.lastrowid

        games = request.form.getlist('gameName[]')
        numbers = request.form.getlist('number[]')
        units = request.form.getlist('unit[]')   
        unit_prices = request.form.getlist('unitPrice[]')  

        for i in range(len(games)):  
            cursor.execute('SELECT name FROM game WHERE id = ?', (games[i], ))
            game=cursor.fetchone()[0]
            cursor.execute('''
                INSERT INTO client_games (client_id, game_name, number, unit, unit_price)
                VALUES (?, ?, ?, ?, ?)
            ''',
            (client_id, game, numbers[i], units[i], unit_prices[i]))
            conn.commit()

        conn.close()
        return redirect('/client')

    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM game')

    datas = cursor.fetchall()
    games = []

    for data in datas:
        game={
            'id': data[0],
            'game': data[1],
            'unit':data[2],
            'unitp':data[3],
        }
        games.append(game)


    return render_template('c_add.html', games=games)

@app.route('/client/edit', methods=['POST', 'GET'])
def edit_client():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        search_date = request.form.get('search_date', None)
        search_name = request.form.get('search_name', None)

        if search_date and search_name:
            cursor.execute('SELECT * FROM client WHERE p_date = ? AND (first_name LIKE ? OR last_name LIKE ?) ORDER BY p_date DESC',(search_date, f'%{search_name}%', f'%{search_name}%'))
        elif search_date:
            cursor.execute('SELECT * FROM client WHERE p_date = ? ORDER BY p_date DESC', (search_date,))
        elif search_name:
            cursor.execute('SELECT * FROM client WHERE first_name LIKE ? OR last_name LIKE ? ORDER BY p_date DESC',
                           (f'%{search_name}%', f'%{search_name}%'))
        else:
            cursor.execute('SELECT * FROM client ORDER BY p_date DESC')
    else:
        cursor.execute('SELECT * FROM client ORDER BY p_date DESC')

    datas = cursor.fetchall()

    users = []
    for data in datas:
        cursor.execute('SELECT * FROM client_games WHERE client_id = ?', (data[0],))
        games = cursor.fetchall()
        cursor.execute('SELECT pay FROM payment WHERE client_id = ?', (data[0],))
        payment=0
        pays=cursor.fetchall()
        for pay in pays:
            payment += pay[0]
        sold = 0
        total = 0
        for game in games:
            total = total + (game[3]*game[4]*game[5])

        sold = total - payment

        user = {
            'id': data[0],
            'p_date': data[1],
            'first_name': data[2],
            'last_name': data[3],
            'pay': payment,
            'sold': sold,
            'total': total
        }

        users.append(user)

    conn.close()


    return render_template('c_edit.html', users=users)

@app.route('/client/edit/<int:id>', methods=['POST', 'GET'])
def modify_client(id):
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')

        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE client SET first_name = ?, last_name = ? WHERE id = ?
        ''', (first_name, last_name, id))
        conn.commit()

        games = request.form.getlist('gameName[]')
        numbers = request.form.getlist('number[]')
        units = request.form.getlist('unit[]')   
        unit_prices = request.form.getlist('unitPrice[]')  

        cursor.execute('DELETE FROM client_games WHERE client_id = ?', (id, ))

        for i in range(len(games)):  
            cursor.execute('SELECT name FROM game WHERE id = ?', (games[i], ))
            game=cursor.fetchone()[0]
            cursor.execute('''
                INSERT INTO client_games (client_id, game_name, number, unit, unit_price)
                VALUES (?, ?, ?, ?, ?)
            ''',
            (id, game, numbers[i], units[i], unit_prices[i]))
            conn.commit()

        conn.close()
        return redirect('/client')

    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM game')

    datas = cursor.fetchall()
    games = []

    for data in datas:
        game={
            'id': data[0],
            'game': data[1],
            'unit':data[2],
            'unitp':data[3],
        }
        games.append(game)
    
    cursor.execute('SELECT game_name, number, unit, unit_price FROM client_games WHERE client_id = ?', (id, ))
    datas = cursor.fetchall()
    lastgames = []

    for data in datas:
        game={
            'name':data[0],
            'number':data[1],
            'unit':data[2],
            'unitp':data[3],
        }
        lastgames.append(game)

    cursor.execute('SELECT first_name, last_name FROM client WHERE id = ?', (id, ))
    fullname = cursor.fetchone()

    return render_template('c_modify.html', games=games, lastgames=enumerate(lastgames), name=fullname, id=id)


@app.route('/client/remove', methods=['POST', 'GET'])
def remove_client():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        search_date = request.form.get('search_date', None)
        search_name = request.form.get('search_name', None)

        if search_date and search_name:
            cursor.execute('SELECT * FROM client WHERE p_date = ? AND (first_name LIKE ? OR last_name LIKE ?) ORDER BY p_date DESC',(search_date, f'%{search_name}%', f'%{search_name}%'))
        elif search_date:
            cursor.execute('SELECT * FROM client WHERE p_date = ? ORDER BY p_date DESC', (search_date,))
        elif search_name:
            cursor.execute('SELECT * FROM client WHERE first_name LIKE ? OR last_name LIKE ? ORDER BY p_date DESC',
                           (f'%{search_name}%', f'%{search_name}%'))
        else:
            cursor.execute('SELECT * FROM client ORDER BY p_date DESC')
    else:
        cursor.execute('SELECT * FROM client ORDER BY p_date DESC')

    datas = cursor.fetchall()

    users = []
    for data in datas:
        cursor.execute('SELECT * FROM client_games WHERE client_id = ?', (data[0],))
        games = cursor.fetchall()
        cursor.execute('SELECT pay FROM payment WHERE client_id = ?', (data[0],))
        payment=0
        pays=cursor.fetchall()
        for pay in pays:
            payment += pay[0]
        sold = 0
        total = 0
        for game in games:
            total = total + (game[3]*game[4]*game[5])

        sold = total - payment

        user = {
            'id': data[0],
            'p_date': data[1],
            'first_name': data[2],
            'last_name': data[3],
            'pay': payment,
            'sold': sold,
            'total': total
        }

        users.append(user)

    conn.close()


    return render_template('c_remove.html', users=users)

@app.route('/client/remove/<int:id>')
def del_client(id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM client_games WHERE client_id = ?',(id,))
    cursor.execute('DELETE FROM client WHERE id = ?',(id,))

    conn.commit()
    conn.close()
    return redirect('/client')


@app.route('/client/view', methods=['POST', 'GET'])
def view_client():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        search_date = request.form.get('search_date', None)
        search_name = request.form.get('search_name', None)

        if search_date and search_name:
            cursor.execute('SELECT * FROM client WHERE p_date = ? AND (first_name LIKE ? OR last_name LIKE ?) ORDER BY p_date DESC',(search_date, f'%{search_name}%', f'%{search_name}%'))
        elif search_date:
            cursor.execute('SELECT * FROM client WHERE p_date = ? ORDER BY p_date DESC', (search_date,))
        elif search_name:
            cursor.execute('SELECT * FROM client WHERE first_name LIKE ? OR last_name LIKE ? ORDER BY p_date DESC',
                           (f'%{search_name}%', f'%{search_name}%'))
        else:
            cursor.execute('SELECT * FROM client ORDER BY p_date DESC')
    else:
        cursor.execute('SELECT * FROM client ORDER BY p_date DESC')

    datas = cursor.fetchall()

    users = []
    for data in datas:
        cursor.execute('SELECT * FROM client_games WHERE client_id = ?', (data[0],))
        games = cursor.fetchall()
        cursor.execute('SELECT pay FROM payment WHERE client_id = ?', (data[0],))
        payment=0
        pays=cursor.fetchall()
        for pay in pays:
            payment += pay[0]
        sold = 0
        total = 0
        for game in games:
            total = total + (game[3]*game[4]*game[5])

        sold = total - payment

        user = {
            'id': data[0],
            'p_date': data[1],
            'first_name': data[2],
            'last_name': data[3],
            'pay': payment,
            'sold': sold,
            'total': total
        }

        users.append(user)

    conn.close()

    return render_template('c_view.html', users=users)

@app.route('/client/view/<int:id>', methods=['POST', 'GET'])
def view_c_game(id):
    if request.method == 'POST':
        date = datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()
        pay = request.form.get('pay')
        cursor.execute('''
            INSERT INTO payment (client_id, date, pay)
            VALUES (?, ?, ?)
        ''', (id, date, pay))
        conn.commit()

        conn.close()
        return redirect('/client/view')

    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT first_name, last_name, p_date FROM client WHERE id = ?', (id,))
    user_data = cursor.fetchone()

    cursor.execute('SELECT game_name, number, unit, unit_price FROM client_games WHERE client_id = ?', (id,))
    client_games = cursor.fetchall()

    cursor.execute('SELECT pay FROM payment WHERE client_id = ?', (id,))
    payment=0
    pays=cursor.fetchall()
    for pay in pays:
        payment += pay[0]

    conn.close()
    total = 0
    games=[]
    for game in client_games:
        t=game[1]*game[2]*game[3]
        g={
            'name': game[0],
            'number': game[1],
            'unit': game[2],
            'unitp': game[3],
            'total': t,
        }
        games.append(g)
        total = total + t

    sold = total - payment

    return render_template('c_view_id.html', user_data=user_data, games=games , sold=sold, payment=payment, total=total, id=id)


@app.route('/client/view/<int:id>/makePDF')
def make_pdf(id):
    return render_template('pdf.html', id=id)


@app.route('/client/view/<int:id>/pdf', methods=['POST', 'GET'])
def generate_pdf(id):
    if request.method=='POST':
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT first_name, last_name, p_date FROM client WHERE id = ?', (id,))
        data = cursor.fetchone()
        user_data = {
            'first': data[0],
            'last': data[1],
            'date': data[2],
        }

        cursor.execute('SELECT game_name, number, unit, unit_price FROM client_games WHERE client_id = ?', (id,))
        games = cursor.fetchall()

        conn.close()
        gamesD = []
        total = 0
        for game in games:
            t = game[1]*game[2]*game[3]
            gameD = {
                'name': game[0],
                'number': game[1],
                'unit': game[2],
                'unitp': game[3],
                'total': t,
            }
            gamesD.append(gameD)
            total = total + (game[1] * game[2] * game[3])

        pdf_content = generate_pdf_content(user_data, gamesD, total, request.form.get('rcNumber'), request.form.get('nif'), request.form.get('nPlusArt'), request.form.get('adresse'))

        response = Response(pdf_content, content_type='application/pdf')
        response.headers['Content-Disposition'] = f'inline; filename=client_info_{id}.pdf'

        return response
    return render_template('pdf.html')



def generate_pdf_content(user_data, games, total, t1, t2, t3, t4):
    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", 'B', size=11)
    pdf.cell(0, 10, "EURL \"EUDOX EMBALLAGE TIZI\" ")
    pdf.ln(5)
    pdf.cell(0, 10, "RC N° 02 B 0662557", ln=True)

    pdf.cell(0, 10, "ART, IMPOS, 29030453801", ln=True)

    pdf.cell(0, 10, "N.I.F M,FISCAL 000229066255719", ln=True)

    pdf.set_font("Arial", 'B', size=18)

    pdf.cell(0, 10, "FACTURE", ln=True, align='C')

    pdf.set_font("Arial", 'B', size=9)

    pdf.cell(0, 10, f"Date: {user_data['date']}", ln=True, align='C')

    pdf.set_font("Arial", 'B', size=14)

    pdf.cell(0, 10, f"Client: {user_data['first']} {user_data['last']}", ln=True, align='C')

    pdf.set_font("Arial", 'B', size=12)

    pdf.cell(50, 10, "RC N°:", ln=False)
    pdf.cell(50, 10, t1, ln=False)
    pdf.ln(5)

    pdf.cell(50, 10, "NIF:", ln=False)
    pdf.cell(50, 10, t2, ln=False)
    pdf.ln(5)

    pdf.cell(50, 10, "N + ART:", ln=False)
    pdf.cell(50, 10, t3, ln=False)
    pdf.ln(5)

    pdf.cell(50, 10, "ADRESSE:", ln=False)
    pdf.cell(50, 10, t4, ln=False)
    pdf.ln(15)

    pdf.set_font("Arial", 'B', size=9)

    pdf.set_fill_color(200, 220, 255)
    pdf.cell(20, 8, "N°D ORDR", border=1, fill=True, align='C')
    pdf.cell(20, 8, "QUANT", border=1, fill=True, align='C')
    pdf.cell(50, 8, "Designation", border=1, fill=True, align='C')
    pdf.cell(20, 8, "unit", border=1, fill=True, align='C')
    pdf.cell(20, 8, "p/u", border=1, fill=True, align='C')
    pdf.cell(40, 8, "montant", border=1, fill=True, align='C')
    pdf.ln(8)

    i = 0 
    for game in games:
        i += 1
        pdf.cell(20, 8, str(i), border=1, align='C')
        pdf.cell(20, 8, str(game['number']), border=1)
        pdf.cell(50, 8, str(game['name']), border=1)
        pdf.cell(20, 8, f"{float(game['unit']):.2f}", border=1)
        pdf.cell(20, 8, f"{float(game['unitp']):.2f}", border=1)
        pdf.cell(40, 8, f"{float(game['total']):.2f}", border=1)
        pdf.ln(8)

    pdf.cell(110, 8, "")
    pdf.cell(20, 8, "", border=1)
    pdf.cell(40, 8, f"{float(total):.2f}", border=1)
    pdf.ln(8)
    t = total*19/100
    pdf.cell(90, 8, "")
    pdf.cell(20, 8, "TVA", align='C')
    pdf.cell(20, 8, "19", border=1)
    pdf.cell(40, 8, f"{float(t):.2f}", border=1)
    pdf.ln(8)
    pdf.cell(110, 8, "")
    pdf.cell(20, 8, "", border=1)
    pdf.cell(40, 8, f"{float(total + t):.2f}", border=1)
    pdf.ln(16)

    pdf.set_font("Arial", 'B', size=10)

    pdf.cell(0, 8, "ARRETE LA PRESENTE FACTURE A LA SOMME DE : UN MILLION CENT T E VINGTS TREIZE")
    pdf.ln(8)
    pdf.cell(0, 8, "HUIT CENT QUATRE VINGTS NEUF DINARS CINQUATE CENTIMES")

    pdf_output = pdf.output(dest='S').encode('latin1')

    return pdf_output

@app.route('/client/view/<int:id>/payment', methods=['POST', 'GET'])
def view_c_pay(id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT first_name, last_name, p_date FROM client WHERE id = ?', (id,))
    user_data = cursor.fetchone()

    cursor.execute('SELECT date, pay FROM payment WHERE client_id = ?', (id,))
    pay_s = cursor.fetchall()

    conn.close()
    total = 0
    for pay in pay_s:
        total += pay[1]

    return render_template('c_view_pay_id.html', user_data=user_data, pays=pay_s, t=total, id=id)



    ### detail ### 


@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/detail/add')
def add_detail():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    day = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("SELECT MAX(t_id) FROM d_mat")
    max_t_id = cursor.fetchone()[0]
    t_id = max_t_id + 1 if max_t_id is not None else 1

    cursor.execute("SELECT COUNT(*) FROM d_mat WHERE date = ?", (day,))
    d = cursor.fetchone()[0]

    if d == 0:
        for p_num in range(15):
            cursor.execute("""
                INSERT INTO d_mat (t_id, date, p_num, nember_d_m, poid_udm, poid_f, number_f_r, poid_feb, poid_be, poid_bu, stock, unit, p_unit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (t_id, day, p_num, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0))

        conn.commit()
        conn.close()
        return render_template('d_add.html', message="Added successfully!")

    conn.close()
    return render_template('d_add.html', message="Records for today already exist.")

@app.route('/detail/remove')
def delete_detail():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT t_id, date FROM d_mat GROUP BY t_id, date ORDER BY date DESC")
    result = cursor.fetchall()

    conn.close()

    return render_template('d_remove.html', dates=result)

@app.route('/detail/remove/<int:d>/delete')
def delete_t_detail(d):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM d_mat WHERE t_id = ?", (d,))
    conn.commit()

    conn.close()

    return redirect('/detail')

@app.route('/detail/view')
def view_detail():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT t_id, date FROM d_mat GROUP BY t_id, date ORDER BY date DESC")
    result = cursor.fetchall()

    conn.close()

    return render_template('d_view.html', dates=result)

@app.route('/detail/view/<int:d>')
def view_d_detail(d):
    return render_template('dt_view.html', date=d)

@app.route('/detail/view/<int:d>/<int:num>', methods=['POST', 'GET'])
def view_stock_d_detail(d,num):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        nember_d_m = request.form.get('ndm')
        poid_udm = request.form.get('pudm')
        poid_f = request.form.get('pf')
        number_f_r = request.form.get('nfr')
        poid_feb = request.form.get('pfb')
        poid_be = request.form.get('pbe')
        poid_bu = request.form.get('pbu')
        stock = request.form.get('stock')
        unit = request.form.get('unit')
        p_unit = request.form.get('p_unit')

        cursor.execute("""
            UPDATE d_mat
            SET nember_d_m=?, poid_udm=?, poid_f=?, number_f_r=?, poid_feb=?, poid_be=?, poid_bu=?, stock=?, unit=?, p_unit=?
            WHERE t_id=? AND p_num=?
        """, (nember_d_m, poid_udm, poid_f, number_f_r, poid_feb, poid_be, poid_bu, stock, unit, p_unit, d, num))

        conn.commit()

        return redirect("/detail/view/"+str(d))
    else:
        cursor.execute("SELECT nember_d_m, poid_udm, poid_f, number_f_r, poid_feb, poid_be, poid_bu, stock, unit, p_unit FROM d_mat WHERE t_id = ? AND p_num = ?", (d, num))

        data = cursor.fetchone()

    conn.close()

    return render_template('dt_s_view.html', date=d, data=data, num=num)


    ### stock ### 


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
            cursor.execute(f"SELECT {updated_game} FROM stv WHERE date = ?", (current_date,))
            old_v = cursor.fetchone()

            if old_v:
                new_v = old_v[0] + int(duplicate_numbers[i])
                cursor.execute(f"UPDATE stv SET {updated_game} = ? WHERE date = ?", (new_v, current_date))
                conn.commit()

        conn.close()
        return redirect('/stock')

    return render_template('s_add.html')

@app.route('/stock/remove', methods=['POST', 'GET'])
def remove_stock():
    if request.method == 'POST':
        current_date = datetime.now().strftime("%Y-%m-%d")

        duplicate_games = request.form.getlist('gameName[]')
        duplicate_numbers = request.form.getlist('number[]')

        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        for i in range(len(duplicate_games)):  
            updated_game = duplicate_games[i].replace(' ', '_') + '_e'
            cursor.execute(f"SELECT {updated_game} FROM stv WHERE date = ?", (current_date,))
            old_v = cursor.fetchone()

            if old_v:
                new_v = old_v[0] - int(duplicate_numbers[i])
                cursor.execute(f"UPDATE stv SET {updated_game} = ? WHERE date = ?", (new_v, current_date))
                conn.commit()

        conn.close()
        return redirect('/stock')

    return render_template('s_remove.html')

@app.route('/stock/view', methods=['POST', 'GET'])
def view_stock():
    if request.method == 'POST':
        today_date = request.form.get('search_date', datetime.now().strftime("%Y-%m-%d"), None)
        if not today_date:
            today_date = datetime.now().strftime("%Y-%m-%d")
    else:
        today_date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM stv WHERE date = ?', (today_date,))
    stock_data = cursor.fetchone()

    cursor.execute('SELECT u, up FROM upt WHERE date = ?', (today_date,))
    vals = cursor.fetchall()

    conn.close()

    product_names = ["MM Super", "MM FARDEAUX", "GMM", "GMM x25", "GMM x30", "MM IMP MANTOUDJ", "PM", "GM IMP", "GM IMP x20", "PAIN", "POUBELLE BASE", "POUBELLE", "CONGELATION", "GGM", "WELCOME"]

    total_stock = sum(stock_data[i * 3 + 2] for i in range(len(product_names)))
    total_entree = sum(stock_data[i * 3 + 3] for i in range(len(product_names)))
    total_sort = sum(stock_data[i * 3 + 4] for i in range(len(product_names)))
    total_rest = sum(stock_data[i * 3 + 2] + stock_data[i * 3 + 3] - stock_data[i * 3 + 4] for i in range(len(product_names)))
    total_v_stock = sum((stock_data[i * 3 + 2] + stock_data[i * 3 + 3] - stock_data[i * 3 + 4]) * vals[i][0] * vals[i][1] for i in range(len(product_names)))
    total_v_vendu = sum(stock_data[i * 3 + 4] * vals[i][0] * vals[i][1] for i in range(len(product_names)))

    return render_template('s_view.html', stock_data=stock_data, vals=vals, product_names=product_names, td=today_date,
                           total_stock=total_stock, total_entree=total_entree, total_sort=total_sort,
                           total_rest=total_rest, total_v_stock=total_v_stock, total_v_vendu=total_v_vendu)

@app.route('/update_value', methods=['POST'])
def update_value():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    data = request.get_json()
    index = data['index']
    sub_index = data['subIndex']
    value = data['value']
    td = data['td']

    if(sub_index):
        cursor.execute('UPDATE upt SET up = ? WHERE num = ? AND date = ?', (value, index, td))
    else:
        cursor.execute('UPDATE upt SET u = ? WHERE num = ? AND date = ?', (value, index, td))

    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/work')
def worker():
    return render_template('worker.html')

@app.route('/work/add', methods=['POST', 'GET'])
def add_worker():
    if request.method == 'POST':
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO worker(first_name, last_name) VALUES(?, ?)', (request.form.get('firstName'), request.form.get('lastName')))
        conn.commit()
        conn.close()
        return redirect('/work')
    return render_template('w_add.html')

@app.route('/work/edit')
def edit_worker():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM worker')
    data_f = cursor.fetchall()
    workers = []

    for data in data_f:
        worker = {
            'id': data[0],
            'first_name': data[1],
            'last_name': data[2]
        }
        workers.append(worker)

    conn.close()
    return render_template('w_edit.html', workers=workers)


@app.route('/work/edit/<int:id>', methods=['POST', 'GET'])
def edit_worker_id(id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        cursor.execute('UPDATE worker set first_name = ?, last_name = ? WHERE id = ?', (request.form.get('firstName'),request.form.get('lastName'), id))
        conn.commit()
        conn.close()
        return redirect('/work')

    cursor.execute('SELECT * FROM worker WHERE id = ?', (id, ))
    data_f = cursor.fetchone()

    conn.close()
    return render_template('w_modify.html', id=data_f[0], firstName=data_f[1], lastName=data_f[2])

@app.route('/work/remove')
def remove_worker():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM worker')
    data_f = cursor.fetchall()
    workers = []

    for data in data_f:
        worker = {
            'id': data[0],
            'first_name': data[1],
            'last_name': data[2]
        }
        workers.append(worker)

    conn.close()
    return render_template('w_remove.html', workers=workers)

@app.route('/work/remove/<int:id>')
def remove_worker_id(id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM w_time WHERE worker_id = ?', (id, ))
    cursor.execute('DELETE FROM worker WHERE id = ?',(id, ))
    conn.commit()
    conn.close()

    return redirect('/work')

def calc_time(start, finish, worker_id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT exit_time, entree_time FROM w_time WHERE worker_id = ? AND date BETWEEN ? AND ?', (worker_id, start, finish))

    results = cursor.fetchall()
    
    total_time = timedelta()
    
    for exit_time_str, entry_time_str in results:
        entry_time = datetime.strptime(entry_time_str, '%H:%M')
        exit_time = datetime.strptime(exit_time_str, '%H:%M')

        if entry_time > exit_time:

            exit_time += timedelta(days=1)
        
        total_time += exit_time - entry_time

    conn.close()

    return total_time

@app.route('/work/view')
def view_worker():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM worker')
    data_f = cursor.fetchall()
    workers = []

    for data in data_f:
        worker = {
            'id': data[0],
            'first_name': data[1],
            'last_name': data[2]
        }
        workers.append(worker)

    conn.close()
    return render_template('w_view.html', workers=workers)

@app.route('/work/calc/<int:id>', methods=['POST', 'GET'])
def calc_worker(id):
    if request.method == 'POST':
        sum = calc_time(request.form.get('start'), request.form.get('last'), id)
        return render_template('w_calc_result.html', sum=sum)
    return render_template('w_calc.html', id=id)


@app.route('/time')
def w_time():
    return render_template('time.html')

@app.route('/time/<name>')
def w_time_cal(name):
    return render_template('time_cal.html', name=name)

@app.route('/time/<name>/add', methods=['POST', 'GET'])
def w_time_add(name):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    current_date = datetime.now().strftime("%Y-%m-%d")
    if request.method == 'POST':
        worker_id = request.form.get('workerSelector')
        t_type = name
        date = current_date
        entree_time = request.form.get('entryTime')
        exit_time = request.form.get('departureTime')
        emargement = request.form.get('emargement')
        observation = request.form.get('observation')

        query = '''
            INSERT INTO w_time 
            (worker_id, t_type, date, entree_time, exit_time, emargement, observation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        cursor.execute(query, (worker_id, t_type, date, entree_time, exit_time, emargement, observation))

        conn.commit()
        conn.close()

        return redirect('/time/' + name)

    cursor.execute('SELECT * FROM worker')
    data_f = cursor.fetchall()
    workers = []

    for data in data_f:
        worker = {
            'id': data[0],
            'name': data[1] + " " + data[2]
        }
        workers.append(worker)

    conn.close()
    return render_template('tn_add.html', name=name, workers=workers)


@app.route('/time/<name>/remove')
def w_time_remove_list(name):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT date
        FROM w_time
        WHERE t_type = ?
        ORDER BY date DESC;
    ''', (name,))
    dates = cursor.fetchall()

    return render_template('tn_date_remove.html', dates=dates, name=name)

@app.route('/time/<name>/<date>/remove')
def w_time_remove(name, date):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT worker.first_name || ' ' || worker.last_name AS full_name,
               w_time.entree_time,
               w_time.exit_time,
               w_time.emargement,
               w_time.observation,
               w_time.id
        FROM w_time
        INNER JOIN worker ON w_time.worker_id = worker.id
        WHERE w_time.t_type = ? AND w_time.date = ?
    ''', (name, date))

    results = cursor.fetchall()
    conn.close()

    return render_template('tn_remove.html', results=results, name=name, date=date)

@app.route('/time/<name>/<date>/remove/<int:id>')
def remove_time_id(name, date, id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM w_time WHERE id = ?',(id,))
    conn.commit()
    conn.close()
    return redirect('/time/'+ name)

@app.route('/time/<name>/view')
def w_time_view_list(name):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT date
        FROM w_time
        WHERE t_type = ?
        ORDER BY date DESC;
    ''', (name,))
    dates = cursor.fetchall()

    return render_template('tn_date_view.html', dates=dates, name=name)

def time_PDF(n_type, date, workers):
    pdf = FPDF()
    pdf = FPDF(orientation='L')

    pdf.add_page()
    pdf.set_font("Arial", 'B', size=18)
    pdf.cell(150, 10, "ETAT DE POINTAGE " + n_type)
    pdf.cell(30, 10, "DU : " + date)
    pdf.set_font("Arial", 'B', size=10)

    pdf.ln(20)
    pdf.cell(85, 15, "NOMS ET PRENOMS", border=1)
    pdf.cell(45, 15, "HEURE D ENTREE", border=1, align='C')
    pdf.cell(45, 15, "HEURE D SORTIE", border=1, align='C')
    pdf.cell(45, 15, "EMARGEMENT", border=1, align='C')
    pdf.cell(45, 15, "OBSERVATION", border=1, align='C')
    pdf.ln(15)
    for worker in workers:
        pdf.cell(85, 10, worker[0], border=1)
        pdf.cell(45, 10, worker[1], border=1, align='C')
        pdf.cell(45, 10, worker[2], border=1, align='C')
        pdf.cell(45, 10, worker[3], border=1, align='C')
        pdf.cell(45, 10, worker[4], border=1, align='C')
        pdf.ln(10)

    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output
    

@app.route('/time/<name>/<date>/view', methods=['POST', 'GET'])
def w_time_view(name, date):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT worker.first_name || ' ' || worker.last_name AS full_name,
               w_time.entree_time,
               w_time.exit_time,
               w_time.emargement,
               w_time.observation
        FROM w_time
        INNER JOIN worker ON w_time.worker_id = worker.id
        WHERE w_time.t_type = ? AND w_time.date = ?
    ''', (name, date))

    results = cursor.fetchall()
    conn.close()
    if request.method == 'POST':
        pdf = time_PDF(name, date, results)
        response = Response(pdf, content_type='application/pdf')
        response.headers['Content-Disposition'] = f'inline; filename=workers_time_{name}.pdf'
        return response

    return render_template('tn_view.html', results=results, name=name, date=date)


if __name__ == '__main__':
    app.run(debug=True)
    # window = webview.create_window('stock', app)
    # webview.start()
