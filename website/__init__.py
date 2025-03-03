# website/__init__.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Import blueprints và biến users, posts từ auth
from .views import views
from .auth import auth, users, posts, save_users, save_posts  # Import thêm save_posts

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
            save_posts()  # Lưu posts vào file sau khi thêm
            print(f"Posts after adding: {posts}")  # Debug
            flash('Post added successfully!', 'success')
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
                            save_users()  # Lưu users
                            print(f"Users after block: {users}")
                            flash(f'User {username} has been blocked.', 'success')
                        elif action == 'reset':
                            users[username]['password'] = generate_password_hash('newpassword')
                            save_users()  # Lưu users
                            print(f"Users after reset: {users}")
                            flash(f'Password for {username} has been reset to "newpassword".', 'success')
                else:
                    flash(f'User {username} not found.', 'danger')

        # Lọc danh sách người dùng để không bao gồm admin
        filtered_users = {username: user for username, user in users.items() if username != 'admin'}
        return render_template('admin.html', users=filtered_users)

    # Route cho quản lý bài viết
    @app.route('/posts', methods=['GET', 'POST'])
    def manage_posts():
        if 'username' not in session:
            flash('Please log in to manage your posts.', 'danger')
            return redirect(url_for('auth.login'))

        if request.method == 'POST':
            # Xử lý xóa nhiều bài viết
            if 'delete' in request.form:
                selected_post_ids = request.form.getlist('post_ids')  # Lấy danh sách ID bài viết được chọn
                # Chuyển post_ids thành kiểu int và xóa bài viết
                selected_post_ids = [int(pid) for pid in selected_post_ids]
                global posts
                posts = [post for post in posts if post['id'] not in selected_post_ids]
                save_posts()  # Lưu posts sau khi xóa
                print(f"Posts after deleting: {posts}")
                flash('Selected posts have been deleted.', 'success')

        # Lọc bài viết của người dùng hiện tại
        user_posts = [post for post in posts if post['user'] == session['username']]
        return render_template('posts.html', posts=user_posts)

    return app