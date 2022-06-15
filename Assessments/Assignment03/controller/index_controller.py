from flask import render_template, Blueprint

from model.user import User
from model.user_admin import Admin

index_page = Blueprint("index_page", __name__)

model_user = User()

@index_page.route("/", methods=["GET"])
def index():
    # check the class variable User.current_login_user
    context = {}
    current_login_user = User.current_login_user
    if current_login_user is not None:
        context["current_user_role"] = current_login_user.role
    # manually register an admin account when open index page
    model_admin = Admin(username="admin", password="admin")
    model_admin.register_admin()
    return render_template("01index.html", **context)
