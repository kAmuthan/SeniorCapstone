from flask import Flask, render_template, request, url_for, redirect

import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        userfirst = request.form['userfirst']
        userlast = request.form['userlast']
        phone = int(request.form['phone'])
        email = request.form['email']
        passconfirm = request.form['passconfirm']


        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (userfirst, userlast, phone, email, password)'
                    'VALUES (%s, %s, %s, %s, %s)',
                    (userfirst, userlast, phone, email, passconfirm))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login/')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')    
    