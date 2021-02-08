from flask import Blueprint, render_template

user = Blueprint('user', __name__)


@user.route('/me')
def me_route():
    return render_template('pages/user/index.html')
