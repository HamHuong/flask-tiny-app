# website/__init__.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Import blueprints từ các file khác
from .views import views
from .auth import auth
from .database import db, User, Post

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Hamhuong@135'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Khởi tạo database với ứng dụng
    db.init_app(app)

    # Đăng ký blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Tạo database nếu chưa tồn tại
    with app.app_context():
        db.create_all()

    # Route cho blog với phân trang
    @app.route('/', methods=['GET', 'POST'])
    def blog():
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        
        if request.method == 'POST':
            content = request.form['content']
            new_post = Post(content=content, user=session['username'])
            db.session.add(new_post)
            db.session.commit()
            flash('Post added successfully!', 'success')

        page = request.args.get('page', 1, type=int)
        per_page = 10
        paginated_posts = Post.query.order_by(Post.id.asc()).paginate(page=page, per_page=per_page, error_out=False)
        total_pages = paginated_posts.pages

        return render_template('blog.html', posts=paginated_posts.items, page=page, total_pages=total_pages)

    # Route cho trang admin
    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        if 'username' not in session:
            flash('Please log in to access the admin page.', 'danger')
            return redirect(url_for('auth.login'))
        if session['username'] != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('blog'))

        if request.method == 'POST':
            if 'username' not in request.form or 'action' not in request.form:
                flash('Invalid form submission: Missing username or action.', 'danger')
            else:
                action = request.form['action']
                username = request.form['username']
                user = User.query.filter_by(username=username).first()
                if user:
                    if username == 'admin':
                        flash('Cannot perform actions on the admin account.', 'danger')
                    else:
                        if action == 'block':
                            user.blocked = True
                            db.session.commit()
                            flash(f'User {username} has been blocked.', 'success')
                        elif action == 'unblock':
                            user.blocked = False
                            db.session.commit()
                            flash(f'User {username} has been unblocked.', 'success')
                        elif action == 'reset':
                            user.password = generate_password_hash('newpassword')
                            db.session.commit()
                            flash(f'Password for {username} has been reset to "newpassword".', 'success')
                else:
                    flash(f'User {username} not found.', 'danger')

        filtered_users = User.query.filter(User.username != 'admin').all()
        return render_template('admin.html', users=filtered_users)

    # Route cho quản lý bài viết với phân trang
    @app.route('/posts', methods=['GET', 'POST'])
    def manage_posts():
        if 'username' not in session:
            flash('Please log in to manage your posts.', 'danger')
            return redirect(url_for('auth.login'))

        if request.method == 'POST':
            if 'delete' in request.form:
                selected_post_ids = request.form.getlist('post_ids')
                selected_post_ids = [int(pid) for pid in selected_post_ids]
                Post.query.filter(Post.id.in_(selected_post_ids), Post.user == session['username']).delete(synchronize_session='fetch')
                db.session.commit()
                flash('Selected posts have been deleted.', 'success')
            elif 'edit' in request.form:
                post_id = request.form.get('post_id')
                content = request.form.get('content')
                post = Post.query.filter_by(id=post_id, user=session['username']).first()
                if post:
                    post.content = content
                    db.session.commit()
                    flash('Post updated successfully!', 'success')
                else:
                    flash('Post not found or you do not have permission.', 'danger')

        page = request.args.get('page', 1, type=int)
        per_page = 10
        paginated_posts = Post.query.filter_by(user=session['username']).order_by(Post.id.asc()).paginate(page=page, per_page=per_page, error_out=False)
        total_pages = paginated_posts.pages

        return render_template('posts.html', posts=paginated_posts.items, page=page, total_pages=total_pages)

    # Route để xem chi tiết bài viết
    @app.route('/post/<int:post_id>')
    def view_post(post_id):
        post = Post.query.get_or_404(post_id)
        return render_template('post_detail.html', post=post)

    return app