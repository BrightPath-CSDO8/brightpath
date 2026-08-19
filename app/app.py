import os
import sqlite3
from flask import Flask, jsonify, request

# Creates a Flask application
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# create SQLite connection
def get_db_connection():
    db = sqlite3.connect("instance/courses.db")
    db.row_factory = sqlite3.Row
    return db


# GET ALL COURSES
@app.route('/api/v1/courses', methods=["GET"])
def get_courses():
    db = get_db_connection()
    courses = db.execute(
        'SELECT * FROM courses'
    ).fetchall()
    print(f"courses:{courses}")
    db.close()
    return [dict(course) for course in courses]

if __name__ == "__main__":
    app.run(debug=True)