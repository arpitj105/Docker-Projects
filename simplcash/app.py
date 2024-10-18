import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'simplcash')

# Initialize MySQL
mysql = MySQL(app)

# Set secret key for session
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')

def init_db():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
    mysql.connection.commit()
    cur.close()

@app.before_first_request
def create_tables():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        
        # Hash the password
        hashed_password = generate_password_hash(password)
        
        # Insert user into database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, name) VALUES (%s, %s, %s)", (username, hashed_password, name))
        mysql.connection.commit()
        cur.close()
        
        # Log the user in
        session['user_id'] = username
        return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Wrong Credentials', 'error')
            return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT amount, description, created_at FROM expenses WHERE username = %s ORDER BY created_at DESC", [session['user_id']])
        expenses = cur.fetchall()
        cur.close()
        return render_template('dashboard.html', expenses=expenses)
    return redirect(url_for('index'))

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user_id' in session:
        amount = request.form['amount']
        description = request.form.get('description', '')
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO expenses (username, amount, description) VALUES (%s, %s, %s)", 
                    (session['user_id'], amount, description))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

@app.route('/view_expenses')
def view_expenses():
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT amount, description, created_at FROM expenses WHERE username = %s ORDER BY created_at DESC", [session['user_id']])
        expenses = cur.fetchall()
        cur.close()
        return render_template('dashboard.html', expenses=expenses)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
