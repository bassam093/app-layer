import mysql.connector
from flask import Flask, jsonify
import os
from dotenv import load_dotenv
load_dotenv()

def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

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

def create_users_table():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                print("Users table created successfully!")
    except Exception as e:
        print(f"Users table creation error: {e}")


def create_bookings_table():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bookings (
                        booking_id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT,
                        holiday_id INT,
                        booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status VARCHAR(20) DEFAULT 'active',
                        total_price DECIMAL(10,2),
                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                        FOREIGN KEY (holiday_id) REFERENCES holidays(holiday_id)
                    )
                """)
                conn.commit()
                print("Bookings table created successfully!")
    except Exception as e:
        print(f"Bookings table creation error: {e}")

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

def create_user(name, email, username, password_hash):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users 
                    (name, email, username, password_hash)
                    VALUES (%s, %s, %s, %s)
                """, (name, email, username, password_hash))
                conn.commit()
                print("New user created successfully!")
    except Exception as e:
        print(f"User creation error: {e}")


def create_booking(user_id, holiday_id, status='active', total_price=None):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO bookings 
                    (user_id, holiday_id, status, total_price)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, holiday_id, status, total_price))
                conn.commit()
                print("New booking created successfully!")
    except Exception as e:
        print(f"Booking creation error: {e}")


if __name__ == "__main__":
    create_holidays_table()
    create_users_table()
    create_bookings_table()
    app.run(debug=True, host="0.0.0.0", port=80)