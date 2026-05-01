CodeCraftHub: Your Personalized Learning Tracker
Welcome to CodeCraftHub, a simple yet powerful tool designed for developers to manage their learning journey. This project is built specifically for beginners who want to learn how REST APIs work using Python and Flask.


Instead of using a complex database, CodeCraftHub stores your data in a simple JSON text file, making it easy to see exactly how your data is being read and written by the server.



🚀 Features
* Full CRUD Operations: Create, Read, Update, and Delete courses.   
* No Database Required: All data is persisted in a local courses.json file.   
* Automatic Data Initialization: The app creates your storage file automatically on its first run.   
* Data Validation: Ensures all courses have the correct status and required information.   
* Timestamps: Automatically tracks when each course was added to your list.   

🛠 Installation
Follow these steps to set up the project on your local machine.
1. Prerequisites
Ensure you have Python 3.x installed. You can check this by running python --version in your terminal.
2. Setup Project Folder
Bash

mkdir CodeCraftHub
cd CodeCraftHub
3. Install Flask
Flask is the web framework we use to build the API. Install it using pip:
Bash

pip install flask
4. Create the files
Create a file named app.py and paste the Python code provided in the previous steps.



🏃 How to Run the Application
In your terminal or command prompt, run the following command:
Bash

python app.py
You should see an output similar to:
* Running on [http://127.0.0.1:5000](http://127.0.0.1:5000) (Press CTRL+C to quit)
Your API is now live and waiting for requests!

📂 Project Structure
* app.py: The "brain" of your application. It contains the Flask server, the API routes, and the logic to handle data.   
* courses.json: This file will appear automatically after you run the app or add your first course. It acts as your database.   

📡 API Documentation
All endpoints return data in JSON format.


Endpoints Summary
Method	Endpoint	Description
GET	/api/courses	Get all courses.
GET	/api/courses/<id>	Get a specific course by ID.
POST	/api/courses	Add a new course.
PUT	/api/courses/<id>	Update an existing course.
DELETE	/api/courses/<id>	Delete a course.
Example Request (Add a Course)
POST /api/courses
JSON

{
  "name": "Flask 101",
  "description": "Learning REST APIs",
  "target_date": "2026-06-01",
  "status": "Not Started"
}

🧪 Testing Instructions
Since this is a REST API without a frontend, you can test it using curl commands in your terminal or a tool like Postman.


Test: Get All Courses
Bash

curl -X GET http://127.0.0.1:5000/api/courses
Test: Create a New Course
Bash

curl -X POST http://127.0.0.1:5000/api/courses \
     -H "Content-Type: application/json" \
     -d '{"name":"Learning REST","description":"Finalizing the project","target_date":"2026-05-01","status":"In Progress"}'

🔍 Troubleshooting
* Address already in use: This means another app is using port 5000. You can change the port in app.py by editing app.run(port=5001).
* JSONDecodeError: If you manually edit courses.json and make a typo (like forgetting a comma), the app might fail to load. Check your JSON formatting.
* 404 Not Found: Ensure you are using the correct ID in the URL (e.g., /api/courses/1).   
* 400 Bad Request: Make sure you have included all required fields: name, description, target_date, and status.   

📝 License
This project is for educational purposes. Feel free to modify and expand it!
