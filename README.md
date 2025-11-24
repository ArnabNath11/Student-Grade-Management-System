# Student-Grade-Management-System

A modern, dark-themed Flask-based Student Grade Management System with authentication, student records, search & filtering, JSON storage, and interactive charts.
📌 Features
🔐 Authentication
Secure Login
New User Registration
Password hashing (Werkzeug)
Logout
Admin & User support
🧑‍🎓 Student Management
Add new student
Update student information
Delete student records
Automatic Grade Calculation
Stores Student ID, Name, Marks, Semester, College
🔎 Search / Filter
Search by Name or Student ID
Filter by Semester
Filter by College
📊 Charts
Top Marks bar chart (Chart.js)
🎨 UI & UX
Beautiful CS-Themed Dark UI
Responsive layout
Clean, modern design
📁 Project Structure
student_grade_web/
│── app.py
│── students.json
│── users.json
│── README.md
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│
└── static/
    ├── style.css
    └── app.js
📸 Screenshots
Dashboard
Login Page
Registration Page
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/student-grade-management-system.git
cd student-grade-management-system
2️⃣ Install dependencies
pip install flask werkzeug
3️⃣ Run the app
python app.py
4️⃣ Open in browser
http://127.0.0.1:5000/
🔑 Default Login Credentials
Username: admin
Password: admin123
(You can also register a new user.)
🧮 Grade Calculation Logic
Marks	Grade
90–100	A
75–89	B
60–74	C
40–59	D
Below 40	F
🗃 Sample JSON Structure
students.json
[
    {
        "id": 1,
        "student_id": "CS2025-01",
        "name": "John Doe",
        "marks": 92,
        "grade": "A",
        "semester": "4",
        "college": "ABC College"
    }
]
users.json
[
    {
        "username": "admin",
        "password": "<hashed_password>",
        "role": "admin"
    }
]
🚀 Future Enhancements
Migrate from JSON → SQLite / PostgreSQL
Add subject-wise marks
Export as PDF / Excel
Add Admin Dashboard
Add profile photo upload
📄 License
This project is free for academic and educational use.

This project is available for educational and academic use.
