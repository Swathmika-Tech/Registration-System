from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "event.db"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        location TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        event_id INTEGER,
        FOREIGN KEY(event_id) REFERENCES events(id)
    )
    """)

    conn.commit()
    conn.close()


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO events (name, date, location) VALUES (?, ?, ?)",
        (data["name"], data["date"], data["location"])
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Event created successfully"})


@app.route("/events", methods=["GET"])
def view_events():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM events")
    events = cur.fetchall()
    conn.close()

    return jsonify(events)


@app.route("/register", methods=["POST"])
def register_event():
    data = request.get_json()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO registrations (user_name, event_id) VALUES (?, ?)",
        (data["user_name"], data["event_id"])
    )

    conn.commit()
    conn.close()
    return jsonify({"message": "Registration successful"})


@app.route("/registrations", methods=["GET"])
def view_registrations():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT registrations.id, user_name, events.name
    FROM registrations
    JOIN events ON registrations.event_id = events.id
    """)
    data = cur.fetchall()
    conn.close()

    return jsonify(data)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
