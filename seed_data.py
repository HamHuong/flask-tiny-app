# seed_data.py
from website import create_app
from website.database import db, User, Post

app = create_app()

# Dữ liệu giả lập
with app.app_context():
    # Tạo người dùng giả lập nếu chưa tồn tại
    user = User.query.filter_by(username='admin').first()
    if not user:
        user = User(
            username='admin',
            email='admin@example.com',
            password='hashedpassword',  # Giả lập, không cần hash thật
            blocked=False
        )
        db.session.add(user)
        db.session.commit()

    # Tạo 50 bài viết giả lập
    for i in range(50):
        post = Post(
            content=f"Sample post {i+1}: This is a test post to demonstrate pagination functionality.",
            user='admin'
        )
        db.session.add(post)
    
    db.session.commit()
    print("Successfully added 50 sample posts for pagination testing!")