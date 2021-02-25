import random

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_mail import Mail, Message
from cs50 import SQL

# setup flask app and database
app = Flask(__name__)
app.secret_key="dev"
db = SQL('sqlite:///app.db')

app.config["MAIL_DEFAULT_SENDER"] = 'selfservebot@gmail.com'
app.config["MAIL_PASSWORD"] = 'iooisrlvxbhhrarw'
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = 'selfservebot@gmail.com'
mail = Mail(app)

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
        combo = request.form.get('combo')
        table = 'Table: ' + request.form.get('table')
        address = 'Address: ' + request.form.get('address')
        radios = request.form.getlist('location')
        
        if 'pick_up' in radios:
            db.execute('INSERT INTO orders (name, email, location, combos) VALUES (?, ?, ?, ?)', name, email, 'Picks it up', combo)
        elif 'on_place' in radios:
            if request.form.get('table') == '':
                flash("Please input your table")
                return redirect(url_for('index'))
            db.execute('INSERT INTO orders (name, email, location, combos) VALUES (?, ?, ?, ?)', name, email, table, combo)
        elif 'delivery' in radios:
            if request.form.get('address') == '':
                flash("Please input your address")
                return redirect(url_for('index'))
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
    # assign user and password
    username = 'admin'
    password = '1234'

    if request.method == 'POST':
        # check for valid and correct input
        input_u = request.form.get("username")
        input_p = request.form.get("password")

        print(f'{input_u}, {input_p}')

        if input_u != username or input_p != password:
            flash('Unable to login')
            return render_template('login.html')

        return redirect(url_for('control'), code=308)
    else:
        # show login form
        return render_template ('login.html')


@app.route('/control', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        if request.form.get('save') == 'save':
            order_id = int(request.form.get('counter'))
            user_data = db.execute('SELECT name, email, location FROM orders WHERE id = ?', order_id)
            name = user_data[0]['name']
            email = user_data[0]['email']
            where = user_data[0]['location']
            if not email == None:
                if 'Address' in where: 
                    message = Message(f"Your order is on the way {name}!", recipients=[email])
                    mail.send(message)
                if 'Picks it up' in where:
                    message = Message(f"{name}, you can pick up your order!", recipients=[email])
                    mail.send(message)
            db.execute('UPDATE orders SET done = 1 WHERE id = ?', order_id)

        if request.form.get('delete') == 'delete':
            order_id = int(request.form.get('counter'))
            db.execute('DELETE FROM orders WHERE id = ?', order_id)

        orders = db.execute('SELECT * FROM orders WHERE done = 0')
        return render_template ('control.html', orders=orders)
          
    else:
            flash('Login needed')
            return redirect(url_for('login'))
       
            

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        orders = db.execute('SELECT * FROM orders')
        return render_template ('log.html', orders=orders)
    else:
        flash('Login needed')
        return redirect(url_for('login'))