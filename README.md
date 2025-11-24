# Student-Grade-Management-System

📚 Student Grade Management System (GradeSys)
A modern, dark-themed Flask-based Student Grade Management System with authentication, student records, filtering, JSON storage, and interactive charts.
🌟 Features
🔐 Authentication
Secure Login
New User Registration
Password hashing (Werkzeug)
Logout
Admin & User support
🧑‍🎓 Student Management
Add new student
Update student information
Delete student
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
Smooth modern design
🛠️ Tech Stack
Component	Technology
Backend	Python (Flask)
Frontend	HTML, CSS, JavaScript
Styling	Custom Dark Theme
Storage	JSON Files
Charts	Chart.js
Auth	Hashed passwords with Werkzeug
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
🖥️ Dashboard
🔐 Login Page
🆕 Registration Page
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/student-grade-web.git
cd student-grade-web
2️⃣ Install dependencies
pip install flask werkzeug
3️⃣ Run the application
python app.py
4️⃣ Open in browser
http://127.0.0.1:5000/
🔑 Default Login
Username: admin
Password: admin123
Or create a new user through the registration page.
🧮 Grade Calculation Logic
Marks	Grade
90–100	A
75–89	B
60–74	C
40–59	D
Below 40	F
📝 students.json Format
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
🚀 Future Enhancements
Database upgrade to SQLite / PostgreSQL
Profile image upload
Multi-subject mark entry
Export to PDF/CSV
Admin-only settings dashboard
📄 License
This project is available for educational and academic use.
