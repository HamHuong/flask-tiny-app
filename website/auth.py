# website/auth.py
import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

# Đường dẫn đến file JSON để lưu users và posts
USERS_FILE = "users.json"
POSTS_FILE = "posts.json"

# Khởi tạo users từ file (nếu file tồn tại)
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}

# Khởi tạo posts từ file (nếu file tồn tại)
if os.path.exists(POSTS_FILE):
    with open(POSTS_FILE, 'r') as f:
        posts = json.load(f)
else:
    posts = []

# Hàm lưu users vào file JSON
def save_users():
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

# Hàm lưu posts vào file JSON
def save_posts():
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Tìm username dựa trên email
        username = next((key for key, user in users.items() if user['email'] == email), None)
        print(f"Users during login: {users}")  # Debug: In trạng thái users
        if username and username in users:
            user = users[username]
            if user['blocked']:
                flash('Tài khoản của bạn đã bị khóa.', 'danger')
                return render_template('login.html')
            if check_password_hash(user['password'], password):
                session['username'] = username
                print(f"Session set: {session['username']}")  # Debug
                return redirect('/')
        flash('Invalid email or password', 'danger')
    return render_template('login.html')

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = email.split('@')[0]
        if email not in [u['email'] for u in users.values()]:
            users[username] = {'email': email, 'password': generate_password_hash(password), 'blocked': False}
            save_users()  # Lưu users vào file sau khi thêm
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        flash('Email already exists', 'danger')
    return render_template('signup.html')

@auth.route("/logout")
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for("views.home"))