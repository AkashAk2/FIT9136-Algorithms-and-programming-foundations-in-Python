from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.course import Course
from model.user import User
from model.user_admin import Admin
from model.user_instructor import Instructor
from model.user_student import Student

user_page = Blueprint("user_page", __name__)

model_user = User()
model_course = Course()
model_student = Student()


def generate_user(login_user_str):
    login_user = None  # a User object
    user_info_list = (login_user_str.strip("\n")).split(";;;")
    if user_info_list[4] == "admin":
        login_user = Admin(int(user_info_list[0]), user_info_list[1], user_info_list[2], user_info_list[3],
                           user_info_list[4])
    elif user_info_list[4] == "instructor":
        course_list = user_info_list[8].strip("\n").split("--")
        login_user = Instructor(uid=int(user_info_list[0]), username=user_info_list[1], password=user_info_list[2],
                                register_time=user_info_list[3], role=user_info_list[4], email=user_info_list[5],
                                display_name=user_info_list[6], job_title=user_info_list[7],
                                course_id_list=course_list)
    elif user_info_list[4] == "student":
        login_user = Student(int(user_info_list[0]), user_info_list[1], user_info_list[2], user_info_list[3],
                             user_info_list[4])
    print(type(login_user))
    return login_user


# use @user_page.route("") for each page url

@user_page.route("/login", methods=["GET"])
def login():
    return render_template("00login.html")


@user_page.route("/login", methods=["POST"])
def login_post():
    req = request.values
    username = req["username"] if "username" in req else "null"
    password = req["password"] if "password" in req else "null"
    # context = {}
    # context["user_obj"] = User()
    if model_user.validate_username(username) is True and model_user.validate_password(password) is True:
        authentication = model_user.authenticate_user(username, password)
        print(authentication)
        if authentication[0] is True:
            user_info_str = (authentication[1]).strip("\n")
            User.current_login_user = generate_user(user_info_str)
            return render_result("Successfully logged in!")
        else:
            return render_err_result("Login failed! Check your username or password.")


@user_page.route("/logout", methods=["GET"])
def logout():
    User.current_login_user = None
    return render_template("01index.html")


@user_page.route("/register", methods=["GET"])
def register():
    return render_template("00register.html")


@user_page.route("/register", methods=["POST"])
def register_post():
    req = request.values
    username = req["username"] if "username" in req else "null"
    password = req["password"] if "password" in req else "null"
    register_time = req["register_time"] if "register_time" in req else "null"
    role = req["role"] if "role" in req else "null"
    email = req["email"] if "email" in req else "null"
    if model_user.validate_username(username) == True and model_user.validate_password(
            password) == True and model_user.validate_email(email) == True:
        model_user.register_user(username=username, password=password,
                                 register_time=register_time, role=role, email=email)
        return render_result("User registration completed!")
    else:
        return render_err_result("User registration failed! Try again.")


@user_page.route("/student-list", methods=["GET"])
def student_list():
    if User.current_login_user is not None:
        req = request.values
        page = req['page'] if "page" in req else 1
        context = {}
        # get values for one_page_instructor_list, total_pages, total_num
        student_details = model_student.get_students_by_page(page)
        one_page_user_list = student_details[0]
        total_pages = student_details[1]
        total_num = student_details[2]
        # get values for page_num_list
        page_num_list = model_course.generate_page_num_list(page=page, total_pages=total_pages)
        # check one_page_instructor_list, make sure this variable not be None, if None, assign it to []
        if one_page_user_list is None:
            context['one_page_instructor_list'] = []
        else:
            context['one_page_instructor_list'] = one_page_user_list
        context['total_pages'] = total_pages
        context['page_num_list'] = page_num_list
        context['current_page'] = int(page)
        context['total_num'] = total_num
        # add "current_user_role" to context
        context["current_user_role"] = User.current_login_user.role
    else:
        return redirect(url_for("index_page.index"))

    return render_template("07instructor_list.html", **context)


@user_page.route("/student-info", methods=["GET"])
def student_info():
    req = request.values
    context = {}
    if User.current_login_user is not None:
        stud_id = int(req["id"]) if "id" in req else model_student.uid
        stud_object = model_student.get_student_by_id(stud_id)
        context['current_user_role'] = User.current_login_user.role
        return stud_object
    else:
        return render_err_result("Something went wrong while getting student information")


@user_page.route("/student-delete", methods=["GET"])
def student_delete():
    req = request.values
    stud_id = int(req['id'])
    result = model_student.delete_student_by_id(stud_id)
    if result is True:
        return redirect(url_for("user_page.student_list"))
    else:
        return redirect(url_for("index_page.index"))
