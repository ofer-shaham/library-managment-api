from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.library.models import db
from flaskr.auth.views import login_required
from flaskr.library.Post import Post

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    select = db.select(Post).order_by(Post.created.desc())
    posts = db.session.execute(select).scalars()
    return render_template("blog/index.html", posts=posts)


def get_post(id, check_user=True):
    """Get a post and its user by id.

    Checks that the id exists and optionally that the current user is
    the user.

    :param id: id of post to get
    :param check_user: require the current user to be the user
    :return: the post with user information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the user
    """
    post = db.get_or_404(Post, id, description=f"Post id {id} doesn't exist.")

    if check_user and post.user != g.user:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db.session.add(Post(title=title, body=body, user=g.user))
            db.session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the user."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    user of the post.
    """
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog.index"))
