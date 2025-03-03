
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from .views import views
from .auth import auth, users, posts

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Hamhuong@135'


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    @app.route('/', methods=['GET', 'POST'])
    def blog():
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        if request.method == 'POST':
            content = request.form['content']
            posts.append({'id': len(posts) + 1, 'content': content, 'user': session['username']})
        return render_template('blog.html', posts=posts)

    
    return app