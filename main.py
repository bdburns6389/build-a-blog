from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'root' #should be a better key for security purposes, but oh well, right?


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self,title,body):
        self.title = title
        self.body = body


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        new_entry = Blog(blog_title, blog_body)
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/blog')
    
    return render_template('newpost.html')


@app.route('/blog', methods=['POST','GET'])
def blog():
    id_exists = request.args.get('id')
    if id_exists:
        individual_entry = Blog.query.get(id_exists)
        return render_template('singlepost.html', individual_entry=individual_entry)
    else:
        entries= Blog.query.all()
        return render_template('blog.html', entries=entries)


@app.route('/', methods=['POST', 'GET'])
def index():
    entries = Blog.query.all()
    print(dir(Blog))
    return render_template('blog.html', entries=entries)

if __name__ == "__main__":
    app.run()

