from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from . import db
from .models import BlogPost, User
from .decorators import ownership_required

views = Blueprint("views", __name__)


@views.route("/")
def home():
    all_blog_posts = BlogPost.query.all()
    return render_template("index.html", all_blog_posts=all_blog_posts)

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/contact")
def contact():
    return render_template("contact.html")


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        data = request.form
        title = data.get("title")
        content = data.get("content")
        if title.strip() == "" or content.strip() == "":
            flash("Title or Content cannot be empty", "error")
        else:
            blog_post = BlogPost(title=title, content=content, author=current_user.id)
            db.session.add(blog_post)
            db.session.commit()
            flash("Blog Post created successfully!")
            return redirect(url_for("views.blog_post", blog_post_id=blog_post.id))
    return render_template("create_post.html")

@views.route("/blog-post/<int:blog_post_id>", methods=["GET", "POST"])
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get(blog_post_id)
    return render_template("post.html", blog_post=blog_post, current_user=current_user)

@views.route("/delete-blog-post/<int:blog_post_id>", methods=["GET", "POST"])
@login_required
@ownership_required
def delete_blog_post(blog_post_id):
    blog_post = BlogPost.query.get(blog_post_id)
    db.session.delete(blog_post)
    db.session.commit()
    flash("Post Deleted Successfully")
    return redirect(url_for("views.home"))

@views.route("/edit-blog-post/<int:blog_post_id>", methods=["GET", "POST"])
@login_required
@ownership_required
def edit_blog_post(blog_post_id):
    blog_post = BlogPost.query.get(blog_post_id)
    if request.method == "POST":
        data = request.form
        title = data.get("title")
        content = data.get("content")
        if title.strip() == "" or content.strip() == "":
            flash("Title or Content cannot be empty", "error")
        else:
            blog_post.title = title
            blog_post.content = content
            db.session.commit()
        flash("Post Edited Successfully")
        return redirect(url_for("views.blog_post", blog_post_id=blog_post.id))
    print(blog_post.title)
    return render_template("edit_post.html", title=blog_post.title, content=blog_post.content)

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    all_blog_posts = BlogPost.query.filter_by(author=user.id).all()
    return render_template("user_posts.html", user=current_user, all_blog_posts=all_blog_posts, username=username)
