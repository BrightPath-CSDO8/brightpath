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
    cursor = db.cursor()

    # Execute the query
    courses = cursor.execute(
        'SELECT * FROM courses'
    ).fetchall()
    db.close()
    return [dict(course) for course in courses]

# RETRIEVE INDIV COURSE BY COURSE_ID
@app.route('/api/v1/courses/<string:course_id>', methods=["GET"])
def get_one_course(course_id): 

    db = get_db_connection()
    cursor = db.cursor()
    course = cursor.execute(
        'SELECT * FROM courses WHERE course_id = ?', 
        (course_id,)
    ).fetchone()
    db.close()

    return jsonify(dict(course)), 200



if __name__ == "__main__":
    # Below allows Flask to be automatically reloaded when changes made and saved
    app.run(debug=True)
    # Command below to run Flask application
    # Command: flask --app app.run --debug