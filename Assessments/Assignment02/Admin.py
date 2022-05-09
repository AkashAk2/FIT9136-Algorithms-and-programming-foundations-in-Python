import re
import os
from User import User



class Admin(User):
    
    def __init__(self, user_id = -1, username = "", password = ""):
        super().__init__(user_id, username, password)

    def register_admin(self):
        print('register admin function is openned')
        registered = False
        file_handle_admin = open('./data/course_data/user_admin.txt', 'r+')
        encrypted_pass = User.encryption(self,self.password)
        for line in file_handle_admin:
            print("file handle for is open", line)
            line_list = [line.split(';;;')]
            print("line_list", line_list)
            for each in line_list:
                print("In for loop of line_list")
                print("each", each)
                print(each[1])
                print(each[2])
                if self.username == each[1] and encrypted_pass == each[2]:
                    print("User is already registered as admin!")
                    registered = True
                    break

        if registered == False:
            write_admin = open("./data/course_data/user_admin.txt", "a+")
            temp_userid = User.generate_unique_user_id(self)
            str_user_id = str(temp_userid)
            write_admin.write("\n")
            write_admin.write(str_user_id)
            write_admin.write(";;;" + self.username + ";;;" + encrypted_pass)
            write_admin.close()

        file_handle_admin.close()

    def extract_course_info(self):

        with open("./data/course_data/raw_data.txt") as file_handle:
            data = file_handle.readlines()
            for each in data:
                pattern = r'\_class\":\"course\"\,\"id\":([0-9]*).*?\"title\":\"(.*?)\"' \
                          r'.*?\"headline\":\"(.*?)\".*?\"num_subscribers.*?\":(.*?)\,\"caption_locales' \
                          r'.*?\"avg_rating\":(.*?)\,\"avg_rating_recent' \
                          r'.*?\"image_100x100\":\"(.*?)\"' \
                          r'.*?\"content_info\":\"([0-9.]*)'
                extracted_data = re.findall(pattern, each)

                with open("./data/result/course.txt", "a+") as course_file:
                    # course_file = open("./data/result/course.txt", "a+")
                    for line in extracted_data:
                        num = 0
                        data_list = list(line)
                        list_order = [0,1,5,2,3,4,6]
                        ordered_list = [data_list[i] for i in list_order]
                        for item in ordered_list:
                            course_file.write(item)
                            if num < len(item):
                                course_file.write(";;;")
                                num += 1
                        course_file.write("\n")
                # course_file.close()



    def extract_review_info(self):
        folder_path = './data/review_data'
        for file in os.listdir(folder_path):
            if file.endswith('.json'):
                file_path = os.path.join(folder_path, file)
                course_id = os.path.basename(file).split('.')[0]
                # print(file_name)
                with open(file_path,'r') as f:
                    data = f.readlines()
                    for each in data:
                        pattern = r'\"_class\": \"course_review\", \"id\":.([0-9]*)\, \"content\":\ \"(.*?)\",' \
                                r'.*? \"rating\": (.*?)\,'
                        extracted_data = re.findall(pattern, each)

                        with open('./data/result/review.txt','a+') as review_file:
                            for line in extracted_data:
                                num = 0
                                data_list = list(line)
                                for item in data_list:
                                    review_file.write(item)
                                    if num < len(data_list):
                                        review_file.write(";;;")
                                        num += 1
                                review_file.write(course_id)
                                review_file.write("\n")


    def extract_students_info(self):
        id_existing = False
        folder_path = './data/review_data'
        for file in os.listdir(folder_path):
            if file.endswith('.json'):
                file_path = os.path.join(folder_path, file)
                course_id = os.path.basename(file).split('.')[0]
                with open(file_path, 'r') as f:
                    data = f.readlines()
                    for each in data:
                        all_pattern = r'\"_class\": \"course_review\", \"id\": (.*?)\,' \
                                      r'.*?\"_class\": \"user\",(.*?) \"title\": \"(.*?)\",' \
                                      r'.*?\"image_50x50\": \"(.*?)\",.*?\"initials\": \"(.*?)\"'
                        extracted_data = re.findall(all_pattern, each)

                        with open('./data/result/user_student.txt','a+') as student_file:
                            for line in extracted_data:
                                num = 1
                                data_list = list(line)
                                list_order = [1, 2, 3, 4, 0]
                                ordered_list = [data_list[i] for i in list_order]
                                user_name_extracted = str(ordered_list[1])
                                stud_user_name = user_name_extracted.lower().replace(" ", "_")
                                extracted_user_id = str(ordered_list[0])
                                stud_id = ""
                                for digit in extracted_user_id:
                                    if digit.isdigit() == True:
                                        stud_id += str(digit)
                                if len(stud_id) == 0:
                                    stud_id += str(User.generate_unique_user_id(self))
                                extracted_user_title = str(ordered_list[3]).lower()
                                stud_password = extracted_user_title + extracted_user_id + extracted_user_title
                                encrypted_pass = User.encryption(self,stud_password)
                                user_name_password = [stud_user_name, encrypted_pass]
                                ordered_list[0] = stud_id
                                final_list = [ordered_list[0], user_name_password[0], user_name_password[1],
                                              ordered_list[1], ordered_list[2], ordered_list[3], ordered_list[4]]
                                # print(len(final_list))

                                for item in final_list:
                                    student_file.write(item)
                                    if num < len(final_list):
                                        student_file.write(";;;")
                                        num += 1
                                student_file.write("\n")

    def extract_instructor_info(self):
        with open("./data/course_data/raw_data.txt") as file_handle:
            data = file_handle.readlines()
            i = 1
            for line in data:
                pattern = r'\"_class\":\"course\",\"id\":(.*?)\,.*?\"visible_instructors\":\[(.*?)\]'
                extracted_data = re.findall(pattern, line)

                for item in extracted_data:
                    course_id = item[0]
                    instructors_data = item[1]
                    instructors_pattern = r'{(.*?)}'
                    instructors_info = re.findall(instructors_pattern, instructors_data)
                    # print(instructors_info)

                    for instructor in instructors_info:
                        instructor = '{' + instructor + '}'
                        instructor = instructor.replace('":', '": ')
                        instructor = eval(instructor)
                        # print(course_id, instructor['id'], instructor['display_name'])
                        instructor_id = str(instructor['id'])
                        # print(instructor_id)
                        display_name = instructor['display_name']
                        job_title = instructor['job_title']
                        image = instructor['image_100x100']
                        username = display_name.replace(" ", "_").lower()
                        password = User.encryption(self,str(instructor_id))
                        result = instructor_id + ";;;" + username + ";;;" + password + ";;;" + display_name + ";;;" +\
                            job_title + ";;;" + image + ";;;" + course_id
                        # print(result[0])

                        with open("./data/result/user_instructor.txt", "a+") as instructor_append:
                            is_already_existing = False
                            with open("./data/result/user_instructor.txt", "r+") as instructor_read:
                                instructor_read_data = instructor_read.readlines()
                                instructor_data_list = []
                                for each in instructor_read_data:
                                    instructor_temp_id = each.split(";;;")[0]
                                    instructor_data_list.append(instructor_temp_id)

                                if instructor_id in instructor_data_list:
                                    is_already_existing = True
                                    get_instructor_line = instructor_data_list.index(instructor_id)
                                    single_instructor = instructor_read_data[get_instructor_line].strip("\n")
                                    single_instructor += "--" + course_id + "\n"
                                    instructor_read_data[get_instructor_line] = single_instructor
                                    with open("./data/result/user_instructor.txt", "w+") as instructor_doc:
                                        instructor_doc.writelines(instructor_read_data)

                                if is_already_existing == False:
                                    instructor_append.write(result)
                                    instructor_append.write("\n")


    def extract_info(self):
        self.extract_course_info()
        self.extract_instructor_info()
        self.extract_students_info()
        self.extract_review_info()

    def remove_data(self):
        with open("./data/result/course.txt", 'r+') as course_file:
            course_file.seek(0)
            course_file.truncate()
            # course_file.write("")
        with open("./data/result/review.txt", 'r+') as review_file:
            review_file.seek(0)
            review_file.truncate()
        with open("./data/result/user_student.txt", 'r+') as students_file:
            students_file.seek(0)
            students_file.truncate()
        with open("./data/result/user_instructor.txt", 'r+') as instructor_file:
            instructor_file.seek(0)
            instructor_file.truncate()


    def view_courses(self, args=[]):
        pass

    def view_users(self):
        pass

    def view_reviews(self, args=[]):
        pass

    def __str__(self):
        User.__str__(self)




admin1 = Admin()
# admin1.register_admin('Admin3','AdminPass')
# admin1.extract_course_info()
# admin1.extract_info()
# admin1.extract_instructor_info()
# admin1.__str__()
