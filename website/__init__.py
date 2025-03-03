# website/__init__.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Import blueprints và biến users, posts từ auth
from .views import views
from .auth import auth, users, posts

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Hamhuong@135'

    # Đăng ký blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Route cho blog
    @app.route('/', methods=['GET', 'POST'])
    def blog():
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        if request.method == 'POST':
            content = request.form['content']
            posts.append({'id': len(posts) + 1, 'content': content, 'user': session['username']})
        return render_template('blog.html', posts=posts)

    # Route cho trang admin
    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        # Kiểm tra nếu người dùng không đăng nhập hoặc không phải admin
        if 'username' not in session:
            flash('Please log in to access the admin page.', 'danger')
            return redirect(url_for('auth.login'))
        if session['username'] != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('blog'))

        # Xử lý hành động từ form (block hoặc reset password)
        if request.method == 'POST':
            # Kiểm tra xem username và action có trong form không
            if 'username' not in request.form or 'action' not in request.form:
                flash('Invalid form submission: Missing username or action.', 'danger')
            else:
                action = request.form['action']
                username = request.form['username']
                if username in users:
                    if username == 'admin':
                        flash('Cannot perform actions on the admin account.', 'danger')
                    else:
                        if action == 'block':
                            users[username]['blocked'] = True
                            print(f"Users after block: {users}")  # Debug: In trạng thái users
                            flash(f'User {username} has been blocked.', 'success')
                        elif action == 'reset':
                            users[username]['password'] = generate_password_hash('newpassword')
                            print(f"Users after reset: {users}")  # Debug: In trạng thái users
                            flash(f'Password for {username} has been reset to "newpassword".', 'success')
                else:
                    flash(f'User {username} not found.', 'danger')

        # Lọc danh sách người dùng để không bao gồm admin
        filtered_users = {username: user for username, user in users.items() if username != 'admin'}
        return render_template('admin.html', users=filtered_users)

    return app