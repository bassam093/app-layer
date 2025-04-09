import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

db_config = {
    "host": "mysql",
    "user": "flaskuser",
    "password": "flaskpassword",
    "database": "flaskdb"
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/')
def home():
    return "Welcome to the Travel Booking API!"

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (data.get('username'),))
        if cursor.fetchone():
            return jsonify({"error": "Username already exists"}), 400

        cursor.execute(
            "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)",
            (data.get('name'), data.get('email'), data.get('username'), data.get('password'))
        )

        user_id = cursor.lastrowid
        connection.commit()

        return jsonify({"message": "Account successfully created", "user_id": user_id}), 201

    except mysql.connector.Error as err:
        connection.rollback()
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s",
        (data.get('name'), data.get('email'), user_id)
    )
    connection.commit()

    cursor.close()
    connection.close()
    
    return jsonify({"message": "User updated successfully"}), 200

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    current_password = request.args.get('currentPassword')
    if not current_password:
        return jsonify({"error": "Password is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id FROM users WHERE id = %s AND password = %s", 
                  (user_id, current_password))
    
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        return jsonify({"error": "Invalid password"}), 401

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "User deleted successfully"}), 200

@app.route('/holidays', methods=['GET'])
def get_holidays():
    destination = request.args.get('destination')
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if destination:
        cursor.execute("SELECT * FROM holidays WHERE destination LIKE %s", (f"%{destination}%",))
    else:
        cursor.execute("SELECT * FROM holidays")
    
    holidays = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return jsonify(holidays)

@app.route('/holidays', methods=['POST'])
def add_holidays():
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO holidays (destination, details) VALUES (%s, %s)",
        (data.get('destination'), data.get('details', ''))
    )

    holiday_id = cursor.lastrowid
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Holiday created", "id": holiday_id}), 201

@app.route('/holidays/<holiday_id>', methods=['GET'])
def get_holiday(holiday_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM holidays WHERE id = %s", (holiday_id,))
    
    holiday = cursor.fetchone()

    cursor.close()
    connection.close()

    if holiday:
        return jsonify(holiday)
    
    return jsonify({"error": "Holiday not found"}), 404

@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    connection = get_db_connection()
    
    cursor = connection.cursor()

    cursor.execute(
        """INSERT INTO bookings 
           (holiday_id, travel_dates, traveler_details) 
           VALUES (%s, %s, %s)""",
        (data.get('holidayId'), 
         data.get('travelDates'), str(data.get('travelerDetails')))
     )
    
    booking_id = cursor.lastrowid
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"id": booking_id}), 201

@app.route('/bookings/<booking_id>', methods=['GET'])
def get_booking(booking_id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM bookings WHERE id = %s AND user_id = %s", 
        (booking_id, request.user_id)
    )
    booking = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if booking:
        return jsonify(booking_id, {"error": "Not found"}), 404

@app.route('/bookings/<booking_id>', methods=['PUT'])
def update_booking(booking_id):
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM bookings WHERE id = %s AND user_id = %s", 
        (booking_id, request.user_id)
    )
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        return jsonify({"error": "Booking not found"}), 404

    cursor.execute(
        """UPDATE bookings 
           SET travel_dates = %s, traveler_details = %s 
           WHERE id = %s""",
        (data.get('travelDates'), str(data.get('travelerDetails')), booking_id)
    )
    connection.commit()
    
    cursor.close()
    connection.close()
    
    return jsonify({"message": "Booking updated"}), 200

@app.route('/bookings/<booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM bookings WHERE id = %s AND user_id = %s", 
        (booking_id, request.user_id)
    )
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        return jsonify({"error": "Booking not found"}), 404

    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
    connection.commit()
    
    cursor.close()
    connection.close()

    return jsonify({"Success"}), 200


@app.route('/payments', methods=['POST'])
def process_payment():
    data = request.json
    if not all(k in data for k in ['bookingId', 'paymentDetails']):
        return jsonify({"error": "Missing required fields"}), 400
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id FROM bookings WHERE id = %s AND user_id = %s", 
        (data.get('bookingId'), request.user_id)
    )
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        return jsonify({"error": "Booking not found"}), 404

    cursor.execute(
        """INSERT INTO payments 
           (booking_id, user_id, amount, payment_details, status) 
           VALUES (%s, %s, %s, %s, %s)""",
        (data.get('bookingId'), request.user_id, 
         data.get('paymentDetails', {}).get('amount', 0),
         str(data.get('paymentDetails')), 'completed')
    )
    
    payment_id = cursor.lastrowid
    connection.commit()
    
    cursor.close()
    connection.close()
    return jsonify({"Payment processed"}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)