from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "savetoday_secret_key"


# -----------------------------
# Create Database Tables
# -----------------------------
def create_tables():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        email TEXT,
        password TEXT
    )
    """)

    # Water Usage Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS water_usage(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        amount INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Electricity Usage Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS electricity_usage(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        units INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Food Waste Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_usage(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        waste TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Home
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(fullname,email,password) VALUES(?,?,?)",
            (fullname, email, password)
        )

        conn.commit()
        conn.close()

        return "Registration Successful! 🎉"

    return render_template("register.html")


# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT fullname FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["username"] = user[0]
            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return "Please login first"

    username = session["username"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM water_usage WHERE username=?",
        (username,)
    )
    water_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM electricity_usage WHERE username=?",
        (username,)
    )
    electricity_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM food_usage WHERE username=?",
        (username,)
    )
    food_count = cursor.fetchone()[0]

    # Calculate Sustainability Score
    total_entries = water_count + electricity_count + food_count

    score = total_entries * 10

    if score > 100:
        score = 100

    conn.close()

    return render_template(
        "dashboard.html",
        username=username,
        water_count=water_count,
        electricity_count=electricity_count,
        food_count=food_count,
        score=score
    )

# -----------------------------
# Water Tracker
# -----------------------------
@app.route("/water", methods=["GET", "POST"])
def water():

    if "username" not in session:
        return "Please login first"

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    if request.method == "POST":

        amount = request.form["amount"]

        cursor.execute(
            "INSERT INTO water_usage(username,amount) VALUES(?,?)",
            (session["username"], amount)
        )

        conn.commit()

    cursor.execute(
        "SELECT amount,date FROM water_usage WHERE username=? ORDER BY date DESC",
        (session["username"],)
    )

    records = cursor.fetchall()

    conn.close()

    return render_template(
        "water.html",
        records=records
    )


# -----------------------------
# Electricity Tracker
# -----------------------------
@app.route("/electricity", methods=["GET", "POST"])
def electricity():

    if "username" not in session:
        return "Please login first"

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    if request.method == "POST":

        units = request.form["units"]

        cursor.execute(
            "INSERT INTO electricity_usage(username,units) VALUES(?,?)",
            (session["username"], units)
        )

        conn.commit()

    cursor.execute(
        "SELECT units,date FROM electricity_usage WHERE username=? ORDER BY date DESC",
        (session["username"],)
    )

    records = cursor.fetchall()

    conn.close()

    return render_template(
        "electricity.html",
        records=records
    )


# -----------------------------
# Food Waste Tracker
# -----------------------------
@app.route("/food", methods=["GET", "POST"])
def food():

    if "username" not in session:
        return "Please login first"

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    if request.method == "POST":

        waste = request.form["waste"]

        cursor.execute(
            "INSERT INTO food_usage(username,waste) VALUES(?,?)",
            (session["username"], waste)
        )

        conn.commit()

    cursor.execute(
        "SELECT waste,date FROM food_usage WHERE username=? ORDER BY date DESC",
        (session["username"],)
    )

    records = cursor.fetchall()

    conn.close()

    return render_template(
        "food.html",
        records=records
    )
# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")
@app.route("/features")
def features():
    return render_template("features.html")
@app.route("/sdg12")
def sdg12():
    return render_template("sdg12.html")
# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    create_tables()
    app.run(debug=True)