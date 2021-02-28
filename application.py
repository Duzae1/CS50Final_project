import random

from flask import Flask, flash, redirect, render_template, request, url_for, session
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
menu = [1, 2, 3, 4]

# customers' page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check for valid input
        if request.form.get('name') == '':
            flash('Please input your name')
            return redirect(url_for('index'))
        if not request.form.get('combo'):
            flash('Please make an order')
            return redirect(url_for('index'))
        for each in request.form.getlist('combo'):
            if not int(each) in menu:
                flash('Combo not available')
        
        # retrieve form values
        name = request.form.get('name')
        email = request.form.get('email')
        order = request.form.getlist('combo')
        combos = ', '.join(order)
        table = 'Table: ' + request.form.get('table')
        address = 'Address: ' + request.form.get('address')
        radios = request.form.getlist('location')

        if not email == '' and not email == None:
            if not '@' in email or not '.com' in email:
                flash('Invalid email')
                return redirect(url_for('index'))

        # get total amount spent
        total = 0
        for item in order:
            if item == '1':
                total += 3
            elif item == '2':
                total += 5
            elif item == '3':
                total += 4
            elif item == '4':
                total += 2
        total = int(total)
        
        if 'pick_up' in radios:
            db.execute('INSERT INTO orders (name, email, location, combos, price) VALUES (?, ?, ?, ?, ?)', name, email, 'Picks it up', combos, total)
        elif 'on_place' in radios:
            if request.form.get('table') == '':
                flash("Please input your table")
                return redirect(url_for('index'))
            db.execute('INSERT INTO orders (name, email, location, combos, price) VALUES (?, ?, ?, ?, ?)', name, email, table, combos, total)
        elif 'delivery' in radios:
            if request.form.get('address') == '':
                flash("Please input your address")
                return redirect(url_for('index'))
            db.execute('INSERT INTO orders (name, email, location, combos, price) VALUES (?, ?, ?, ?, ?)', name, email, address, combos, total)
        else:
            flash('Invalid order')
            return redirect(url_for('index'))
       
        # Acknowledge order
        flash(f'Successful order! The total came up to ${total}')
        return redirect(url_for('index'))    
    
    else:
        # render the order form with the aforementioned combos
        return render_template('index.html', menu=menu)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # assign user and password
    username = 'admin'
    password = random.randrange(10000000)

    if request.method == 'POST':
        # check for valid and correct input
        input_u = request.form.get("username")
        input_p = request.form.get("password")

        if input_u != username or input_p != password:
            flash('Unable to login')
            return render_template('login.html')

        session['username'] = input_p
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
            if not email == '':
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
        return redirect(url_for('control'), code=303)

    else:
        if not session.get('username'):
            flash('Login needed')
            return redirect(url_for('login'))
        else:
            orders = db.execute('SELECT * FROM orders WHERE done = 0')
            return render_template ('control.html', orders=orders)
       
            

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        orders = db.execute('SELECT * FROM orders WHERE done = 1')
        return render_template ('log.html', orders=orders)
    else:
        flash('Login needed')
        return redirect(url_for('login'))