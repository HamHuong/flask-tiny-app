# website/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db, User, Post

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.blocked:
                flash('Tài khoản của bạn đã bị khóa.', 'danger')
                return render_template('login.html')
            if check_password_hash(user.password, password):
                session['username'] = user.username
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
        if not User.query.filter_by(email=email).first():
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                blocked=False
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        flash('Email already exists', 'danger')
    return render_template('signup.html')

@auth.route("/logout")
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for("views.home"))