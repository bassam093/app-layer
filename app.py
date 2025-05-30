import mysql.connector
from flask import Flask, jsonify, request, redirect, url_for, render_template

app = Flask(__name__)

# Database configuration (update with your actual credentials)
db_config = {
    "host": "mysql",
    "user": "mysqluser",
    "password": "mysqlpassword",
    "database": "example_db"  # Update if your database name is different
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Hardcoded user ID for temporary use
    user_id = 1
    
    try:
        # Get bookings
        cursor.execute("""
            SELECT b.*, r.name as room_name, r.price_per_night 
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            WHERE b.user_id = %s
            ORDER BY b.check_in DESC
        """, (user_id,))
        bookings = cursor.fetchall()
        
        # Get available rooms
        cursor.execute("SELECT * FROM rooms WHERE available = 1")
        rooms = cursor.fetchall()
        
        return render_template('dashboard.html', bookings=bookings, rooms=rooms)
        
    except mysql.connector.Error as err:
        return render_template('error.html', error=str(err))
        
    finally:
        cursor.close()
        conn.close()

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT id FROM users WHERE username = %s", (data.get('username'),))
            if cursor.fetchone():
                return render_template('auth/register.html', error="Username exists")
            
            cursor.execute(
                "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)",
                (data.get('name'), data.get('email'), data.get('username'), data.get('password'))
            )
            conn.commit()
            return redirect(url_for('login'))

        except mysql.connector.Error as err:
            conn.rollback()
            return render_template('auth/register.html', error=str(err))

        finally:
            cursor.close()
            conn.close()
    
    return render_template('auth/register.html')

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and user['password'] == password:
            return redirect(url_for('dashboard'))
            
    return render_template('auth/login.html')

@app.route('/bookings/create', methods=['POST'])
def create_booking():
    user_id = 1  # Hardcoded temporary user ID
    room_id = request.form['room_id']
    check_in = request.form['check_in']
    check_out = request.form['check_out']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO bookings (user_id, room_id, check_in, check_out, status)
            VALUES (%s, %s, %s, %s, 'pending')
        """, (user_id, room_id, check_in, check_out))
        
        cursor.execute("UPDATE rooms SET available = 0 WHERE id = %s", (room_id,))
        conn.commit()
        return redirect(url_for('dashboard'))
        
    except mysql.connector.Error as err:
        conn.rollback()
        return render_template('error.html', error=str(err))
        
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
