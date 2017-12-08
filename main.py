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

@app.route('/')
@app.route('/blog', methods=['POST', 'GET'])
def index():
    entries = Blog.query.all()

    return render_template('blog.html', entries=entries)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        #WORK HERE !!!!!!!!!!!!!
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        new_entry = Blog(blog_title, blog_body)
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/blog')
    
    return render_template('newpost.html')





if __name__ == "__main__":
    app.run()

