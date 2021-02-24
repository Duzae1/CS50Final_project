from flask import Flask, flash, redirect, render_template, request, session, url_for
import random
from cs50 import SQL

# setup flask app and database
app = Flask(__name__)
app.secret_key="dev"
db = SQL('sqlite:///app.db')

# list off the diferent combos
combos=[1, 2, 3, 4]

# customers' page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check for valid input
        if request.form.get('name') == '':
            flash('Please input your name')
            return redirect(url_for('index'))
        elif not int(request.form.get('combo')) in combos:
            flash('Combo not available')
            return redirect(url_for('index'))
        
        # retrieve form values
        name = request.form.get('name')
        email = request.form.get('email')
        combo = int(request.form.get('combo'))
        table = 'Table: ' + request.form.get('table')
        address = 'Address: ' + request.form.get('address')
        

        radios = request.form.getlist('location')
        if 'pick_up' in radios:
            db.execute('INSERT INTO orders (name, email, location, combos) VALUES (?, ?, ?, ?)', name, email, 'Picks it up', combo)
        elif 'on_place' in radios:
            db.execute('INSERT INTO orders (name, email, location, combos) VALUES (?, ?, ?, ?)', name, email, table, combo)
        elif 'delivery' in radios:
            db.execute('INSERT INTO orders (name, email, location, combos) VALUES (?, ?, ?, ?)', name, email, address, combo)
        else:
            flash('Invalid order')
            return redirect(url_for('index'))
       
        # Acknowledge order
        flash('Successful order!')
        return redirect(url_for('index'))    
    
    else:
        # render the order form with the aforementioned combos
        return render_template('index.html', combos=combos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # assign a username and create a different password each time someone tries to access the login form
    # print the password to the command line
    username = 'admin'
    password = '1234'

    if request.method == 'POST':
        # check for correct valid and correct input
        input_u = request.form.get("username")
        input_p = request.form.get("password")

        if input_u != username or input_p != password:
            flash('Unable to login')
            return render_template('login.html')

        return redirect(url_for('control'))
    else:
        # show login form
        return render_template ('login.html')


@app.route('/control', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        # return all orders
        orders = db.execute('SELECT * FROM orders')
        return render_template ('control.html', orders=orders)
    else:
        flash('Login needed')
        return redirect(url_for('login'))