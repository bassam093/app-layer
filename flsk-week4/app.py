from flask import Flask, jsonify, request
import secrets
import functools


app = Flask(__name__)


db = {"users": {}, "holidays": {}, "bookings": {}, "tokens": {}}


def auth_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token not in db["tokens"]:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper


@app.route('/')
def home():
    return "Welcome to the Travel Booking API!"


@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    if db["users"].get(data['username']) == data['password']:
        token = secrets.token_hex(16)
        db["tokens"][token] = data['username']
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/auth/logout', methods=['POST'])
@auth_required
def logout():
    token = request.headers.get('Authorization')
    db["tokens"].pop(token, None)
    return jsonify({"message": "Logged out"}), 200

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    if data['username'] not in db["users"]:
        db["users"][data['username']] = data['password']
        return jsonify({"message": "Registered"}), 201
    return jsonify({"error": "User exists"}), 400


@app.route('/users/<username>', methods=['PUT', 'DELETE'])
@auth_required
def manage_user(username):
    if request.method == 'PUT':
        db["users"][username] = request.json.get('password', db["users"][username])
    elif request.method == 'DELETE':
        db["users"].pop(username, None)
    return jsonify({"message": "Success"}), 200


@app.route('/holidays', methods=['GET'])
@auth_required
def get_holidays():
    return jsonify(list(db["holidays"].values()))

@app.route('/holidays/<holiday_id>', methods=['GET'])
@auth_required
def get_holiday(holiday_id):
    return jsonify(db["holidays"].get(holiday_id, {"error": "Not found"}))


@app.route('/bookings', methods=['POST'])
@auth_required
def create_booking():
    booking_id = secrets.token_hex(8)
    db["bookings"][booking_id] = request.json
    return jsonify({"id": booking_id}), 201

@app.route('/bookings/<booking_id>', methods=['GET', 'PUT', 'DELETE'])
@auth_required
def manage_booking(booking_id):
    if request.method == 'GET':
        return jsonify(db["bookings"].get(booking_id, {"error": "Not found"}))
    elif request.method == 'PUT':
        db["bookings"][booking_id].update(request.json)
    elif request.method == 'DELETE':
        db["bookings"].pop(booking_id, None)
    return jsonify({"message": "Success"}), 200


@app.route('/payments', methods=['POST'])
@auth_required
def process_payment():
    return jsonify({"message": "Payment processed"}), 200

if __name__ == '__main__':
    app.run(debug=True)
