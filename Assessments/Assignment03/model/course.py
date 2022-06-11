import os
import json
import pandas as pd

class Course:

    def __init__(self, category_title = "", subcategory_id = -1, subcategory_title = "", subcategory_description = "",
                 subcategory_url = "", course_id = -1, course_title = "", course_url = "", num_of_subscribers = 0,
                 avg_rating = 0.0, num_of_reviews = 0):
        self.category_title = category_title
        self.subcategory_id = subcategory_id
        self.subcategory_title = subcategory_title
        self.subcategory_description = subcategory_description
        self.subcategory_url = subcategory_url
        self.course_id = course_id
        self.course_title = course_title
        self.course_url = course_url
        self.num_of_subscribers = num_of_subscribers
        self.avg_rating = avg_rating
        self.num_of_reviews = num_of_reviews

    def __str__(self):
        return self.category_title + ";;;" + str(self.subcategory_id) + ";;;" + str(self.subcategory_title) + ";;;" +\
               str(self.subcategory_description) + ";;;" + str(self.subcategory_url) + ";;;" + str(self.course_id) + \
               ";;;" + self.course_title + ";;;" + str(self.course_url) + ";;;" + str(self.num_of_subscribers) +\
               ";;;" + str(self.avg_rating) + ";;;" + str(self.num_of_reviews)


    def get_courses(self):
        files_list = list()
        for (dirpath, subdir, filenames) in os.walk("./data/source_course_files"):
            files_list += [os.path.join(dirpath, file) for file in filenames]
        for each in files_list:
            if each.endswith(".json"):
                with open(each, 'r') as course_files:
                    with open("./data/course.txt", "a+") as course_file:
                        item_data = json.load(course_files)
                        self.category_title = item_data['unitinfo']['category']
                        subcategory = item_data['unitinfo']['source_objects']
                        item = item_data['unitinfo']['items']
                        subcategory_dict = {}
                        item_dict = {}
                        for each_subcategory in subcategory:
                            subcategory_dict.update(each_subcategory)

                        self.subcategory_id = subcategory_dict['id']
                        self.subcategory_title = subcategory_dict['title']
                        self.subcategory_description = subcategory_dict['description']
                        self.subcategory_url = subcategory_dict['url']

                        for each_item in item:
                            item_dict.update(each_item)

                            self.course_id = item_dict['id']
                            self.course_title = item_dict['title']
                            self.course_url = item_dict['url']
                            self.num_of_subscribers = item_dict['num_subscribers']
                            self.avg_rating = item_dict['avg_rating']
                            self.num_of_reviews =  item_dict['num_reviews']


                            course_file.write(self.__str__())
                            course_file.write("\n")



    def clear_course_data(self):
        with open("./data/course.txt", "w+") as course_file:
            course_file.seek(0)
            course_file.truncate()

    def generate_page_num_list(self, page, total_pages):
        page_number_list = []
        if page <= 5:
            page_number_list = [1,2,3,4,5,6,7,8,9]

        if 5 < page < (total_pages - 4):
            boundary = 4
            page_number_list.append(page)
            for num in range(0,4):
                temp = page - boundary
                page_number_list.append(temp)
                temp = page + boundary
                page_number_list.append(temp)
                boundary -= 1

        elif page >= (total_pages - 4):
            boundary = 8
            page_number_list.append(total_pages)
            for num in range(0, boundary):
                temp = total_pages - boundary
                page_number_list.append(temp)
                boundary -= 1
        page_number_list.sort()
        return page_number_list




    def get_courses_by_page(self, page):
        with open("./data/course.txt", "r+") as course_file:
            course_data = course_file.readlines()
            num_of_courses = len(course_data)
            total_pages = round(num_of_courses / 20)
            line_range = page * 20
            course_list = []
            for each in range(line_range - 20, line_range):
                course = course_data[each]
                course_split_list = course.split(";;;")
                course_obj = Course(course_split_list[0], int(course_split_list[1]), course_split_list[2],
                                    course_split_list[3], course_split_list[4], int(course_split_list[5]),
                                    course_split_list[6], course_split_list[7], int(course_split_list[8]),
                                    float(course_split_list[9]), int(course_split_list[10]))
                course_list.append(course_obj)
            return (course_list, total_pages, num_of_courses)



    def delete_course_by_id(self, course_id):
        is_deleted = False
        with open("./data/course.txt", "r+") as course_file:
            course_data = course_file.readlines()
            course_file.seek(0)
            for each in course_data:
                course_id_in_text = int(each.split(";;;")[5])
                if course_id_in_text != course_id:
                    course_file.write(each)
                elif course_id_in_text == course_id:
                    is_deleted = True
            course_file.truncate()
        with open("./data/user.txt", "r+") as user_file:
            user_data = user_file.readlines()
            user_file.seek(0)
            for each in user_data:
                data_list = each.split(";;;")
                if data_list[4] == "instructor":
                    instructor_data = each.split(";;;")
                    course_id_in_user = instructor_data[-1]
                    course_id_list = course_id_in_user.split("--")
                    for item in course_id_list:
                        if course_id == int(item):
                            id_line = user_data.index(each)
                            course_id_list.remove(item)
                            result = ""
                            for num in range(len(instructor_data)-1):
                                result += instructor_data[num]
                                result += ";;;"
                            for num in range(len(course_id_list) - 1):
                                result += course_id_list[num]
                                result += "--"
                            result += course_id_list[-1]
                            user_data[id_line] = result
                            is_deleted = True
            for line in user_data:
                user_file.write(line)
            user_file.truncate()

        return is_deleted


    def get_course_by_course_id(self, temp_course_id):
        is_course_found = False
        with open("./data/course.txt", "r+") as course_file:
            course_data = course_file.readlines()
            for each in course_data:
                comment = ""
                course_id_in_text = int(each.split(";;;")[5])
                if temp_course_id == course_id_in_text:
                    num_of_subscribers = int(each.split(";;;")[-3])
                    avg_rating = round(float(each.split(";;;")[-2]), 2)
                    num_of_reviews = int(each.split(";;;")[-1])
                    if num_of_subscribers > 100000 and avg_rating > 4.5 and num_of_reviews > 10000:
                        comment += "Top Courses"
                    elif num_of_subscribers > 50000 and avg_rating > 4.0 and num_of_reviews > 5000:
                        comment += "Popular Courses"
                    elif num_of_subscribers > 10000 and avg_rating > 3.5 and num_of_reviews > 1000:
                        comment += "Good Courses"
                    else:
                        comment += "General Courses"

                    course_split_list = each.split(";;;")
                    course_obj = Course(course_split_list[0], int(course_split_list[1]), course_split_list[2],
                                        course_split_list[3], course_split_list[4], int(course_split_list[5]),
                                        course_split_list[6], course_split_list[7], int(course_split_list[8]),
                                        float(course_split_list[9]), int(course_split_list[10]))
                    is_course_found = True
                    return course_obj, comment

            if not is_course_found:
                comment += "Course not found!"
                return (comment)


    def get_course_by_instructor_id(self, instructor_id):
        course_id_list = []
        with open("./data/user.txt", "r+") as user_file:
            user_data = user_file.readlines()
            user_file.seek(0)
            for each in user_data:
                data_list = each.split(";;;")
                if data_list[4] == "instructor":
                    instructor_data = each.split(";;;")
                    instructor_text_id = int(instructor_data[0])
                    course_id_in_user = instructor_data[-1].strip("\n")
                    if instructor_id == instructor_text_id:
                        course_id_list = course_id_in_user.split("--")
                        print(len(course_id_list))
        with open("./data/course.txt", "r+") as course_file:
            course_data = course_file.readlines()
            course_list = []
            for item in course_id_list:
                for course_item in course_data:
                    course_id = course_item.split(";;;")[5]
                    if item == course_id:
                        course_list.append(course_item)

            if len(course_list) > 20:
                return (course_list[:20], len(course_list))
            else:
                return (course_list, len(course_list))









    def generate_course_figure1(self):
        pass

    def generate_course_figure2(self):
        pass

    def generate_course_figure3(self):
        pass

    def generate_course_figure4(self):
        pass

    def generate_course_figure5(self):
        pass

    def generate_course_figure6(self):
        pass

course = Course()
# course.clear_course_data()
# course.get_courses()
# course.generate_page_num_list(32,33)
# course.get_courses_by_page(10)
# course.delete_course_by_id(772137256)
# course.get_course_by_course_id(872028607)
course.get_course_by_instructor_id(612742716)