
from flask import render_template, Blueprint

from model.user import User
from model.user_admin import Admin


index_page = Blueprint("index_page", __name__)

@index_page.route("/", methods=["GET"])
def index():

    # check the class variable User.current_login_user
    context = {}
    context["current_user"] = User()
    if context["current_user"].current_login_user != None:
        context["current_user_role"] = User.current_login_user.role

    # manually register an admin account when open index page
    context["admin_account"] = Admin(username="admin", password="admin")
    encrypted_pass = context["current_user"].encrypt_password(context["admin_account"].password)
    with open("./data/user.txt", "r+", encoding="utf-8") as user_text:
        text_data = user_text.readlines()
        admin_list = []
        for each in text_data:
            temp_role = (each.split(";;;")[4]).strip("\n")
            if temp_role == "admin":
                admin_list.append(each)
        if len(admin_list) == 0:
            context["admin_account"].register_admin()
        else:
            for item in admin_list:
                temp_username = item.split(";;;")[1]
                temp_password = item.split(";;;")[2]
                if temp_username == context["admin_account"].username and temp_password == encrypted_pass:
                    print("User already existing")
                else:
                    context["admin_account"].register_admin()

    return render_template("01index.html", **context)

