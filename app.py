import os
import re
from flask import Flask, request, jsonify, send_from_directory
from database import db_manager

app = Flask(__name__, static_folder='public', static_url_path='')
ADMIN_PASSWORD = 'admin123'  # Default passcode for college project review

# Enable CORS manually for robustness
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Helper to verify admin authorization header
def is_admin_authorized(req):
    auth_header = req.headers.get('Authorization')
    return auth_header == ADMIN_PASSWORD

# Route for serving main website homepage
@app.route('/')
def index():
    return app.send_static_file('index.html')

# --- ADMIN LOGIN API ---
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json() or {}
    password = data.get('password')
    
    if password == ADMIN_PASSWORD:
        return jsonify({"success": True, "message": "Authentication successful"}), 200
    else:
        return jsonify({"success": False, "error": "Incorrect passcode. Try again!"}), 401

# --- BOOKINGS API ---

# Create reservation
@app.route('/api/bookings', methods=['POST', 'OPTIONS'])
def create_booking():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    room_type = data.get('roomType', '').strip()
    checkin = data.get('checkin', '').strip()
    checkout = data.get('checkout', '').strip()

    if not all([name, email, room_type, checkin, checkout]):
        return jsonify({"error": "All fields are required"}), 400

    email_pattern = r"^[^\s@]+@[^\s@]+\.com$"
    if not re.match(email_pattern, email):
        return jsonify({"error": "Invalid email address. Must end with .com"}), 400

    new_booking = db_manager.add_booking({
        "name": name,
        "email": email,
        "roomType": room_type,
        "checkin": checkin,
        "checkout": checkout
    })
    
    return jsonify({
        "success": True, 
        "message": "Booking created successfully!", 
        "booking": new_booking
    }), 201

# Get all bookings (Admin only)
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    if not is_admin_authorized(request):
        return jsonify({"error": "Unauthorized. Invalid admin password."}), 401
    
    bookings = db_manager.get_bookings()
    return jsonify(bookings), 200

# Cancel a booking (Admin only)
@app.route('/api/bookings/<int:booking_id>', methods=['DELETE', 'OPTIONS'])
def cancel_booking(booking_id):
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    if not is_admin_authorized(request):
        return jsonify({"error": "Unauthorized. Invalid admin password."}), 401

    success = db_manager.delete_booking(booking_id)
    if success:
        return jsonify({"success": True, "message": "Reservation cancelled successfully."}), 200
    else:
        return jsonify({"error": "Booking not found."}), 404

# --- FOOD ORDERS API ---

# Create order
@app.route('/api/orders', methods=['POST', 'OPTIONS'])
def create_order():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    data = request.get_json() or {}
    item = data.get('item', '').strip()
    price = data.get('price')
    room_number = data.get('roomNumber', '').strip() or 'Room 101'

    if not item or price is None:
        return jsonify({"error": "Item name and price are required"}), 400

    new_order = db_manager.add_order({
        "item": item,
        "price": price,
        "roomNumber": room_number
    })
    
    return jsonify({
        "success": True, 
        "message": "Order placed successfully!", 
        "order": new_order
    }), 201

# Get all orders (Admin only)
@app.route('/api/orders', methods=['GET'])
def get_orders():
    if not is_admin_authorized(request):
        return jsonify({"error": "Unauthorized. Invalid admin password."}), 401
    
    orders = db_manager.get_orders()
    return jsonify(orders), 200

# Update order status (Admin only)
@app.route('/api/orders/<int:order_id>/status', methods=['PUT', 'OPTIONS'])
def update_order_status(order_id):
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    if not is_admin_authorized(request):
        return jsonify({"error": "Unauthorized. Invalid admin password."}), 401

    data = request.get_json() or {}
    status = data.get('status')

    if not status or status not in ['Pending', 'Preparing', 'Served']:
        return jsonify({"error": "Invalid or missing status parameter."}), 400

    updated_order = db_manager.update_order_status(order_id, status)
    if updated_order:
        return jsonify({"success": True, "order": updated_order}), 200
    else:
        return jsonify({"error": "Order not found."}), 404

# --- CONTACT MESSAGES API ---

# Submit message
@app.route('/api/messages', methods=['POST', 'OPTIONS'])
def submit_message():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400

    email_pattern = r"^[^\s@]+@[^\s@]+\.com$"
    if not re.match(email_pattern, email):
        return jsonify({"error": "Invalid email address."}), 400

    new_message = db_manager.add_message({
        "name": name,
        "email": email,
        "message": message
    })
    
    return jsonify({
        "success": True, 
        "message": "Message sent successfully!", 
        "messageData": new_message
    }), 201

# Get all messages (Admin only)
@app.route('/api/messages', methods=['GET'])
def get_messages():
    if not is_admin_authorized(request):
        return jsonify({"error": "Unauthorized. Invalid admin password."}), 401
    
    messages = db_manager.get_messages()
    return jsonify(messages), 200

# --- REVIEWS & RATINGS API ---

# Submit new review
@app.route('/api/reviews', methods=['POST', 'OPTIONS'])
def create_review():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    data = request.get_json() or {}
    name = data.get('name', '').strip()
    room_type = data.get('roomType', '').strip()
    rating = data.get('rating')
    review_text = data.get('review', '').strip()

    if not name or not room_type or rating is None or not review_text:
        return jsonify({"error": "All fields are required"}), 400

    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 5:
            return jsonify({"error": "Rating must be between 1 and 5"}), 400
    except ValueError:
        return jsonify({"error": "Rating must be a valid integer"}), 400

    new_review = db_manager.add_review({
        "name": name,
        "roomType": room_type,
        "rating": rating_int,
        "review": review_text
    })

    return jsonify({
        "success": True,
        "message": "Review submitted successfully!",
        "review": new_review
    }), 201

# Get all reviews (Public)
@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    reviews = db_manager.get_reviews()
    return jsonify(reviews), 200

# Delete a review (Admin only)
@app.route('/api/reviews/<int:review_id>', methods=['DELETE', 'OPTIONS'])
def delete_review_endpoint(review_id):
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    if not is_admin_authorized(request):
        return jsonify({"error": "Unauthorized. Invalid admin password."}), 401

    success = db_manager.delete_review(review_id)
    if success:
        return jsonify({"success": True, "message": "Review deleted successfully."}), 200
    else:
        return jsonify({"error": "Review not found."}), 404

# Catch-all route to serve static frontend files (e.g. admin.html, styles, scripts)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('public', path)

if __name__ == '__main__':
    print("==================================================")
    print("  [Citylight Hotel Backend] listening on port 3000")
    print("  Frontend available: http://localhost:3000")
    print("  Admin passcode: admin123")
    print("==================================================")
    # Run server on port 3000
    app.run(host='0.0.0.0', port=3000, debug=True)
