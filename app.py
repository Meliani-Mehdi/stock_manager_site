from flask import Flask, render_template, request, redirect, jsonify, Response
from fpdf import FPDF
from datetime import datetime, timedelta
import webview
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('form_data.db')
cursor = conn.cursor()

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
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id INTEGER,
        p_date TEXT NOT NULL,
        stock INTEGER NOT NULL,
        today_stock INTEGER NOT NULL,
        FOREIGN KEY (game_id) REFERENCES game(id)
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
        unitPrice REAL NOT NULL,
        deleted INTEGER DEFAULT 0 
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
    CREATE TABLE IF NOT EXISTS payment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        date TEXT NOT NULL,
        pay REAL NOT NULL,
        FOREIGN KEY (client_id) REFERENCES client(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cost (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        type TEXT,
        price REAL,
        txt1 TEXT,
        txt2 TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS detail (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        game TEXT NOT NULL,
        number_d_m INTEGER DEFAULT 0,
        poid_udm REAL DEFAULT 0,
        poid_f REAL DEFAULT 0,
        number_f_r REAL DEFAULT 0,
        poid_feb REAL DEFAULT 0,
        poid_be REAL DEFAULT 0,
        poid_bu REAL DEFAULT 0,
        stock INTEGER DEFAULT 0,
        unit REAL DEFAULT 0,
        p_unit REAL DEFAULT 0
    )
''')

conn.commit()
conn.close()

def insert_daily_data():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    current_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute('SELECT DISTINCT MAX(p_date) FROM stock')
    test = cursor.fetchone()[0]
    if test is None:
        cursor.execute('SELECT id FROM game WHERE deleted = 0')
        game_data = cursor.fetchall()
        for game in game_data:
            cursor.execute('INSERT INTO stock(game_id, p_date, stock, today_stock) VALUES(?, ?, 0, 0)', (game[0], current_date))
    elif test != current_date:
        cursor.execute('SELECT id, name FROM game WHERE deleted = 0')
        game_data = cursor.fetchall()
        for game in game_data:
            cursor.execute('SELECT SUM(client_games.number) AS num FROM client_games JOIN client ON client_games.client_id = client.id WHERE client.p_date = ? AND client_games.game_name = ?', (test, game[1]))
            rem = cursor.fetchone()[0]
            cursor.execute('SELECT stock, today_stock FROM stock WHERE p_date = ? AND game_id = ?', (test, game[0]))
            stk = cursor.fetchone()
            stock = 0 if stk[0] is None else stk[0]
            tstock = 0 if stk[1] is None else stk[1]
            remove = 0 if rem is None else rem
            total = stock + tstock - remove
            cursor.execute('INSERT INTO stock(game_id, p_date, stock, today_stock) VALUES(?, ?, ?, 0)', (game[0], current_date, total))

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
        current_date = datetime.now().strftime("%Y-%m-%d")

        cursor.execute('INSERT INTO game(name, unit, unitPrice) VALUES(?, ?, ?)', (request.form.get('name'), request.form.get('unite'), request.form.get('punit')))
        game_id = cursor.lastrowid
        cursor.execute('INSERT INTO stock(game_id, p_date, stock, today_stock) VALUES(?, ?, 0, 0)', (game_id, current_date))

        conn.commit()
        conn.close()
        return redirect('/game')
    return render_template('g_add.html')

@app.route('/game/edit')
def edit_game():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM game WHERE deleted = 0')
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

    cursor.execute('SELECT * FROM game WHERE deleted = 0')
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

    cursor.execute('UPDATE game set deleted = 1 WHERE id = ?', (id, ))
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

    cursor.execute('SELECT * FROM game WHERE deleted = 0')
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
            cursor.execute('SELECT name FROM game WHERE id = ? AND deleted = 0', (games[i], ))
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
    cursor.execute('SELECT * FROM game WHERE deleted = 0')

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
            cursor.execute('SELECT name FROM game WHERE id = ? AND deleted = 0', (games[i], ))
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
    cursor.execute('SELECT * FROM game WHERE deleted = 0')

    datas = cursor.fetchall()
    games = []

    for data in datas:
        game={
            'id': data[0],
            'game': data[1],
            'unit':f"{data[2]:.2f}",
            'unitp':f"{data[3]:.2f}",
        }
        games.append(game)
    
    cursor.execute('SELECT game_name, number, unit, unit_price FROM client_games WHERE client_id = ?', (id, ))
    datas = cursor.fetchall()
    lastgames = []

    for data in datas:
        game={
            'name':data[0],
            'number':data[1],
            'unit':f"{data[2]:.2f}",
            'unitp':f"{data[3]:.2f}",
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

    cursor.execute("SELECT date FROM detail WHERE date = ?", (day,))
    d = cursor.fetchone()

    if d is None:
        cursor.execute('SELECT name FROM game WHERE deleted = 0')
        games = cursor.fetchall()

        for game in games:
            cursor.execute('INSERT INTO detail(date, game) VALUES(?, ?)', (day, game[0]))
        conn.commit()
        conn.close()
        return render_template('d_add.html', message="Added successfully!")

    conn.close()
    return render_template('d_add.html', message="Records for today already exist.")

@app.route('/detail/remove', methods=['POST', 'GET'])
def delete_detail():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        day = request.form.get('search_date')
        if day != '':
            cursor.execute("SELECT DISTINCT date FROM detail WHERE date = ? ORDER BY date DESC", (day, ))
            result = cursor.fetchall()
            conn.close()
            return render_template('d_remove.html', dates=result)

    cursor.execute("SELECT DISTINCT date FROM detail ORDER BY date DESC")
    result = cursor.fetchall()

    conn.close()

    return render_template('d_remove.html', dates=result)

@app.route('/detail/remove/<date>/delete')
def delete_t_detail(date):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM detail WHERE date = ?", (date,))
    conn.commit()

    conn.close()

    return redirect('/detail')

@app.route('/detail/view', methods=['POST', 'GET'])
def view_detail():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        day = request.form.get('search_date')
        if day != '':
            cursor.execute("SELECT DISTINCT date FROM detail WHERE date = ? ORDER BY date DESC", (day, ))
            result = cursor.fetchall()
            conn.close()
            return render_template('d_view.html', dates=result)

    cursor.execute("SELECT DISTINCT date FROM detail ORDER BY date DESC")
    result = cursor.fetchall()

    conn.close()

    return render_template('d_view.html', dates=result)

@app.route('/detail/view/<date>')
def view_d_detail(date):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT game FROM detail WHERE date = ?', (date, ))
    games = cursor.fetchall()

    return render_template('dt_view.html', date=date, games=games)

@app.route('/detail/view/<date>/<name>', methods=['POST', 'GET'])
def view_stock_d_detail(date,name):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        number_d_m = request.form.get('ndm')
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
            UPDATE detail
            SET number_d_m=?, poid_udm=?, poid_f=?, number_f_r=?, poid_feb=?, poid_be=?, poid_bu=?, stock=?, unit=?, p_unit=?
            WHERE date = ? AND game = ?
        """, (number_d_m, poid_udm, poid_f, number_f_r, poid_feb, poid_be, poid_bu, stock, unit, p_unit, date, name))

        conn.commit()

        return redirect(f"/detail/view/{date}")
    else:
        cursor.execute("SELECT number_d_m, poid_udm, poid_f, number_f_r, poid_feb, poid_be, poid_bu, stock, unit, p_unit FROM detail WHERE date = ? AND game = ?", (date, name))

        data = cursor.fetchone()

    conn.close()

    return render_template('dt_s_view.html', date=date, data=data, name=name)


    ### stock ### 


@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/stock/add', methods=['POST', 'GET'])
def add_stock():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    current_date = datetime.now().strftime("%Y-%m-%d")

    if request.method == 'POST':
        names = request.form.getlist('gameName[]')
        numbers = request.form.getlist('number[]')
        for name, number in zip(names, numbers):
            cursor.execute('UPDATE stock SET today_stock = today_stock + ? WHERE game_id = ? AND p_date = ?', (number, name, current_date))
        conn.commit()
        conn.close()
        return redirect('/stock')

    cursor.execute('SELECT id, name FROM game WHERE deleted = 0')
    games = cursor.fetchall()
    conn.close()
    return render_template('s_add.html', games=games)

@app.route('/stock/remove', methods=['GET', 'POST'])
def remove_stock():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    current_date = datetime.now().strftime("%Y-%m-%d")

    if request.method == 'POST':
        names = request.form.getlist('gameName[]')
        numbers = request.form.getlist('number[]')
        for i in range(len(names)):
            cursor.execute('UPDATE stock SET today_stock = today_stock - ? WHERE game_id = ? AND p_date = ?', (numbers[i], names[i], current_date))
        conn.commit()
        conn.close()
        return redirect('/stock')

    cursor.execute('SELECT id, name FROM game WHERE deleted = 0')
    games = cursor.fetchall()
    conn.close()
    
    return render_template('s_remove.html', games=games)

@app.route('/stock/view', methods=['POST', 'GET'])
def view_stock():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    if request.method == 'POST' and request.form.get('search_date'):
        cursor.execute('SELECT DISTINCT p_date FROM stock WHERE p_date = ? ORDER BY p_date DESC;', (request.form.get('search_date'), ))
    else:
        cursor.execute('SELECT DISTINCT p_date FROM stock ORDER BY p_date DESC;')


    dates = cursor.fetchall()

    conn.close()

    return render_template('s_view.html',dates = dates)

@app.route('/stock/view/<date>')
def view_stock_date(date):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT game.name, stock.stock, stock.today_stock, game.unit, game.unitPrice FROM stock JOIN game ON stock.game_id = game.id WHERE stock.p_date = ?', (date, ))
    datas = cursor.fetchall()
    stocks = []

    for data in datas:

        cursor.execute(
            """
                SELECT
                    SUM(unit * unit_price * number) AS total_cost,
                    SUM(number) AS total_units
                FROM
                    client
                    JOIN client_games ON client.id = client_games.client_id
                WHERE
                    p_date = ? AND
                    game_name = ?
            ;""", (date, data[0])
        )
        tp = cursor.fetchone()
        tot =  0 if tp[1] is None else tp[1]
        price =  0 if tp[0] is None else tp[0]

        stock = {
            'name': data[0],
            'stock': data[1],
            'today_stock': data[2],
            't': data[1] + data[2],
            'exit': tot,
            'total': data[1] + data[2] - tot,
            'unit': data[3],
            'unitp': data[4],
            'price': price,
        }
        stocks.append(stock)

    conn.close()

    return render_template('s_view_date.html', stocks=stocks, Date=date)


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

        ### time ###

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
    pdf.cell(70, 15, "NOMS ET PRENOMS", border=1)
    pdf.cell(36, 15, "HEURE D ENTREE", border=1, align='C')
    pdf.cell(36, 15, "HEURE D SORTIE", border=1, align='C')
    pdf.cell(64, 15, "EMARGEMENT", border=1, align='C')
    pdf.cell(64, 15, "OBSERVATION", border=1, align='C')
    pdf.ln(15)
    for worker in workers:
        pdf.cell(70, 10, worker[0], border=1)
        pdf.cell(36, 10, worker[1], border=1, align='C')
        pdf.cell(36, 10, worker[2], border=1, align='C')
        pdf.cell(64, 10, worker[3], border=1, align='C')
        pdf.cell(64, 10, worker[4], border=1, align='C')
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

        ### frai ###

@app.route('/cost')
def cost():
    return render_template('frai.html')

@app.route('/cost/<name>')
def type_cost(name):
    return render_template('f_type.html', name=name)


@app.route('/cost/<name>/add', methods=['POST', 'GET'])
def add_cost(name):
    if request.method == 'POST':
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()
        date = request.form.get('date', datetime.now().strftime("%Y-%m-%d"))
        cursor.execute('INSERT INTO cost(date, type, price, txt1, txt2) VALUES(?, ?, ?, ?, ?)')

    return render_template('f_add.html')

# @app.route('/cost')
# def cost():
#     return render_template('frai.html')

@app.route('/cost/<name>/view')
def view_cost():
    return render_template('f_view.html')


if __name__ == '__main__':
    app.run(debug=True)
    # window = webview.create_window('stock', app)
    # webview.start()
