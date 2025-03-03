from flask import Flask, render_template, request

app = Flask(__name__)
posts = []

@app.route('/', methods = ['GET','POST'])
def blog():
    if request.method == 'POST':
        content = request.form['content']
        posts.append({'id': len(posts)+1, 'content': content})
    return render_template('blog.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)