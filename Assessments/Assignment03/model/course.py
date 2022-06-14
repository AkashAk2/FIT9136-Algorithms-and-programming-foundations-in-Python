import os
import json
import pandas as pd
from matplotlib import pyplot as plt

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
        try:
            files_list = list()
            for (dirpath, subdir, filenames) in os.walk("./data/source_course_files"):
                files_list += [os.path.join(dirpath, file) for file in filenames]
            for each in files_list:
                if each.endswith(".json"):
                    with open(each, 'r', encoding="utf-8") as course_files:
                        with open("./data/course.txt", "a+", encoding="utf-8") as course_file:
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
        except:
            return "Something went wrong while extracting course information!"



    def clear_course_data(self):
        try:
            with open("./data/course.txt", "w+", encoding="utf-8") as course_file:
                course_file.seek(0)
                course_file.truncate()
        except:
            return "Something went wrong couldn't clear course data"

    def generate_page_num_list(self, page, total_pages):
        try:
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

        except:
            return "Something went wrong while generating page numbers!"




    def get_courses_by_page(self, page):
        try:
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
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
        except:
            return "Something went wrong while getting course details by page!"



    def delete_course_by_id(self, course_id):
        try:
            is_deleted = False
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                course_file.seek(0)
                for each in course_data:
                    course_id_in_text = int(each.split(";;;")[5])
                    if course_id_in_text != course_id:
                        course_file.write(each)
                    elif course_id_in_text == course_id:
                        is_deleted = True
                course_file.truncate()
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
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

        except:
            return "Something went wrong while deleting course by id!"


    def get_course_by_course_id(self, temp_course_id):
        try:
            is_course_found = False
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
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

        except:
            return "Something went wrong while getting course by course id!"


    def get_course_by_instructor_id(self, instructor_id):
        try:
            course_id_list = []
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
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
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
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

        except:
            return "Something went wrong while getting course details by instructor id!"


    def generate_course_figure1(self):
        try:
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                subcategory_ids_list = []
                subscribers_count_list = []
                for each in course_data:
                    sub_id = int(each.split(";;;")[1])
                    subcategory_ids_list.append(sub_id)
                subcategory_ids_list = list(dict.fromkeys(subcategory_ids_list))
                for item in subcategory_ids_list:
                    total_subscribers = 0
                    for each_id in course_data:
                        temp_sub_id = int(each_id.split(";;;")[1])
                        if item == temp_sub_id:
                            total_subscribers += int(each_id.split(";;;")[-3])

                    subscribers_count_list.append(total_subscribers)
                df = pd.DataFrame({"total_subscribers" : subscribers_count_list,
                                   "subcategory_id" : subcategory_ids_list})
                ten_courses = df.nlargest(10, "total_subscribers")
                subscribers_count_list = ten_courses["total_subscribers"]
                subcategory_ids_list = ten_courses['subcategory_id']
                temp_list = []
                for sub_id in subcategory_ids_list:
                    for each in course_data:
                        temp_id = int(each.split(";;;")[1])
                        if int(sub_id) == temp_id:
                            id_name = str(sub_id) + "_" +((each.split(";;;")[2])[:3])
                            temp_list.append(id_name)

                sub_name_list = list(dict.fromkeys(temp_list))
                df = pd.DataFrame({"total_subscribers": subscribers_count_list,
                                   "subcategory_id": sub_name_list})
                df.plot(kind="bar", figsize=(15, 15), x="subcategory_id", y="total_subscribers")
                plt.ylim(0, df["total_subscribers"].iloc[0] + 500000)
                plt.title("Bar chart for top 10 course subcategories with most subscribers.", fontweight="bold",
                          fontsize=22, y= 1.02)
                plt.xlabel("Subcategory_ID", fontweight="bold", fontsize=20)
                plt.ylabel("Total_Subscribers", fontweight="bold", fontsize=20)
                # Annotate values of the grid
                for i, data in enumerate(df['total_subscribers'].tolist()):
                    plt.text(i, data + 1, str(data), horizontalalignment="center")
                plt.savefig("static/img/course_figure1.png", dpi=300, format="png")
                result = "The subcategory with id " + (sub_name_list[0])[:-4] + \
                         " has the most number of subscribers among others."
                return result

        except:
            return "Something went wrong while generating course_figure1"


    def generate_course_figure2(self):
        try:
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                course_name_list = []
                avg_rating_list = []
                for each in course_data:
                    temp_course_reviews = int(each.split(";;;")[-1])
                    if temp_course_reviews > 50000:
                        course_name = each.split(";;;")[6]
                        temp_name = course_name.split()[0] + "\n" + course_name.split()[1] + "\n" +\
                                    course_name.split()[2]
                        course_name_list.append(temp_name)
                        avg_rating_list.append(float((each.split(";;;")[-2])[:5]))

                df = pd.DataFrame({'course_name': course_name_list, 'avg_rating': avg_rating_list})
                ten_courses = df.nsmallest(10, 'avg_rating')
                ten_courses.plot(kind="bar", figsize=(15, 15), x="course_name", y="avg_rating")
                plt.ylim(0, ten_courses["avg_rating"].iloc[0] + 5)
                plt.title("Bar chart for top 10 courses with lowest avg review.", fontweight = "bold", fontsize=22,
                          y= 1.02)
                plt.xlabel("Course Names", fontweight="bold", fontsize=20)
                plt.ylabel("Average Rating", fontweight="bold", fontsize=20)
                # Annotate values of the grid
                for i, data in enumerate(ten_courses['avg_rating'].tolist()):
                    plt.text(i, data + 0.1, str(data), horizontalalignment="center")
                plt.savefig("static/img/course_figure2.png", dpi=300, format="png")
                bottom_course = (ten_courses['course_name'].iloc[0]).replace("\n", " ")
                result = "The course named " + bottom_course + \
                         " has the lowest review among others which is " + str(ten_courses['avg_rating'].iloc[0]) + "."
                return result

        except:
            return "Something went wrong while generating course figure 2"


    def generate_course_figure3(self):
        try:
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                avg_rating_list = []
                subscribers_list = []
                for each in course_data:
                    temp_subscribers = int(each.split(";;;")[-3])
                    if 10000 < temp_subscribers < 100000:
                        subscribers_list.append(temp_subscribers)
                        avg_rating_list.append(float((each.split(";;;")[-2])[:5]))

                plt.figure(figsize= (15,15))
                plt.scatter(avg_rating_list, subscribers_list, s= 100)
                plt.xlabel("Average course ratings", fontweight = 'bold', fontsize = 20)
                plt.ylabel("Number of Subscribers", fontweight = 'bold', fontsize = 20)
                plt.title("Scatter chart to show all the course avg rating distribution and num of subscribers",
                          fontweight = "bold", fontsize = 22, y= 1.02)
                plt.savefig("static/img/course_figure3.png", dpi=300, format="png")
                return "This scatter plot shows the negatively skewed distribution between course avg " \
                       "rating and number of subscribers"

        except:
            return "Something went wrong while generating course figure 3"



    def generate_course_figure4(self):
        try:
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                category_title = []
                course_count = []
                for each in course_data:
                    category_title.append(each.split(";;;")[0])
                category_title = list(dict.fromkeys(category_title))
                for item in category_title:
                    temp_list = []
                    for each_item in course_data:
                        temp_title = each_item.split(";;;")[0]
                        if item == temp_title:
                            temp_list.append(each_item.split(";;;")[5])
                    course_count.append(temp_list)
                for each_course in course_count:
                    temp = each_course
                    ind = course_count.index(each_course)
                    course_count[ind] = len(temp)
                df = pd.DataFrame({'category_title': category_title, 'no_of_courses': course_count})
                sorted_df = df.sort_values(by= 'no_of_courses')
                explode_list = []
                for i in range(len(course_count)):
                    if i == 39:
                        explode_list.append(0.5)
                    else:
                        explode_list.append(0)
                explode_num = tuple(explode_list)
                plt.figure(figsize=(22,22))
                plt.pie(sorted_df['no_of_courses'], labels= sorted_df['category_title'], explode= explode_num,
                        shadow= True, autopct='%1.1f%%')
                plt.axis('equal')
                plt.title("Pie chart to show the number of courses for all categories,"
                          " the second largest number of course is exploded",
                          fontweight="bold", fontsize=22, y=1.02)
                plt.xlabel("Total categories are " + str(len(category_title)) + " and total courses are " +\
                       str(len(course_data)), fontweight="bold", fontsize=18)
                plt.savefig("static/img/course_figure4.png", dpi=300, format="png")

                return "Total categories are " + str(len(category_title)) + " and total courses are " +\
                       str(len(course_data)) + ". The category with second largest number of courses is " +\
                       str(sorted_df['category_title'].iloc[39]) + " which has " + \
                       str(sorted_df['no_of_courses'].iloc[39]) + " courses."

        except:
            return "Something went wrong while generating course figure 4."


    def generate_course_figure5(self):
        try:
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                course_with_reviews = []
                for each in course_data:
                    if int(each.split(";;;")[-1]) != 0:
                        course_with_reviews.append(each)
                course_details = [len(course_with_reviews), len(course_data) - len(course_with_reviews)]
                print(course_details)
                titles = ["course_with_reviews", "course_without_reviews"]
                fig = plt.figure(figsize= (15, 15))
                plt.bar(titles, course_details)
                plt.xlabel("Courses", fontweight="bold", fontsize=20)
                plt.ylabel("Number of courses", fontweight="bold", fontsize=20)
                plt.title("Bar chart for courses with reviews and courses without reviews.", fontweight="bold",
                          fontsize=22, y=1.02)
                for i, data in enumerate(course_details):
                    plt.text(i, data + 100, str(data), horizontalalignment="center", fontsize = 12)
                plt.savefig("static/img/course_figure5.png", dpi=300, format="png")
                return "Total number of courses are " + str(len(course_data)) + ". Courses with reviews are " +\
                       str(course_details[0]) + " and courses without reviews are " + str(course_details[1]) + "."
        except:
            return "Something went wrong while generating course figure 5. Please check for course data files."

    def generate_course_figure6(self):
        try:
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                subcategory_ids_list = []
                subscribers_count_list = []
                for each in course_data:
                    sub_id = int(each.split(";;;")[1])
                    subcategory_ids_list.append(sub_id)
                subcategory_ids_list = list(dict.fromkeys(subcategory_ids_list))
                for item in subcategory_ids_list:
                    total_subscribers = 0
                    for each_id in course_data:
                        temp_sub_id = int(each_id.split(";;;")[1])
                        if item == temp_sub_id:
                            total_subscribers += int(each_id.split(";;;")[-3])

                    subscribers_count_list.append(total_subscribers)
                df = pd.DataFrame({"total_subscribers": subscribers_count_list,
                                   "subcategory_id": subcategory_ids_list})
                ten_courses = df.nsmallest(10, "total_subscribers")
                print(ten_courses)
                subscribers_count_list = ten_courses["total_subscribers"]
                subcategory_ids_list = ten_courses['subcategory_id']
                temp_list = []
                for sub_id in subcategory_ids_list:
                    for each in course_data:
                        temp_id = int(each.split(";;;")[1])
                        if int(sub_id) == temp_id:
                            id_name = str(sub_id) + "_" + ((each.split(";;;")[2])[:3])
                            temp_list.append(id_name)

                sub_name_list = list(dict.fromkeys(temp_list))
                df = pd.DataFrame({"total_subscribers": subscribers_count_list,
                                   "subcategory_id": sub_name_list})
                df.plot(kind="bar", figsize=(15, 15), x="subcategory_id", y="total_subscribers")
                plt.ylim(0, df["total_subscribers"].iloc[0] + 100)
                plt.title("Bar chart for top 10 course subcategories with least subscribers.", fontweight="bold",
                          fontsize=22, y=1.02)
                plt.xlabel("Subcategory_ID", fontweight="bold", fontsize=20)
                plt.ylabel("Total_Subscribers", fontweight="bold", fontsize=20)
                # Annotate values of the grid
                for i, data in enumerate(df['total_subscribers'].tolist()):
                    plt.text(i, data + 1, str(data), horizontalalignment="center")
                plt.savefig("static/img/course_figure6.png", dpi=300, format="png")
                result = "The subcategory with id " + (sub_name_list[0])[:-4] + \
                         " has the least number of subscribers among others."
                return result

        except:
            return "Something went wrong while generating course_figure6"

course = Course()
# course.clear_course_data()
# course.get_courses()
# course.generate_page_num_list(32,33)
# course.get_courses_by_page(10)
# course.delete_course_by_id(772137256)
# course.get_course_by_course_id(872028607)
# course.get_course_by_instructor_id(612742716)
# course.generate_course_figure6()