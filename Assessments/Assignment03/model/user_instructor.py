#Name: AKash Balakrishnan
#Student ID: 32192886
#Description: This class extracts the instructor data and plots graph

from model.user import User
import os
import json
import pandas as pd
from matplotlib import pyplot as plt

# child class to User
class Instructor(User):
    # constructor
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS",
                 role="instructor", email="", display_name="", job_title="", course_id_list=[]):
        super().__init__(uid, username, password, register_time)
        self.role = role
        self.email = email
        self.display_name = display_name
        self.job_title = job_title
        self.course_id_list = course_id_list

    # return string method
    def __str__(self):
        return super().__str__() + self.role + ";;;" + self.email + ";;;" + self.display_name + ";;;" + self.job_title + ";;;" + \
               str(self.course_id_list)

    # This method reads the source files to extract the instructor information
    def get_instructors(self):
        try:
            #creating list to store the source file paths
            files_list = list()
            instructor_data = []
            for (dirpath, subdir, filenames) in os.walk("./data/source_course_files"):
                files_list += [os.path.join(dirpath, file) for file in filenames]
            # Iterating through each file in files_list
            for each in files_list:
                # if the file name ends with .json this block will execute
                if each.endswith(".json"):
                    # Openning source files and reading the file
                    with open(each, 'r', encoding="utf-8") as course_files:
                        # using json load to read the json files
                            item_data = json.load(course_files)
                            item = item_data['unitinfo']['items']
                            item_dict = {} # creating dictionary for item (course) data
                            for each_item in item:
                                item_dict.update(each_item)
                                course_id = str(item_dict['id'])
                                visible_inst_dict = {} # creating dictionary for visible instructors
                                visible_instructor_data = item_dict['visible_instructors']
                                # iterating through each instructor data and extracting the information
                                for each_instructor in visible_instructor_data:
                                    visible_inst_dict.update(each_instructor)
                                    instructor_id = visible_inst_dict['id']
                                    display_name = visible_inst_dict['display_name']
                                    username = str(display_name).lower().replace(" ", "_")
                                    password = User.encrypt_password(self, str(instructor_id))
                                    email = username + "@gmail.com"
                                    job_title = visible_inst_dict['job_title']
                                    write_format = str(instructor_id) + ";;;" + username + ";;;" + password + ";;;" + \
                                               self.register_time + ";;;" + self.role + ";;;" + email + ";;;" + \
                                               display_name + ";;;" + str(job_title) + ";;;" + course_id
                                    instructor_data_list = [] # creating list to store the instructor id
                                    for inst_item in instructor_data:
                                        instructor_temp_id = inst_item.split(";;;")[0]
                                        instructor_data_list.append(instructor_temp_id) # appending the id to the list

                                    # if the id is in the instructor data list to append the course id
                                    if str(instructor_id) in instructor_data_list:
                                        get_instructor_line = instructor_data_list.index(str(instructor_id)) # line
                                        single_instructor = instructor_data[get_instructor_line].strip("\n")
                                        single_instructor += "--" + course_id # adding course id to the end
                                        instructor_data[get_instructor_line] = single_instructor # adding modified data

                                    # if not found append to the list
                                    else:
                                        instructor_data.append(write_format)
            # opening user.txt to write
            with open("./data/user.txt", "w+", encoding="utf-8") as user_file_write:
                for line in instructor_data:
                    user_file_write.write(line) # writing each item from the list
                    user_file_write.write("\n")
        except:
            return "Something went wrong while reading instructors data!"


    #This method reads the user.txt file to retrieve all the instructor information as a tuple.
    def get_instructors_by_page(self, page):
        try:
            # if page is greater than 0
            if page > 0:
                # reading the user text file
                with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                    user_data = user_file.readlines()
                    instructor_data = []

                    # splitting the instructors from the file
                    for item in user_data:
                        split_list = item.split(";;;")
                        if split_list[4] == "instructor":
                            instructor_data.append(item)
                    # calculating number of instructors, total_pages and line_range(index range)
                    total_instructors = len(instructor_data)
                    if total_instructors % 20 == 0:
                        total_pages = total_instructors // 20
                    else:
                        total_pages = (total_instructors // 20) + 1
                    if page != total_pages:
                        line_range = page * 20
                    else:
                        line_range = page * 20 - (20 - total_instructors % 20)
                    # empty list to store the instructor objects
                    instructor_list = []
                    if total_instructors > 0:
                        # iterating the list to get instructors as per the page
                        for each in range(line_range - 20, line_range):
                            instructor = instructor_data[each]
                            instructor_split_list = instructor.split(";;;")
                            # creating instructor objects
                            instructor_obj = Instructor(int(instructor_split_list[0]), instructor_split_list[1],
                                            instructor_split_list[2], instructor_split_list[3],
                                            instructor_split_list[4], instructor_split_list[5],
                                            instructor_split_list[6], instructor_split_list[7],
                                            [instructor_split_list[8]])
                            instructor_list.append(instructor_obj) # appending the objected to the list
                        result = (instructor_list, total_pages, total_instructors)
                    else:
                        result = (instructor_list, total_pages, total_instructors)

                    # returning a tuple contains (instructor_list, total_pages, total_instructors)
                    return result
            else:
                print("Invalid page number!")

        except:
            return "No Instructor records found!"

    # Generating a graph that shows the top 10 instructors who teach the most courses.
    def generate_instructor_figure1(self):
        try:
            # reading the file
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_data = user_file.readlines()
                instructor_data = [] # list to store the instructor data from user text file
                instructor_name = [] # list to store the instructor name
                instructor_course_ids = [] # list to store the instructor teaching course count
                for item in user_data:
                    split_list = item.split(";;;")
                    if split_list[4] == "instructor":
                        instructor_data.append(item) # appending the instructor
                for each in instructor_data:
                    instructor_name.append(each.split(";;;")[6])
                    course_id_temp = (each.split(";;;")[-1]).split("--")
                    instructor_course_ids.append(len(course_id_temp)) # appending number of courses to the list

                # creating a data frame to find top 10 instructors
                df = pd.DataFrame({'Instructor_Name' : instructor_name, 'Number_of_Courses' : instructor_course_ids})
                # using nlargest to find top 10
                ten_instructors = df.nlargest(10, 'Number_of_Courses')
                # plotting a bar graph
                ten_instructors.plot(kind= "bar", figsize = (15, 15), x = "Instructor_Name", y = "Number_of_Courses")
                plt.ylim(0, ten_instructors["Number_of_Courses"].iloc[0]+5)
                plt.title("Bar chart for top 10 instructors teaching most courses.", fontweight = "bold", fontsize=22)
                plt.xlabel("Instructor Names", fontweight = "bold", fontsize=20)
                plt.ylabel("Number of Courses", fontweight = "bold", fontsize=20)
                # Annotate values of the grid
                for i, data in enumerate(ten_instructors['Number_of_Courses'].tolist()):
                    plt.text(i, data + 0.5, str(data), horizontalalignment = "center")
                plt.savefig("static/img/instructor_figure1.png", dpi = 300, format = "png")
                top_instructor = instructor_data[ten_instructors.iloc[0].name]
                top_instructor_courses = len((top_instructor.split(";;;")[-1]).split("--"))
                result = "The instructor named " + top_instructor.split(";;;")[6] +\
                         " teaches the most number of courses which is " + str(top_instructor_courses) + "."
                # returning string about the graph.
                return result

        except:
            return "Something went wrong while generating instructor figure!"

