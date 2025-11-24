from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json, os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_random_secret'  # replace for production

STUDENTS_FILE = 'students.json'
USERS_FILE = 'users.json'

# Helpers
def load_json(file):
    if not os.path.exists(file):
        return []
    with open(file, 'r') as f:
        return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Ensure files exist
if not os.path.exists(STUDENTS_FILE):
    save_json(STUDENTS_FILE, [])

if not os.path.exists(USERS_FILE):
    # default admin account: admin / admin123 (hashed)
    hashed = generate_password_hash('admin123')
    save_json(USERS_FILE, [{'username': 'admin', 'password': hashed, 'role': 'admin'}])

# AJAX-friendly auth decorator (single definition)
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            # Detect AJAX / fetch calls and prefer JSON 401
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            wants_json = 'application/json' in (request.headers.get('Accept') or '')
            if is_ajax or wants_json:
                return jsonify({'error': 'not_authenticated'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# Grade calculation
def calculate_grade(marks):
    marks = int(marks)
    if marks >= 90:
        return 'A'
    elif marks >= 75:
        return 'B'
    elif marks >= 60:
        return 'C'
    elif marks >= 40:
        return 'D'
    else:
        return 'F'

@app.route('/')
@login_required
def index():
    return render_template('index.html', user=session.get('user'))

# Login route (supports normal form POST and AJAX/JSON)
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Accept JSON or form-encoded
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    else:
        data = request.form
        username = data.get('username')
        password = data.get('password')

    users = load_json(USERS_FILE)
    user = next((u for u in users if u['username'] == username), None)
    if user and check_password_hash(user['password'], password):
        # set session
        session['user'] = {'username': user['username'], 'role': user.get('role','user')}
        session.permanent = True  # helps keep cookie stable during dev
        wants_json = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in (request.headers.get('Accept') or '')
        if wants_json or request.is_json:
            return jsonify({'ok': True, 'username': user['username']})
        return redirect(url_for('index'))

    wants_json = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in (request.headers.get('Accept') or '')
    if wants_json or request.is_json:
        return jsonify({'ok': False, 'error': 'Invalid credentials'}), 401
    return render_template('login.html', error='Invalid credentials')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    data = request.form
    username = data.get('username').strip()
    password = data.get('password')
    confirm = data.get('confirm')

    if not username or not password:
        return render_template('register.html', error='Username and password required')

    if password != confirm:
        return render_template('register.html', error='Passwords do not match')

    users = load_json(USERS_FILE)
    if any(u['username'] == username for u in users):
        return render_template('register.html', error='Username already taken')

    hashed = generate_password_hash(password)
    users.append({'username': username, 'password': hashed, 'role': 'user'})
    save_json(USERS_FILE, users)
    return render_template('login.html', message='Registration successful. Please log in.')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Add student (protected)
@app.route('/add_student', methods=['POST'])
@login_required
def add_student():
    try:
        data = request.form
        name = data.get('name')
        marks_raw = data.get('marks')
        if not name or not marks_raw:
            return jsonify({'error':'name and marks required'}), 400
        try:
            marks = int(marks_raw)
        except ValueError:
            return jsonify({'error':'marks must be an integer'}), 400

        semester = data.get('semester')
        college = data.get('college')
        student_id = data.get('student_id')

        students = load_json(STUDENTS_FILE)
        sid = 1 if not students else max(s['id'] for s in students) + 1
        grade = calculate_grade(marks)
        record = {
            'id': sid,
            'student_id': student_id,
            'name': name,
            'marks': marks,
            'grade': grade,
            'semester': semester,
            'college': college
        }
        students.append(record)
        save_json(STUDENTS_FILE, students)
        return jsonify({'message': 'Student added', 'student': record})
    except Exception as e:
        # log server-side
        import traceback
        print("add_student exception:", traceback.format_exc())
        return jsonify({'error':'internal_server_error', 'msg': str(e)}), 500

# Get students (supports search & filter query params)
@app.route('/get_students')
@login_required
def get_students():
    q = request.args.get('q', '').lower()
    semester = request.args.get('semester')
    college = request.args.get('college')

    students = load_json(STUDENTS_FILE)
    def matches(s):
        if q:
            if q in str(s.get('name','')).lower() or q in str(s.get('student_id','')).lower():
                return True
            return False
        return True

    filtered = [s for s in students if matches(s)]
    if semester:
        filtered = [s for s in filtered if str(s.get('semester','')) == str(semester)]
    if college:
        filtered = [s for s in filtered if college.lower() in str(s.get('college','')).lower()]

    return jsonify(filtered)

# Update student
@app.route('/update_student/<int:id>', methods=['PUT'])
@login_required
def update_student(id):
    data = request.json or {}
    students = load_json(STUDENTS_FILE)
    s = next((x for x in students if x['id'] == id), None)
    if not s:
        return jsonify({'error':'Not found'}), 404
    s['name'] = data.get('name', s['name'])
    if 'marks' in data:
        s['marks'] = int(data['marks'])
        s['grade'] = calculate_grade(s['marks'])
    s['semester'] = data.get('semester', s.get('semester'))
    s['college'] = data.get('college', s.get('college'))
    save_json(STUDENTS_FILE, students)
    return jsonify({'message':'Updated','student': s})

# Delete student
@app.route('/delete_student/<int:id>', methods=['DELETE'])
@login_required
def delete_student(id):
    students = load_json(STUDENTS_FILE)
    new = [s for s in students if s['id'] != id]
    if len(new) == len(students):
        return jsonify({'error':'Not found'}), 404
    save_json(STUDENTS_FILE, new)
    return jsonify({'message':'Deleted'})

# Simple stats for chart
@app.route('/stats')
@login_required
def stats():
    students = load_json(STUDENTS_FILE)
    data = sorted(students, key=lambda x: x['marks'], reverse=True)[:50]
    return jsonify({'labels':[s['name'] for s in data],'marks':[s['marks'] for s in data]})

# Debug endpoint to check session
@app.route('/whoami')
def whoami():
    return jsonify({'session_user': session.get('user')})

# Temporary debug add (no auth) — remove after debugging if you want
@app.route('/debug_add', methods=['POST'])
def debug_add():
    try:
        data = request.form
        name = data.get('name', 'DebugName')
        marks_raw = data.get('marks', '55')
        try:
            marks = int(marks_raw)
        except:
            return jsonify({'error':'marks must be integer', 'marks_raw': marks_raw}), 400

        students = load_json(STUDENTS_FILE)
        sid = 1 if not students else max(s['id'] for s in students) + 1
        rec = {'id': sid, 'student_id': data.get('student_id'),'name': name, 'marks': marks, 'grade': calculate_grade(marks), 'semester': data.get('semester'), 'college': data.get('college')}
        students.append(rec)
        save_json(STUDENTS_FILE, students)
        print("DEBUG_ADD: wrote record:", rec)
        return jsonify({'message':'debug added','student':rec,'path':os.path.abspath(STUDENTS_FILE)})
    except Exception as e:
        import traceback
        print("DEBUG_ADD exception:", traceback.format_exc())
        return jsonify({'error':'exception','msg': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
# --- Diagnostic endpoint: returns session, headers, form/json body, and students.json path+contents
@app.route('/debug_status', methods=['GET','POST'])
def debug_status():
    try:
        info = {}
        info['session_user'] = session.get('user')
        # headers (only a few useful ones)
        info['headers'] = {
            'Host': request.headers.get('Host'),
            'Cookie': request.headers.get('Cookie'),
            'X-Requested-With': request.headers.get('X-Requested-With'),
            'Accept': request.headers.get('Accept'),
            'Content-Type': request.headers.get('Content-Type')
        }
        # show how the server sees incoming data
        if request.method == 'POST':
            if request.is_json:
                info['body_json'] = request.get_json()
            else:
                info['form'] = request.form.to_dict()
                # also list files if any
                info['files'] = list(request.files.keys())
        else:
            info['query'] = request.args.to_dict()

        # students.json path and a small preview of its contents
        info['students_path'] = os.path.abspath(STUDENTS_FILE)
        try:
            data = load_json(STUDENTS_FILE)
            info['students_count'] = len(data)
            info['students_preview'] = data[-10:]  # last 10 entries
        except Exception as e:
            info['students_error'] = str(e)

        return jsonify({'ok': True, 'debug': info})
    except Exception as e:
        import traceback
        return jsonify({'ok': False, 'error': str(e), 'trace': traceback.format_exc()}), 500
