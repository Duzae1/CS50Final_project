from flask import Flask, flash, redirect, render_template, request, session, url_for
import random
from cs50 import SQL

app = Flask(__name__)
app.secret_key="dev"
db = SQL('sqlite:///app.db')

combos=[1, 2, 3, 4]

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('name') == '':
            flash('Please input your name')
            return redirect(url_for('index'))
        elif not int(request.form.get('combo')) in combos:
            flash('Combo not available')
            return redirect(url_for('index'))
        
        name = request.form.get('name')
        email = request.form.get('email')
        combo = int(request.form.get('combo'))

        address = request.form.get('address')
        table = request.form.get('table')

        if request.form.get('delivery') == True:
            db.execute('INSERT INTO orders (name, email, combo, address) VALUES (?, ?, ?, ?)', name, email, combo, address)
        else:
            db.execute('INSERT INTO orders (name, email, combo, table_n) VALUES (?, ?, ?, ?)', name, email, combo, address)

        flash('Successful order!')
        return redirect(url_for('index'))    
    
    else:
        return render_template('index.html', combos=combos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = 'admin'
    password = str(random.randrange(100000000))
    print(f"Pass: {password}")

    if request.method == 'POST':
        input_u = request.form.get("username")
        input_p = request.form.get("password")

        if input_u != username or input_p != password:
            flash('Unable to login')
            return render_template('login.html')

        return redirect(url_for('control'))
    else:
        return render_template ('login.html')


@app.route('/control', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        orders = db.execute('SELECT * FROM orders')
        return render_template ('control.html', orders=orders)
    else:
        flash('Login needed')
        return redirect(url_for('login'))