# 🏨 Citylight Hotel - Full Stack Reservation & Management System (Python Stack)

Welcome to the **Citylight Hotel** complete full-stack web application. This project features a modernized, premium user frontend and a robust Python/Flask backend integrated with an Admin Dashboard and local persistent data storage.

---

## 🚀 Technology Stack

- **Frontend**: HTML5, Vanilla CSS3 (Custom responsive layout & glassmorphic cards), Vanilla ES6 JavaScript
- **Backend**: Python 3.x, Flask (REST APIs, CORS configuration, static page hosting)
- **Database**: File-based Atomic JSON DB manager (Initializes inside `database/db.json` automatically, requires **zero database installation**)

---

## ✨ Features

1. **Elegant Landing Page**: Stunning glassmorphic header, parallax styling, room cards, and chef menu displays.
2. **Room Reservations**: Live check-in/check-out date validation (prevents picking past dates or checkout before checkin), room selector, and dynamic database booking.
3. **Room-Service Food Orders**: Place culinary requests from the menu which directly enter the chef's active queue.
4. **Guest Message Center Center**: Direct messaging system for queries and feedback submissions.
5. **Admin Management Console (`/admin.html`)**:
   - Protected by a security passcode (`admin123`).
   - **Real-time Analytics**: Total bookings counter, food order counter, active feedback counter, and **dynamically calculated revenue** (sum of nights stayed * room rates + ordered food prices).
   - **Reservation Manager**: View check-in details, emails, and cancel reservations.
   - **Kitchen Display Queue**: Update food statuses (`Pending` -> `Preparing` -> `Served`) in real-time.
   - **Inquiry Reader**: Read guest queries with timestamps.

---

## 💻 How to Run (Step-by-Step for Windows)

Since this project runs on Python, follow these simple steps to launch the server on your computer:

### Step 1: Install Python
If you don't have Python installed on your PC:
1. Go to the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the latest installer for Windows.
3. Run the installer. **CRITICAL STEP**: Make sure to check the box at the bottom that says **"Add python.exe to PATH"** before clicking Install.

### Step 2: Open Command Prompt / PowerShell
1. Click the Windows Start menu, type `cmd` or `PowerShell`, and open it.
2. Navigate to this project directory:
   ```powershell
   cd "C:\Users\Harshitha Singh\Desktop\PROJECT(AURA)"
   ```

### Step 3: Install Flask Dependencies
Install the required Flask server framework packages by running:
```powershell
pip install -r requirements.txt
```

### Step 4: Start the Server
Start the Python backend server using:
```powershell
python app.py
```

You will see a success message in your terminal:
```text
==================================================
  🏨 Citylight Hotel Backend listening on port 3000
  🌐 Frontend available: http://localhost:3000
  ⚙️  Admin passcode: admin123
==================================================
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:3000
```

### Step 5: Open in Your Browser
Once the server starts:
- Visit the main website: **[http://localhost:3000](http://localhost:3000)**
- Visit the Admin Console: **[http://localhost:3000/admin.html](http://localhost:3000/admin.html)** (Passcode: `admin123`)

---

## 📁 File Structure

```text
PROJECT(AURA)/
│
├── database/
│   ├── db.json          # Generated automatically. Stores bookings, food orders, and messages.
│   └── db_manager.py    # Python DB CRUD helper layer (atomic json reads/writes)
│
├── public/              # Frontend static directory
│   ├── css/
│   │   └── style.css    # Premium CSS design tokens & animations
│   ├── js/
│   │   ├── app.js       # Homepage script (API calls, date picker, alerts)
│   │   └── admin.js     # Admin panel logic (fetching lists, deletions, status updates)
│   ├── index.html       # Landing page HTML
│   └── admin.html       # Passcode protected management dashboard
│
├── requirements.txt     # Python server dependencies (Flask)
├── app.py               # Flask application server (APIs, static routing, auth validation)
└── README.md            # You are reading this!
```
