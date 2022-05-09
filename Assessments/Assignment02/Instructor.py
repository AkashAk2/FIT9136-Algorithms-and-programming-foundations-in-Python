from User import User
from Course import Course


class Instructor:

    def __init__(self, id = -1, username = "", password = "", display_name = "", job_title = "", image_100x100 = "",
                 course_id_list = []):
        self.id = id
        self.username = username
        self.password = password
        self.display_name = display_name
        self.job_title = job_title
        self.image_100x100 = image_100x100
        self.course_id_list = course_id_list

    def view_courses(self, args = []):
        courses = Course.find_course_by_instructor_id(self, self.id)
        if len(courses) > 10:
            for each in courses:
                for item in range(10):
                    print(each)
        else:
            for each in courses:
                print(each)

    def view_reviews(self, args = []):
        courses = Course.find_course_by_instructor_id(self, self.id)
        result = []
        for each in courses:
            # print(each)
            temp_course_id = each.split(";;;")[0]
            course_id_list = temp_course_id.split("--")
            with open("./data/result/review.txt", "r") as review_doc:
                review_data = review_doc.readlines()
                # print(review_data)
                for line in review_data:
                    course_id_in_review = line.split(";;;")[-1].replace("\n", "")
                    # print(course_id_in_review)
                    for item in course_id_list:
                        if item == course_id_in_review:
                            result.append(line)
                            # print(line, course_id_list)
        # print(len(result))
        if len(result) > 10:
            sliced_list = result[0:10]
            for each in sliced_list:
                print(each)
            print("The total reviews for the instructor are: ", len(result))

        else:
            for each in result:
                print(each)
            print("The total reviews for the instructor are: ", len(result))

    # def __str__(self):
    #     User.__str__(self)



# instructor = Instructor(id = 13363166)
# # instructor.view_courses()
# instructor.view_reviews()








