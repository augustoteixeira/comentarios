import os
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.String(2500), nullable=False)

    def __repr__(self):
        return "<Comment: {}>".format(self.id)

#db.create_all()

@app.route("/comments/single/<label>/")
def get_comments(label):
    comments = Comment.query.filter_by(chapter_id=label)
    return render_template("comentarios.html", label=label,
                           comments=comments)

@app.route("/comments/submit/<label>/", methods=['POST'])
def submit_comments(label):
    new_comment = Comment(chapter_id=request.form['id'],
                          author=request.form['name'],
                          url=request.form['url'],
                          body=request.form['comment'])
    db.session.add(new_comment)
    db.session.commit()
    return get_comments(label)

@app.route("/admin/comments/comment/<id>/<password>")
def deletar(id, password):
    if (password != "fantacaju"):
        return ""
    comment = Comment.query.filter_by(id=id).one()
    db.session.delete(comment)
    db.session.commit()
    return "Comment deleted"

@app.route("/comments/chapter/<chapter>/count")
def counter(chapter):
    list = ( db.session.query(Comment.chapter_id,
                              func.count(Comment.chapter_id))
             .group_by(Comment.chapter_id).all() )
    resp = {}
    for a in list:
        resp[a[0]] = a[1]
    return jsonify( resp )

if __name__ == "__main__":
    app.run(host='0.0.0.0')


