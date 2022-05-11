
# the course class will return the course by searches using keyword, id, and instructor_id
class Course:

    # constructor
    def __init__(self, course_id=-1, course_title="", course_image_100x100="", course_headline="",
                 course_num_subscribers=-1, course_avg_rating=-1.0, course_content_length=-1.0):
        self.course_id = course_id
        self.course_title = course_title
        self.course_image_100x100 = course_image_100x100
        self.course_headline = course_headline
        self.course_num_subscribers = course_num_subscribers
        self.course_avg_rating = course_avg_rating
        self.course_content_length = course_content_length

    # This method will return the matched course by keyword as course object
    def find_course_by_title_keyword(self, keyword):
        # opening the file and reading the lines
        with open("./data/result/course.txt", "r+") as course_file:
            course_data = course_file.readlines()
            # empty list to append the matches
            result = []
            for each in course_data:
                # splitting the title from the lines of course text file
                title = each.split(";;;")[1].lower()
                # if keyword matches with the course title then appending the course objects to result list
                if keyword in title:
                    course_id = each.split(";;;")[0]
                    course_title = each.split(";;;")[1]
                    course_image_100x100 = each.split(";;;")[2]
                    course_headline = each.split(";;;")[3]
                    course_num_subscribers = each.split(";;;")[4]
                    course_avg_rating = each.split(";;;")[5]
                    course_content_length = each.split(";;;")[6]
                    result.append(Course(int(course_id), course_title, course_image_100x100, course_headline,
                                         int(course_num_subscribers), float(course_avg_rating),
                                         float(course_content_length)))
        # returning the result list
        return result

    # this method will return the course matched by id as course object
    def find_course_by_id(self, course_id):
        # opening the file
        with open("./data/result/course.txt", "r+") as course_file:
            # reading lines
            course_data = course_file.readlines()
            for each in course_data:
                # stripping the course id from lines of text file
                course_id_data = each.split(";;;")[0]
                # if the course id matches with the id in the text file returning the course as course object
                if str(course_id) == course_id_data:
                    course_title = each.split(";;;")[1]
                    course_image_100x100 = each.split(";;;")[2]
                    course_headline = each.split(";;;")[3]
                    course_num_subscribers = each.split(";;;")[4]
                    course_avg_rating = each.split(";;;")[5]
                    course_content_length = each.split(";;;")[6]
                    course = Course(int(course_id_data), course_title, course_image_100x100, course_headline,
                                    int(course_num_subscribers), float(course_avg_rating),
                                    float(course_content_length))
                    break
                # if no match found then returning None
                else:
                    course = None
        return course

    # this method will return the matched courses by instructor id as course objects
    def find_course_by_instructor_id(self, instructor_id):
        # opening and reading lines of user instructor text
        with open("./data/result/user_instructor.txt", "r+") as instructor_doc:
            instructor_data = instructor_doc.readlines()
            result = []
            # empty list to store all course ids of an instructor
            all_course_id = []
            for each in instructor_data:
                # splitting the instructor ids
                instructor_id_data = each.split(";;;")[0]
                # matching instructor id with the data created above
                if str(instructor_id) == instructor_id_data:
                    temp_course_id = each.split(";;;")[-1].strip("\n")
                    # appending the match to all course id list
                    all_course_id.append(temp_course_id.split("--"))

            # reading the course text to find the course using course id
            with open("./data/result/course.txt", "r+") as course_file:
                course_data = course_file.readlines()
                for each in course_data:
                    course_id_data = each.split(";;;")[0]
                    for line in all_course_id:
                        for id in line:
                            # if the id of the all course id list matches then appending the course to the result list
                            if id == course_id_data:
                                course_title = each.split(";;;")[1]
                                course_image_100x100 = each.split(";;;")[2]
                                course_headline = each.split(";;;")[3]
                                course_num_subscribers = each.split(";;;")[4]
                                course_avg_rating = each.split(";;;")[5]
                                course_content_length = each.split(";;;")[6]
                                result.append(Course(int(course_id_data), course_title, course_image_100x100,
                                                 course_headline, int(course_num_subscribers), float(course_avg_rating),
                                                 float(course_content_length)))

        # returning the courses as course object
        return result

    # This method returns the course length
    def course_overview(self):
        with open("./data/result/course.txt", "r+") as course_file:
            course_data = course_file.readlines()
            course_length = str(len(course_data))
            return course_length

    # str return function formats the return string as shown below
    def __str__(self):
        return_format = str(self.course_id) + ";;;" + self.course_title + ";;;" + self.course_image_100x100 \
                        + ";;;" + self.course_headline + ";;;" + str(self.course_num_subscribers) + \
                        ";;;" + str(self.course_avg_rating) + ";;;" + str(self.course_content_length) + "\n"
        return return_format



