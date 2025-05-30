import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)   

@app.route("/")
def home():
    return "Travel Booking System - Operational!"

@app.route("/holidays")
def list_holidays():
    try:
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM holidays")
                holidays = cursor.fetchall()
                return jsonify(holidays)
    except:
        return "Database error:", 500

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="mysql",
            user="root",
            password="Qwepoi123",
            database="travel_booking"
        )
    except:
        print("Database connection failed")
        return None

def create_holidays_table():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS holidays (
                        holiday_id INT AUTO_INCREMENT PRIMARY KEY,
                        destination VARCHAR(255) NOT NULL,
                        description TEXT,
                        price DECIMAL(10, 2) NOT NULL,
                        availability BOOLEAN DEFAULT TRUE,
                        duration_days INT NOT NULL,
                        start_date DATE NOT NULL,
                        end_date DATE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                print("Holidays table created successfully!")
    except:
        print("Table creation error")


def create_holiday(destination, price, duration_days, description=None):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO holidays 
                    (destination, description, price, duration_days)
                    VALUES (%s, %s, %s, %s)
                """, (destination, description, price, duration_days))
                conn.commit()
                print("New holiday package created!")
    except:
        print("Creation error")

if __name__ == "__main__":
    create_holidays_table()
    app.run(debug=True, host="0.0.0.0", port=80)