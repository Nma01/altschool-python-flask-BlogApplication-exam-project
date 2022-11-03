import functools
from flask_login import current_user
from flask import flash, redirect, url_for
from .models import BlogPost

def ownership_required(view_func):
    @functools.wraps(view_func)
    def wrapper(blog_post_id):
        blog_post = BlogPost.query.get(blog_post_id)
        if current_user.id == blog_post.author:
            return view_func(blog_post_id)
        else:
            flash("You are not the Owner of the Post. You don't have write permission!", "error")
            return redirect(url_for("views.blog_post", blog_post_id=blog_post.id))
    return wrapper
    