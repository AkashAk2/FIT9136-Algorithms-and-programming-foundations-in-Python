#Name: AKash Balakrishnan
#Student ID: 32192886
#Description: This class extracts the course data from the given source files.

import os
import json
import pandas as pd
from matplotlib import pyplot as plt

class Course:

    # Constructor
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

    # return string method
    def __str__(self):
        return self.category_title + ";;;" + str(self.subcategory_id) + ";;;" + str(self.subcategory_title) + ";;;" +\
               str(self.subcategory_description) + ";;;" + str(self.subcategory_url) + ";;;" + str(self.course_id) + \
               ";;;" + self.course_title + ";;;" + str(self.course_url) + ";;;" + str(self.num_of_subscribers) +\
               ";;;" + str(self.avg_rating) + ";;;" + str(self.num_of_reviews)

    #Extracting course data from source files
    def get_courses(self):
        #using try except to handle exceptions
        try:
            #creating list to store the source file paths
            files_list = list()
            for (dirpath, subdir, filenames) in os.walk("./data/source_course_files"):
                files_list += [os.path.join(dirpath, file) for file in filenames]
            #Iterating through each file in files_list
            for each in files_list:
                #if the file name ends with .json this block will execute
                if each.endswith(".json"):
                    # Openning source files and reading the file
                    with open(each, 'r', encoding="utf-8") as course_files:
                        with open("./data/course.txt", "a+", encoding="utf-8") as course_file:
                            item_data = json.load(course_files) # using json load to read the json files
                            self.category_title = item_data['unitinfo']['category']
                            subcategory = item_data['unitinfo']['source_objects']
                            item = item_data['unitinfo']['items']
                            subcategory_dict = {} # creating dictionary for the subcategory data
                            item_dict = {} # creating dictionary for item (course) data
                            for each_subcategory in subcategory:
                                subcategory_dict.update(each_subcategory)
                            # assigning the values of subcategory data
                            self.subcategory_id = subcategory_dict['id']
                            self.subcategory_title = subcategory_dict['title']
                            self.subcategory_description = subcategory_dict['description']
                            self.subcategory_url = subcategory_dict['url']

                            for each_item in item:
                                item_dict.update(each_item)
                                # assigning the values of course data
                                self.course_id = item_dict['id']
                                self.course_title = item_dict['title']
                                self.course_url = item_dict['url']
                                self.num_of_subscribers = item_dict['num_subscribers']
                                self.avg_rating = item_dict['avg_rating']
                                self.num_of_reviews =  item_dict['num_reviews']

                                # writing the extracted data to the course_file
                                course_file.write(self.__str__())
                                course_file.write("\n")
        except:
            return "Something went wrong while extracting course information!"


    # Deleting course _data
    def clear_course_data(self):
        try:
            #Opening the course.txt file
            with open("./data/course.txt", "w+", encoding="utf-8") as course_file:
                # removing all content
                course_file.seek(0)
                course_file.truncate()
                course_file.seek(0)
        except:
            return "Something went wrong couldn't clear course data"

    # Generating page number list using page and total page values
    def generate_page_num_list(self, page, total_pages):
        try:
            if page > 0 and total_pages > 0:
                #  If the current page is less than or equal to 5 the default page number list is defined below
                if page <= 5:
                    page_number_list = [1,2,3,4,5,6,7,8,9]
                    return page_number_list
                # If the current page number is greater than 5 and less than (total_pages - 4) below list will return
                if 5 < page < (total_pages - 4):
                    boundary = 4
                    page_number_list = []
                    for num in range(0,4):
                        temp = page - boundary
                        page_number_list.append(temp)
                        temp = page + boundary
                        page_number_list.append(temp)
                        boundary -= 1
                    page_number_list.sort()
                    return page_number_list
                # If the current page number is equal to or greater than (total_pages - 4) the following will execute
                elif page >= (total_pages - 4):
                    boundary = 8
                    page_number_list = []
                    for num in range(0, boundary):
                        temp = total_pages - boundary
                        page_number_list.append(temp)
                        boundary -= 1
                    page_number_list.sort()
                    return page_number_list
                else:
                    page_number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    return page_number_list

            # if the page number is not greater than 0 then this block returns [0]
            else:
                return ([0])

        except:
            return [0]


    # This method returns course objects by page
    def get_courses_by_page(self, page):
        try:
            # if the page is greater than 0 this block will execute
            if page > 0:
                # opening the course.txt file to read course data
                with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                    course_data = course_file.readlines()
                    num_of_courses = len(course_data)

                    # if number of courses is divided by 20 and the remainder is 0 this will execute
                    if num_of_courses % 20 == 0:
                        # Total pages can be calculated by dividing total courses by 20
                        total_pages = num_of_courses / 20
                    # if the total pages / 20 yields any remainder then this method will execute
                    else:
                        total_pages = (num_of_courses // 20) + 1

                    # current page is not equal to total page (Last page) this block will set the line_range = page * 20
                    if page != total_pages:
                        line_range = page * 20
                    # if the current page is equal to last page then line range will be set as follows
                    else:
                        line_range = page * 20 - (20 - num_of_courses % 20)
                    course_list = [] # creating empty list to store course objects
                    # Iterating through the course data by range (page)  and store the objects to course list
                    for each in range(line_range - 20, line_range):
                        course = course_data[each]
                        course_split_list = course.split(";;;")
                        course_obj = Course(course_split_list[0], int(course_split_list[1]), course_split_list[2],
                                    course_split_list[3], course_split_list[4], int(course_split_list[5]),
                                    course_split_list[6], course_split_list[7], int(course_split_list[8]),
                                    float(course_split_list[9]), int(course_split_list[10]))
                        course_list.append(course_obj)
                    # returns a tuple contains course_list, total_pages, and number of courses
                    return (course_list, total_pages, num_of_courses)
            else:
                print("Invalid page number")
        except:
            return(None,0,0)


    # This method will delete the course data by course id.
    def delete_course_by_id(self, course_id):
        try:
            is_deleted = False
            # reading the course.txt and deleting the course data by matching the id in text file with the provided id.
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
# reading instructor data to delete course id from the instructor data by matching id in text file with the provided id.
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_data = user_file.readlines()
                user_file.seek(0)
                for each in user_data:
                    data_list = each.split(";;;")
                    if data_list[4] == "instructor":
                        instructor_data = each.split(";;;")
                        course_id_in_user = instructor_data[-1] # temp course id variable to match
                        course_id_list = course_id_in_user.split("--")
                        for item in course_id_list: # iterating through course id list created above
                            if course_id == int(item):
                                id_line = user_data.index(each)
                                course_id_list.remove(item) # removing the matched course id
                                # storing the modified instructor data
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
                # rewriting the modified data
                for line in user_data:
                    user_file.write(line)
                user_file.truncate()

            # returning boolean value
            return is_deleted

        except:
            return "Something went wrong while deleting course by id!"

    # This method returns course object and a comment about the course
    def get_course_by_course_id(self, temp_course_id):
        try:
            is_course_found = False
            # reading the course.txt file
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                for each in course_data:
                    # creating empty string to store comments
                    comment = ""
                    course_id_in_text = int(each.split(";;;")[5])
                    if temp_course_id == course_id_in_text:
                        num_of_subscribers = int(each.split(";;;")[-3])
                        avg_rating = round(float(each.split(";;;")[-2]), 2)
                        num_of_reviews = int(each.split(";;;")[-1])
                        # Defining top courses
                        if num_of_subscribers > 100000 and avg_rating > 4.5 and num_of_reviews > 10000:
                            comment += "Top Courses"
                        # Defining Popular courses
                        elif num_of_subscribers > 50000 and avg_rating > 4.0 and num_of_reviews > 5000:
                            comment += "Popular Courses"
                        # Defining Good courses
                        elif num_of_subscribers > 10000 and avg_rating > 3.5 and num_of_reviews > 1000:
                            comment += "Good Courses"
                        # Defining General courses
                        else:
                            comment += "General Courses"
                        # creating course object
                        course_split_list = each.strip("\n").split(";;;")
                        course_obj = Course(course_split_list[0], int(course_split_list[1]), course_split_list[2],
                                        course_split_list[3], course_split_list[4], int(course_split_list[5]),
                                        course_split_list[6], course_split_list[7], int(course_split_list[8]),
                                        float(course_split_list[9]), int(course_split_list[10]))
                        is_course_found = True
                        # returning course object and comment as a tuple
                        return course_obj, comment

                if not is_course_found:
                    comment += "Course not found!"
                    return (comment)

        except:
            return "Something went wrong while getting course by course id!"


    def get_course_by_instructor_id(self, instructor_id):
        try:
            course_id_list = []
            # reading the user.txt file to get the course ids taught by this instructor
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_data = user_file.readlines()
                user_file.seek(0)
                for each in user_data:
                    data_list = each.split(";;;")
                    if data_list[4] == "instructor":
                        instructor_data = each.split(";;;")
                        instructor_text_id = int(instructor_data[0]) # assigning the text instructor id
                        course_id_in_user = instructor_data[-1].strip("\n")
                        if int(instructor_id) == instructor_text_id:
                            course_id_list = course_id_in_user.split("--") # adding the matched course id to the list

            # reading the course.txt file
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                course_list = []
                for item in course_id_list:
                    for course_item in course_data:
                        course_id = course_item.split(";;;")[5]
                        # matching the given id with the id in the course data and creating course objects
                        if int(item) == int(course_id):
                            course_split_list = course_item.strip("\n").split(";;;")
                            course_obj = Course(course_split_list[0], int(course_split_list[1]), course_split_list[2],
                                                course_split_list[3], course_split_list[4], int(course_split_list[5]),
                                                course_split_list[6], course_split_list[7], int(course_split_list[8]),
                                                float(course_split_list[9]), int(course_split_list[10]))
                            course_list.append(course_obj)
                # returning only 20 course objects and total courses if the instructor is teaching more than 20 courses
                if len(course_list) > 20:
                    print((course_list[:20], len(course_list)))
                    return (course_list[:20], len(course_list))
                # returning course objects and total courses teaching by the instructor
                else:
                    print((course_list, len(course_list)))
                    return (course_list, len(course_list))

        except:
            print("Exception")
            return "Something went wrong while getting course details by instructor id!"

    # Generating a graph to show the top 10 subcategories with most subscribers
    def generate_course_figure1(self):
        try:
            # reading course text file
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                subcategory_ids_list = [] # list to store subcategory ids
                subscribers_count_list = [] # list to store subscribers counts
                for each in course_data:
                    sub_id = int(each.split(";;;")[1])
                    subcategory_ids_list.append(sub_id) # appending the subcategory id to the list
                # creating dictionary to avoid duplicates
                subcategory_ids_list = list(dict.fromkeys(subcategory_ids_list))
                for item in subcategory_ids_list:
                    total_subscribers = 0
                    for each_id in course_data:
                        temp_sub_id = int(each_id.split(";;;")[1])
                        if item == temp_sub_id:
                            total_subscribers += int(each_id.split(";;;")[-3]) # getting the total subscribers value

                    subscribers_count_list.append(total_subscribers)
                # creating a dataframe to calculate the top 10 subcategories
                df = pd.DataFrame({"total_subscribers" : subscribers_count_list,
                                   "subcategory_id" : subcategory_ids_list})
                ten_courses = df.nlargest(10, "total_subscribers") # calculating the top 10 by nlargest
                subscribers_count_list = ten_courses["total_subscribers"] #assigning top 10 category's subscribers count
                subcategory_ids_list = ten_courses['subcategory_id'] # assigning subcategory id to the list
                temp_list = [] # temp list to store subcategory id added with first 3 letters of the name
                for sub_id in subcategory_ids_list:
                    for each in course_data:
                        temp_id = int(each.split(";;;")[1])
                        if int(sub_id) == temp_id:
                            id_name = str(sub_id) + "_" +((each.split(";;;")[2])[:3]) #adding first 3 letters to the id
                            temp_list.append(id_name)
                # creating another dataframe to plot the graph
                sub_name_list = list(dict.fromkeys(temp_list))
                df = pd.DataFrame({"total_subscribers": subscribers_count_list,
                                   "subcategory_id": sub_name_list})
                # plotting bar graph with figure size 15 x 15
                df.plot(kind="bar", figsize=(15, 15), x="subcategory_id", y="total_subscribers")
                plt.ylim(0, df["total_subscribers"].iloc[0] + 500000)
                plt.title("Bar chart for top 10 course subcategories with most subscribers.", fontweight="bold",
                          fontsize=22, y= 1.02)
                plt.xlabel("Subcategory_ID", fontweight="bold", fontsize=20)
                plt.ylabel("Total_Subscribers", fontweight="bold", fontsize=20)
                # Annotate values of the grid
                for i, data in enumerate(df['total_subscribers'].tolist()):
                    plt.text(i, data + 1, str(data), horizontalalignment="center")
                # saving the file to img/ folder as png
                plt.savefig("static/img/course_figure1.png", dpi=300, format="png")
                result = "The subcategory with id " + (sub_name_list[0])[:-4] + \
                         " has the most number of subscribers among others."
                # returning a string about the graph
                return result

        except:
            return "Something went wrong while generating course_figure1"

    # This method generates a graph to show the top 10 courses that have lowest avg rating and over 50000 reviews
    def generate_course_figure2(self):
        try:
            # reading the course file
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                course_name_list = [] # list to store course names
                avg_rating_list = [] # list to store avg_ratings
                for each in course_data:
                    temp_course_reviews = int(each.split(";;;")[-1])
                    if temp_course_reviews > 50000:
                        course_name = each.split(";;;")[6]
                        temp_name = course_name.split()[0] + "\n" + course_name.split()[1] + "\n" +\
                                    course_name.split()[2]
                        course_name_list.append(temp_name) # appending the course names to the list
                        avg_rating_list.append(float((each.split(";;;")[-2])[:5])) # appending avg_rating to the list

                # creating a dataframe to calculate top 10 courses that have lowest avg rating and over 50000 reviews
                df = pd.DataFrame({'course_name': course_name_list, 'avg_rating': avg_rating_list})
                ten_courses = df.nsmallest(10, 'avg_rating') # using nsmallest to calculate the lowest values
                # Creating a bar graph
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
                # returning a string about the graph
                return result

        except:
            return "Something went wrong while generating course figure 2"

    #Generating a graph to show all the courses avg rating distribution and number of subscribers.
    # The courses have subscribers between 100000 and 10000.
    def generate_course_figure3(self):
        try:
            # reading the course file
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                avg_rating_list = [] # list to store avg_ratings
                subscribers_list = [] # list to store subscribers counts
                for each in course_data:
                    temp_subscribers = int(each.split(";;;")[-3])
                    if 10000 < temp_subscribers < 100000:
                        subscribers_list.append(temp_subscribers) # appending the subscribers counts to the list
                        avg_rating_list.append(float((each.split(";;;")[-2])[:5])) # appending the avg_ratings to list
                # Creating a graph with size 15 x 15
                plt.figure(figsize= (15,15))
                # plotting a scatter graph
                plt.scatter(avg_rating_list, subscribers_list, s= 100)
                plt.xlabel("Average course ratings", fontweight = 'bold', fontsize = 20)
                plt.ylabel("Number of Subscribers", fontweight = 'bold', fontsize = 20)
                plt.title("Scatter chart to show all the course avg rating distribution and num of subscribers",
                          fontweight = "bold", fontsize = 22, y= 1.02)
                plt.savefig("static/img/course_figure3.png", dpi=300, format="png")

                # returning a string about the graph
                return "This scatter plot shows the negatively skewed distribution between course avg " \
                       "rating and number of subscribers"

        except:
            return "Something went wrong while generating course figure 3"


    #Generate a graph to show the number of courses for all categories and
    # sort in ascending order (pie chart, offsetting the second largest number of course with "explode")
    def generate_course_figure4(self):
        try:
            # reading the course file
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                category_title = [] # creating a list to store the category_title
                course_count = [] # creating a list to store the course_count
                for each in course_data:
                    category_title.append(each.split(";;;")[0]) # appending the category title to the list
                category_title = list(dict.fromkeys(category_title)) # creating dictionary to avoid duplicates
                for item in category_title:
                    temp_list = []
                    for each_item in course_data:
                        temp_title = each_item.split(";;;")[0]
                        if item == temp_title:
                            temp_list.append(each_item.split(";;;")[5]) # appending the course id to the temp_list
                    course_count.append(temp_list) # appending the course content to calculate the count
                for each_course in course_count:
                    temp = each_course
                    ind = course_count.index(each_course)
                    course_count[ind] = len(temp) # replacing the list with the length of course instead of course data
                # creating a dataframe to sort the values
                df = pd.DataFrame({'category_title': category_title, 'no_of_courses': course_count})
                sorted_df = df.sort_values(by= 'no_of_courses') # sorting
                explode_list = [] # explode list
                #creating explode list values
                for i in range(len(course_count)):
                    if i == 39:
                        explode_list.append(0.5)
                    else:
                        explode_list.append(0)
                explode_num = tuple(explode_list) # assigning the list to tuple
                # creating a figure
                plt.figure(figsize=(22,22))
                # plotting pie chart
                plt.pie(sorted_df['no_of_courses'], labels= sorted_df['category_title'], explode= explode_num,
                        shadow= True, autopct='%1.1f%%')
                plt.axis('equal')
                plt.title("Pie chart to show the number of courses for all categories,"
                          " the second largest number of course is exploded",
                          fontweight="bold", fontsize=22, y=1.02)
                plt.xlabel("Total categories are " + str(len(category_title)) + " and total courses are " +\
                       str(len(course_data)), fontweight="bold", fontsize=18)
                # saving the image to the folder img/
                plt.savefig("static/img/course_figure4.png", dpi=300, format="png")

                #returning a string about the graph
                return "Total categories are " + str(len(category_title)) + " and total courses are " +\
                       str(len(course_data)) + ". The category with second largest number of courses is " +\
                       str(sorted_df['category_title'].iloc[39]) + " which has " + \
                       str(sorted_df['no_of_courses'].iloc[39]) + " courses."

        except:
            return "Something went wrong while generating course figure 4."

    # Generating a graph to show how many courses have reviews and how many courses do not have reviews.(bar chart)
    def generate_course_figure5(self):
        try:
            # reading the course file
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                course_with_reviews = [] # list to store the course data with reviews
                for each in course_data:
                    if int(each.split(";;;")[-1]) != 0:
                        course_with_reviews.append(each) # appending the result to the list
                # creating a list contains count of course with reviews and course without reviews
                course_details = [len(course_with_reviews), len(course_data) - len(course_with_reviews)]
                titles = ["course_with_reviews", "course_without_reviews"] # title for plot
                fig = plt.figure(figsize= (15, 15))
                # plotting a bar graph
                plt.bar(titles, course_details)
                plt.xlabel("Courses", fontweight="bold", fontsize=20)
                plt.ylabel("Number of courses", fontweight="bold", fontsize=20)
                plt.title("Bar chart for courses with reviews and courses without reviews.", fontweight="bold",
                          fontsize=22, y=1.02)
                # Annotate the grid
                for i, data in enumerate(course_details):
                    plt.text(i, data + 100, str(data), horizontalalignment="center", fontsize = 12)
                plt.savefig("static/img/course_figure5.png", dpi=300, format="png")
                # returing a string about the graph
                return "Total number of courses are " + str(len(course_data)) + ". Courses with reviews are " +\
                       str(course_details[0]) + " and courses without reviews are " + str(course_details[1]) + "."
        except:
            return "Something went wrong while generating course figure 5. Please check for course data files."


    #Generating a graph to show the top 10 subcategories with the least courses
    def generate_course_figure6(self):
        try:
            # reading the course.txt file
            with open("./data/course.txt", "r+", encoding="utf-8") as course_file:
                course_data = course_file.readlines()
                subcategory_ids_list = [] # list to store the subcategory ids
                subscribers_count_list = [] # list to store subscribers counts
                for each in course_data:
                    sub_id = int(each.split(";;;")[1])
                    subcategory_ids_list.append(sub_id) # appending the subcategory id to the list
                # creating dictionary to avoid duplicates
                subcategory_ids_list = list(dict.fromkeys(subcategory_ids_list))
                for item in subcategory_ids_list:
                    total_subscribers = 0
                    for each_id in course_data:
                        temp_sub_id = int(each_id.split(";;;")[1])
                        if item == temp_sub_id:
                            total_subscribers += int(each_id.split(";;;")[-3])  # getting the total subscribers value

                    subscribers_count_list.append(total_subscribers) # appending the total subscribers to the list
                # creating a dataframe to calculate the top 10 subcategories with the least courses
                df = pd.DataFrame({"total_subscribers": subscribers_count_list,
                                   "subcategory_id": subcategory_ids_list})
                # calculating the top 10 by nsmallest
                ten_courses = df.nsmallest(10, "total_subscribers")
                subscribers_count_list = ten_courses["total_subscribers"] #assigning top 10 category's subscribers count
                subcategory_ids_list = ten_courses['subcategory_id'] # assigning subcategory id to the list
                temp_list = [] # temp list to store subcategory id added with first 3 letters of the name
                for sub_id in subcategory_ids_list:
                    for each in course_data:
                        temp_id = int(each.split(";;;")[1])
                        if int(sub_id) == temp_id:
                            id_name = str(sub_id) + "_" + ((each.split(";;;")[2])[:3]) #adding first 3 letters to the id
                            temp_list.append(id_name)

                # creating another dataframe to plot the graph
                sub_name_list = list(dict.fromkeys(temp_list))
                df = pd.DataFrame({"total_subscribers": subscribers_count_list,
                                   "subcategory_id": sub_name_list})
                # plotting bar graph with figure size 15 x 15
                df.plot(kind="bar", figsize=(15, 15), x="subcategory_id", y="total_subscribers")
                plt.ylim(0, df["total_subscribers"].iloc[0] + 100)
                plt.title("Bar chart for top 10 course subcategories with least subscribers.", fontweight="bold",
                          fontsize=22, y=1.02)
                plt.xlabel("Subcategory_ID", fontweight="bold", fontsize=20)
                plt.ylabel("Total_Subscribers", fontweight="bold", fontsize=20)
                # Annotate values of the grid
                for i, data in enumerate(df['total_subscribers'].tolist()):
                    plt.text(i, data + 1, str(data), horizontalalignment="center")
                # saving the file to img/ folder as png
                plt.savefig("static/img/course_figure6.png", dpi=300, format="png")
                result = "The subcategory with id " + (sub_name_list[0])[:-4] + \
                         " has the least number of subscribers among others."
                # returning a string about the graph
                return result

        except:
            return "Something went wrong while generating course_figure6"
