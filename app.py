import json
import os
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
DATA_FILE = 'courses.json'

# --- Helper Functions for Data Persistence ---

def load_data():
    """Reads the JSON file and returns the list of courses."""
    if not os.path.exists(DATA_FILE):
        # Create an empty file if it doesn't exist
        save_data([])
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Handle file read errors
        return []

def save_data(data):
    """Writes the updated course list back to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        return False
    return True

# --- API Endpoints (CRUD Operations) ---

@app.route('/api/courses', methods=['GET'])
def get_courses():
    """Retrieve all courses from the learning path[cite: 1]."""
    courses = load_data()
    return jsonify(courses), 200

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Retrieve details for a single course by ID[cite: 1]."""
    courses = load_data()
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course), 200

@app.route('/api/courses', methods=['POST'])
def add_course():
    """Add a new course to the learning path[cite: 1]."""
    data = request.get_json()
    courses = load_data()

    # 1. Validate required fields[cite: 1]
    required_fields = ['name', 'description', 'target_date', 'status']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # 2. Validate status values[cite: 1]
    valid_statuses = ["Not Started", "In Progress", "Completed"]
    if data['status'] not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {valid_statuses}"}), 400

    # 3. Auto-generate ID and timestamp[cite: 1]
    new_id = max([c['id'] for c in courses], default=0) + 1
    new_course = {
        "id": new_id,
        "name": data['name'],
        "description": data['description'],
        "target_date": data['target_date'],
        "status": data['status'],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # 4. Append and Save[cite: 1]
    courses.append(new_course)
    if save_data(courses):
        return jsonify(new_course), 201
    return jsonify({"error": "File write error"}), 500

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """Modify status or details of an existing course[cite: 1]."""
    data = request.get_json()
    courses = load_data()
    course = next((c for c in courses if c['id'] == course_id), None)

    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Update fields if provided[cite: 1]
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
    """Remove a course from the platform[cite: 1]."""
    courses = load_data()
    # Create a new list excluding the course with the given ID[cite: 1]
    updated_courses = [c for c in courses if c['id'] != course_id]

    if len(updated_courses) == len(courses):
        return jsonify({"error": "Course not found"}), 404

    save_data(updated_courses)
    return jsonify({"message": f"Course {course_id} deleted successfully"}), 200

if __name__ == '__main__':
    # Initialize courses.json if it doesn't exist on startup[cite: 1]
    load_data()
    app.run(debug=True, port=5000)