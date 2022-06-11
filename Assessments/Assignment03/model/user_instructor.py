from user import User
import os
import json
import pandas as pd
from matplotlib import pyplot as plt


class Instructor:
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS",
                 role="instructor", email="", display_name="", job_title="", course_id_list=[]):
        self.uid = uid
        self.username = username
        self.password = password
        self.register_time = register_time
        self.role = role
        self.email = email
        self.display_name = display_name
        self.job_title = job_title
        self.course_id_list = course_id_list

    def __str__(self):
        return str(self.uid) + ";;;" + self.username + ";;;" + self.password + ";;;" + self.register_time + ";;;" + \
               self.role + ";;;" + self.email + ";;;" + self.display_name + ";;;" + self.job_title + ";;;" + \
               str(self.course_id_list)

    def get_instructors(self):
        try:
            files_list = list()
            instructor_data = []
            for (dirpath, subdir, filenames) in os.walk("./data/source_course_files"):
                files_list += [os.path.join(dirpath, file) for file in filenames]
            for each in files_list:
                if each.endswith(".json"):
                    with open(each, 'r', encoding="utf-8") as course_files:

                            item_data = json.load(course_files)
                            item = item_data['unitinfo']['items']
                            item_dict = {}
                            for each_item in item:
                                item_dict.update(each_item)
                                course_id = str(item_dict['id'])
                                visible_inst_dict = {}
                                visible_instructor_data = item_dict['visible_instructors']
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
                                    instructor_data_list = []
                                    for inst_item in instructor_data:
                                        instructor_temp_id = inst_item.split(";;;")[0]
                                        instructor_data_list.append(instructor_temp_id)

                                    if str(instructor_id) in instructor_data_list:
                                        get_instructor_line = instructor_data_list.index(str(instructor_id))
                                        single_instructor = instructor_data[get_instructor_line].strip("\n")
                                        single_instructor += "--" + course_id
                                        instructor_data[get_instructor_line] = single_instructor

                                    else:
                                        instructor_data.append(write_format)

            with open("./data/user.txt", "w+", encoding="utf-8") as user_file_write:
                for line in instructor_data:
                    user_file_write.write(line)
                    user_file_write.write("\n")
        except:
            print("Something went wrong while reading instructors data!")





    def get_instructors_by_page(self, page):
        try:
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_data = user_file.readlines()
                instructor_data = []

                for item in user_data:
                    split_list = item.split(";;;")
                    if split_list[4] == "instructor":
                        instructor_data.append(item)

                total_instructors = len(instructor_data)
                total_pages = round(total_instructors / 20)
                line_range = page * 20
                instructor_list = []
                for each in range(line_range - 20, line_range):
                    instructor = instructor_data[each]
                    instructor_split_list = instructor.split(";;;")
                    instructor_obj = Instructor(int(instructor_split_list[0]), instructor_split_list[1],
                                            instructor_split_list[2], instructor_split_list[3],
                                            instructor_split_list[4], instructor_split_list[5],
                                            instructor_split_list[6], instructor_split_list[7],
                                            [instructor_split_list[8]])
                    instructor_list.append(instructor_obj)
                result = (instructor_list, total_pages, total_instructors)
                print(result)
                print(total_instructors)
                print(total_pages)
                return result
        except:
            print("No Instructor records found!")

    def generate_instructor_figure1(self):
        try:
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_data = user_file.readlines()
                instructor_data = []
                instructor_name = []
                instructor_course_ids = []
                for item in user_data:
                    split_list = item.split(";;;")
                    if split_list[4] == "instructor":
                        instructor_data.append(item)
                for each in instructor_data:
                    instructor_name.append(each.split(";;;")[6])
                    course_id_temp = (each.split(";;;")[-1]).split("--")
                    instructor_course_ids.append(len(course_id_temp))

                df = pd.DataFrame({'Instructor_Name' : instructor_name, 'Number_of_Courses' : instructor_course_ids})
                ten_instructors = df.nlargest(10, 'Number_of_Courses')
                ten_instructors.plot(kind= "bar", figsize = (15, 15), x = "Instructor_Name", y = "Number_of_Courses")
                plt.ylim(0, ten_instructors["Number_of_Courses"].iloc[0]+5)
                plt.xlabel("Instructor Names", fontweight = "bold", fontsize=20)
                plt.ylabel("Number of Courses", fontweight = "bold", fontsize=20)
                # Annotate values of the grid
                for i, data in enumerate(ten_instructors['Number_of_Courses'].tolist()):
                    plt.text(i, data + 0.5, str(data), horizontalalignment = "center")
                plt.savefig("static/img/instructor_figure1.png", dpi = 300, format = "png")

        except:
            print("Something went wrong while generating instructor figure!")




instructor = Instructor()
# instructor.get_instructors()
# instructor.get_instructors_by_page(1)
instructor.generate_instructor_figure1()
