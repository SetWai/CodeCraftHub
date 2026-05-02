import json
import os
from datetime import datetime
# Added 'send_from_directory' to serve the frontend files
from flask import Flask, request, jsonify, send_from_directory
# You may need to install this: pip install flask-cors
from flask_cors import CORS 

app = Flask(__name__)
# Enable CORS so your frontend can talk to the backend
CORS(app) 

DATA_FILE = 'courses.json'

# --- Helper Functions for Data Persistence ---

def load_data():
    """Reads the JSON file and returns the list of courses."""
    if not os.path.exists(DATA_FILE):
        save_data([])
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data):
    """Writes the updated course list back to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        return False
    return True

# --- Frontend Serving Route ---

@app.route('/')
def serve_frontend():
    """Serves the index.html file from the current directory."""
    # Ensure index.html is in the same folder as app.py
    return send_from_directory('.', 'index.html')

# --- API Endpoints (CRUD Operations) ---

@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Retrieve all courses from the learning path."""
    courses = load_data()
    return jsonify(courses), 200

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Retrieve details for a single course by ID."""
    courses = load_data()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course), 200

@app.route('/api/courses', methods=['POST'])
def add_course():
    """Add a new course to the learning path."""
    data = request.get_json()
    courses = load_data()

    required_fields = ['name', 'description', 'target_date', 'status']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    valid_statuses = ["Not Started", "In Progress", "Completed"]
    if data['status'] not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {valid_statuses}"}), 400

    new_id = max([c['id'] for c in courses], default=0) + 1
    new_course = {
        "id": new_id,
        "name": data['name'],
        "description": data['description'],
        "target_date": data['target_date'],
        "status": data['status'],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    courses.append(new_course)
    if save_data(courses):
        return jsonify(new_course), 201
    return jsonify({"error": "File write error"}), 500

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """Modify status or details of an existing course."""
    data = request.get_json()
    courses = load_data()
    course = next((c for c in courses if c['id'] == course_id), None)

    if not course:
        return jsonify({"error": "Course not found"}), 404

    valid_statuses = ["Not Started", "In Progress", "Completed"]
    if 'status' in data and data['status'] not in valid_statuses:
        return jsonify({"error": "Invalid status value"}), 400

    course['name'] = data.get('name', course['name'])
    course['description'] = data.get('description', course['description'])
    course['target_date'] = data.get('target_date', course['target_date'])
    course['status'] = data.get('status', course['status'])

    save_data(courses)
    return jsonify(course), 200

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Remove a course from the platform."""
    courses = load_data()
    updated_courses = [c for c in courses if c['id'] != course_id]

    if len(updated_courses) == len(courses):
        return jsonify({"error": "Course not found"}), 404

    save_data(updated_courses)
    return jsonify({"message": f"Course {course_id} deleted successfully"}), 200

if __name__ == '__main__':
    load_data()
    app.run(debug=True, port=5000)