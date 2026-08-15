import os

from flask import Flask, jsonify, request

# Creates a Flask application
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Test API routes

# Sends a GET request
@app.get('/api/greet')
def greet():
    return "Welcome first connection"


@app.get('/api/courses')
def get_courses():
    return jsonify({"message": "GET /api/courses works!"})

if __name__ == "__main__":
    app.run(debug=True)