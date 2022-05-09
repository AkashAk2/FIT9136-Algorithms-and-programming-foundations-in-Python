
class Course:
    def __init__(self, course_id = -1, course_title = "", course_image_100x100 = "", course_headline = "",
                 course_num_subscribers = -1, course_avg_rating = -1.0, course_content_length = -1):
        self.course_id = course_id
        self.course_title = course_title
        self.course_image_100x100 = course_image_100x100
        self.course_headline = course_headline
        self.course_num_subscribers = course_num_subscribers
        self.course_avg_rating = course_avg_rating
        self.course_content_length = course_content_length

    def find_course_by_title_keyword(self, keyword):
        with open("./data/result/course.txt", "r+") as course_file:
            course_data = course_file.readlines()
            result = []
            for each in course_data:
                title = each.split(";;;")[1].lower()
                if keyword in title:
                    result.append(each)
        return result

    def find_course_by_id(self, course_id):
        with open("./data/result/course.txt", "r+") as course_file:
            course_data = course_file.readlines()
            for each in course_data:
                course_id_data = each.split(";;;")[0]
                if str(course_id) == course_id_data:
                    course = each
                    break
                else:
                    course = None
        return course

    def find_course_by_instructor_id(self, instructor_id):
        with open("./data/result/user_instructor.txt", "r+") as instructor_doc:
            instructor_data = instructor_doc.readlines()
            result = []
            for each in instructor_data:
                instructor_id_data = each.split(";;;")[0]
                if str(instructor_id) == instructor_id_data:
                    match = each
                    temp_course_id = each.split(";;;")[-1].replace("\n", "")
                    course_id_list = temp_course_id.split("--")
                    # print(match)
                    # print(course_id)

        with open("./data/result/course.txt", "r+") as course_file:
            course_data = course_file.readlines()
            for each in course_data:
                course_id_data = each.split(";;;")[0]
                for item in course_id_list:
                    # print(item)
                    if item == course_id_data:
                        result.append(each)
                        # print(each)
        # print(result)
        return result

    def course_overview(self):
        with open("./data/result/course.txt", "r+") as course_file:
            course_data = course_file.readlines()
            course_length = len(course_data)
            # print(course_length)
            return course_length

    def __str__(self):
        with open("./data/result/course.txt", "r+") as course_file:
            course_data = course_file.readlines()
            for each in course_data:
                return each


course1 = Course()
# course1.find_course_by_title_keyword("developer")
# course1.find_course_by_id(851712)
# course1.find_course_by_instructor_id("13363166")
course1.course_overview()