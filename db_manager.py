import os
import json
import threading
from datetime import datetime

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, 'db.json')
db_lock = threading.Lock()

def init_db():
    """Ensure the JSON database file exists with the initial keys."""
    if not os.path.exists(DB_PATH):
        initial_data = {
            "bookings": [],
            "orders": [],
            "messages": [],
            "reviews": []
        }
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=2)

def read_db():
    """Read contents of the JSON database."""
    init_db()
    with db_lock:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Auto-migration: ensure 'reviews' key exists in older database files
        if "reviews" not in data:
            data["reviews"] = []
            with open(DB_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
        return data

def write_db(data):
    """Write contents to the JSON database atomically."""
    # Write to a temp file first, then replace the original file
    temp_path = DB_PATH + '.tmp'
    with db_lock:
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        os.replace(temp_path, DB_PATH)

# --- BOOKINGS CRUD ---
def get_bookings():
    db = read_db()
    return db.get("bookings", [])

def add_booking(booking_data):
    db = read_db()
    bookings = db.get("bookings", [])
    
    new_id = max([b["id"] for b in bookings]) + 1 if bookings else 1
    new_booking = {
        "id": new_id,
        "name": booking_data.get("name", "Anonymous"),
        "email": booking_data.get("email", ""),
        "roomType": booking_data.get("roomType", "Deluxe Room"),
        "checkin": booking_data.get("checkin", ""),
        "checkout": booking_data.get("checkout", ""),
        "status": "Confirmed",
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }
    bookings.append(new_booking)
    db["bookings"] = bookings
    write_db(db)
    return new_booking

def delete_booking(booking_id):
    db = read_db()
    bookings = db.get("bookings", [])
    
    target_index = -1
    for i, b in enumerate(bookings):
        if b["id"] == int(booking_id):
            target_index = i
            break
            
    if target_index == -1:
        return False
        
    bookings.pop(target_index)
    db["bookings"] = bookings
    write_db(db)
    return True

# --- FOOD ORDERS CRUD ---
def get_orders():
    db = read_db()
    return db.get("orders", [])

def add_order(order_data):
    db = read_db()
    orders = db.get("orders", [])
    
    new_id = max([o["id"] for o in orders]) + 1 if orders else 1
    new_order = {
        "id": new_id,
        "item": order_data.get("item", ""),
        "price": float(order_data.get("price", 0.0)),
        "roomNumber": order_data.get("roomNumber", "Room 101"),
        "status": "Pending",
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }
    orders.append(new_order)
    db["orders"] = orders
    write_db(db)
    return new_order

def update_order_status(order_id, status):
    db = read_db()
    orders = db.get("orders", [])
    
    target_order = None
    for o in orders:
        if o["id"] == int(order_id):
            target_order = o
            break
            
    if not target_order:
        return None
        
    target_order["status"] = status
    db["orders"] = orders
    write_db(db)
    return target_order

# --- CONTACT MESSAGES CRUD ---
def get_messages():
    db = read_db()
    return db.get("messages", [])

def add_message(message_data):
    db = read_db()
    messages = db.get("messages", [])
    
    new_id = max([m["id"] for m in messages]) + 1 if messages else 1
    new_message = {
        "id": new_id,
        "name": message_data.get("name", "Anonymous"),
        "email": message_data.get("email", ""),
        "message": message_data.get("message", ""),
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }
    messages.append(new_message)
    db["messages"] = messages
    write_db(db)
    return new_message

# --- GUEST REVIEWS CRUD ---
def get_reviews():
    db = read_db()
    return db.get("reviews", [])

def add_review(review_data):
    db = read_db()
    reviews = db.get("reviews", [])
    
    new_id = max([r["id"] for r in reviews]) + 1 if reviews else 1
    new_review = {
        "id": new_id,
        "name": review_data.get("name", "Anonymous"),
        "roomType": review_data.get("roomType", "Deluxe Room"),
        "rating": int(review_data.get("rating", 5)),
        "review": review_data.get("review", ""),
        "createdAt": datetime.utcnow().isoformat() + "Z"
    }
    reviews.append(new_review)
    db["reviews"] = reviews
    write_db(db)
    return new_review

def delete_review(review_id):
    db = read_db()
    reviews = db.get("reviews", [])
    
    target_index = -1
    for i, r in enumerate(reviews):
        if r["id"] == int(review_id):
            target_index = i
            break
            
    if target_index == -1:
        return False
        
    reviews.pop(target_index)
    db["reviews"] = reviews
    write_db(db)
    return True

