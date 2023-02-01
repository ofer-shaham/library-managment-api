from flask import Blueprint
# from flask import request
from flask import Flask, jsonify, request

from flaskr import db
# from flaskr.auth.views import login_required
from flaskr.library.Author import Author

bp = Blueprint("author", __name__, url_prefix="/author")


@bp.route('/')
def hello_world():
    return 'Hello, World!'
