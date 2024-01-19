from os import close
from flask import Flask, render_template, request, redirect, jsonify
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
        last_name TEXT NOT NULL,
        payment INTEGER NOT NULL
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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS payment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        c_id INTEGER,
        date TEXT NOT NULL,
        pay INTEGER NOT NULL,
        FOREIGN KEY (c_id) REFERENCES stock_data(id)
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
        up INTEGER NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS d_mat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        p_num INTEGER NOT NULL,
        nember_d_m INTEGER,
        poid_udm REEL,
        poid_f RELL,
        number_f_r RELL,
        poid_feb RELL,
        poid_be RELL,
        poid_bu RELL
    )
''')

conn.commit()
conn.close()

def insert_daily_data():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d")
    print(current_date)

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

@app.route('/main')
def homepage():
    return render_template('main.html')

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
            INSERT INTO stock_data (p_date, first_name, last_name, payment)
            VALUES (?, ?, ?, 0)
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

            updated_game = duplicate_games[i].replace(' ', '_') + '_so'
            cursor.execute(f"SELECT {updated_game} FROM stv WHERE date = ?", (current_date,))
            old_v = cursor.fetchone()

            if old_v:
                new_v = old_v[0] + int(duplicate_numbers[i])
                cursor.execute(f"UPDATE stv SET {updated_game} = ? WHERE date = ?", (new_v, current_date))
                conn.commit()


        conn.close()
        return redirect('/client')

    return render_template('c_add.html')

@app.route('/client/view', methods=['POST', 'GET'])
def view_client():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        search_date = request.form.get('search_date', None)
        search_name = request.form.get('search_name', None)

        if search_date and search_name:
            cursor.execute('SELECT * FROM stock_data WHERE p_date = ? AND (first_name LIKE ? OR last_name LIKE ?) ORDER BY p_date DESC',(search_date, f'%{search_name}%', f'%{search_name}%'))
        elif search_date:
            cursor.execute('SELECT * FROM stock_data WHERE p_date = ? ORDER BY p_date DESC', (search_date,))
        elif search_name:
            cursor.execute('SELECT * FROM stock_data WHERE first_name LIKE ? OR last_name LIKE ? ORDER BY p_date DESC',
                           (f'%{search_name}%', f'%{search_name}%'))
        else:
            cursor.execute('SELECT * FROM stock_data ORDER BY p_date DESC')
    else:
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

        sold = total - user[4]

        user_with_games = {
            'id': user[0],
            'p_date': user[1],
            'first_name': user[2],
            'last_name': user[3],
            'pay': user[4],
            'sold': sold,
            'total': total
        }

        users_with_games.append(user_with_games)

    conn.close()

    return render_template('c_view.html', users=users_with_games)

@app.route('/client/view/<int:id>', methods=['POST', 'GET'])
def view_c_game(id):
    if request.method == 'POST':
        date = datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT payment FROM stock_data WHERE id = ?', (id,))
        pay = request.form.get('pay')
        new_val = int(pay) + cursor.fetchone()[0]
        cursor.execute('UPDATE stock_data SET payment = ? WHERE id = ?', (new_val,id))
        cursor.execute('''
            INSERT INTO payment (c_id, date, pay)
            VALUES (?, ?, ?)
        ''', (id, date, pay))
        conn.commit()

        conn.close()
        return redirect('/client/view')
        
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT first_name, last_name, p_date, payment FROM stock_data WHERE id = ?', (id,))
    user_data = cursor.fetchone()

    cursor.execute('SELECT * FROM stk_game WHERE stock_id = ?', (id,))
    games = cursor.fetchall()

    conn.close()
    total = 0
    for game in games:
        total = total + (game[3]*game[4]*game[5])

    sold = total - user_data[3]

    return render_template('c_view_id.html', user_data=user_data, games=games , sold=sold, t=total, id=id)

@app.route('/client/view/<int:id>/payment', methods=['POST', 'GET'])
def view_c_pay(id):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT first_name, last_name, p_date, payment FROM stock_data WHERE id = ?', (id,))
    user_data = cursor.fetchone()

    cursor.execute('SELECT * FROM payment WHERE c_id = ?', (id,))
    pay_s = cursor.fetchall()

    conn.close()
    total = 0
    for pay in pay_s:
        total += pay[3]

    return render_template('c_view_pay_id.html', user_data=user_data, pays=pay_s, t=total, id=id)



                                           ### detail ### 


@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/detail/add')
def add_detail():
    return render_template('detail.html')

@app.route('/detail/view')
def view_detail():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, date FROM d_mat")
    d = cursor.fetchall()

    conn.close()


    return render_template('d_view.html', dates=d)

@app.route('/detail/view/<int:d>')
def view_d_detail(d):
    return render_template('dt_view.html', date=d)

@app.route('/detail/view/<int:d>/<int:num>', methods=['POST', 'GET'])
def view_stock_d_detail(d,num):
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        pass
    else:
        cursor.execute("SELECT nember_d_m, poid_udm, poid_f, number_f_r, poid_feb, poid_be, poid_bu FROM d_mat WHERE id = ? AND p_num = ?", (d, num))

        data = cursor.fetchone()
    
    conn.close()
    
    return render_template('dt_s_view.html', date=d, data=data)


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

# webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    app.run(debug=True)
