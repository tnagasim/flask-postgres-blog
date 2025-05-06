import os
from datetime import datetime

import pytz
from flask import (
    Flask,
    redirect,
    render_template,
    request,
)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)
migrate.init_app(app, db)


class Post(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    tokyo_timezone = pytz.timezone("Asia/Tokyo")
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(tokyo_timezone)
    )


@app.route("/admin")
def admin():
    posts = Post.query.order_by(Post.id).all()
    return render_template("admin.html", posts=posts)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return redirect("/admin")
    elif request.method == "GET":
        return render_template("create.html", method="get")


@app.route("/<int:post_id>/update", methods=["GET", "POST"])
def update(post_id):
    post = Post.query.get(post_id)
    if request.method == "POST":
        post.title = request.form.get("title")
        post.body = request.form.get("body")
        db.session.commit()
        return redirect("/admin")
    elif request.method == "GET":
        return render_template("update.html", post=post)


@app.route("/<int:post_id>/delete", methods=["GET", "POST"])
def delete(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/admin")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
