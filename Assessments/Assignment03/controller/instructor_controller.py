from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.user import User
from model.course import Course

import pandas as pd
from flask import render_template, Blueprint

from model.user_instructor import Instructor

instructor_page = Blueprint("instructor_page", __name__)

model_instructor = Instructor()
model_course = Course()

# this method retrieves the instructor data
@instructor_page.route("/instructor-list", methods=["GET"])
def instructor_list():
    if User.current_login_user is not None:
        req = request.values
        page = int(req['page']) if "page" in req else 1 # getting page from request.values else default to 1.
        context = {}
        # get values for one_page_instructor_list, total_pages, total_num
        instructor_list = model_instructor.get_instructors_by_page(page)
        one_page_instructor_list = instructor_list[0]
        total_pages = instructor_list[1]
        total_num = instructor_list[2]
        # get values for page_num_list
        page_num_list = model_course.generate_page_num_list(page=page, total_pages=total_pages)
        # check one_page_instructor_list, make sure this variable not be None, if None, assign it to []
        if instructor_list[0] is None:
            one_page_instructor_list = []
        else:
            one_page_instructor_list = instructor_list[0]
        context['one_page_instructor_list'] = one_page_instructor_list
        context['total_pages'] = total_pages
        context['page_num_list'] = page_num_list
        context['current_page'] = int(page)
        context['total_num'] = total_num
        # add "current_user_role" to context
        context["current_user_role"] = User.current_login_user.role
    else:
        return redirect(url_for("index_page.index"))

    return render_template("07instructor_list.html", **context)

# this method retrieves instructor teaching courses
@instructor_page.route("/teach-courses", methods=["GET"])
def teach_courses():
    context = {}

    if User.current_login_user is not None:
        # get instructor id
        req = request.values
        instructor_id = int(req['id']) if 'id' in req else User.current_login_user.uid # getting user id
        # get values for course_list, total_num
        search_result = model_course.get_course_by_instructor_id(instructor_id) # getting course data
        if search_result[0] is None:
            course_list = [] # setting [] if the result is None.
        else:
            course_list = search_result[0]
        total_num = search_result[1]
        context['course_list'] = course_list
        context['total_num'] = total_num
        # add "current_user_role" to context
        context["current_user_role"] = User.current_login_user.role

    else:
        return redirect(url_for("index_page.index"))
    return render_template("09instructor_courses.html", **context)



@instructor_page.route("/instructor-analysis")
def instructor_analysis():
    # if Instructor.instructor_data.shape[0] == 0:
    #     return render_err_result(msg="no instructor in datafile")

    explain1 = model_instructor.generate_instructor_figure1()

    context = {}
    context['explain1'] = explain1

    return render_template("08instructor_analysis.html", **context)


@instructor_page.route("/process-instructor", methods=["POST"])
def process_instructor():
    try:
        model_instructor.get_instructors()
    except Exception as e:
        print(e)
        return render_err_result(msg="error in process instructors")

    return render_result(msg="process instructors finished successfully")