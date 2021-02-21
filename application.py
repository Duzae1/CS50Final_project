from flask import Flask, flash, redirect, render_template, request, session, url_for
import random
from cs50 import SQL

app = Flask(__name__)
app.secret_key="dev"
db = SQL('sqlite:///app.db')

@app.route('/')
def index():
    return render_template('index.html')


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
        
        return render_template ('control.html')
    else:
        flash('Login needed')
        return redirect(url_for('login'))