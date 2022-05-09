from User import User
from Course import Course
from Instructor import Instructor

class Student:
    def __init__(self, id = -1, username = "", password = "", user_title = "", user_image_50x50 = "",
                 user_initials = "", review_id = -1):
        self.id = id
        self.username = username
        self.password = password
        self.user_title = user_title
        self.user_image_50x50 = user_image_50x50
        self.user_initials = user_initials
        self.review_id = review_id

    def view_courses(self, args = []):

        with open("./data/result/user_student.txt", "r") as student_doc:
            student_details = student_doc.readlines()
            for each in student_details:
                student_id_in_doc = each.split(";;;")[0]
                # print(student_id_in_doc)
                if str(self.id) == student_id_in_doc:
                    review_id = each.split(";;;")[-1].replace("\n","")
        #
        # with open("./data/result/review.txt", "r") as review_doc:
        #     review_data = review_doc.readlines()
        #     for line in review_data:
        #         course_id_in_review = line.split(";;;")[-1].replace("\n", "")
        #         if review_id == course_id_in_review:
        #             course_id += course_id_in_review
        #
        # with open("./data/result/course.txt", "r+") as course_file:
        #     course_data = course_file.readlines()
        #     for each in course_data:
        #         course_id_data = each.split(";;;")[0]
        #         if course_id == course_id_data:
        #             print(each)


student = Student(id = 25332022)
student.view_courses()