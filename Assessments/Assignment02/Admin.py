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
                        # id_pattern = r'\"_class\": \"user\", \"id\":.*?\,'
                        # extracted_id = re.search(id_pattern, each)
                        # if str(extracted_id) == "None":
                        #     {
                        #         id_existing == False
                        #     }
                        # else:
                        #     {
                        #         id_existing == True
                        #     }
                        all_pattern = r'\"_class\": \"course_review\", \"id\": (.*?)\,' \
                                      r'.*?\"_class\": \"user\", \"id\": (.*?)\,.*? \"title\": \"(.*?)\",' \
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
                                extracted_user_title = str(ordered_list[3]).lower()
                                stud_password = extracted_user_title + extracted_user_id + extracted_user_title
                                encrypted_pass = User.encryption(self,stud_password)
                                user_name_password = [stud_user_name, encrypted_pass]
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
        pass

    def extract_info(self):
        pass

    def remove_data(self):
        pass

    def view_courses(self, args=[]):
        pass

    def view_users(self):
        pass

    def view_reviews(self, args=[]):
        pass

    def __str__(self):
        pass




admin1 = Admin()
# admin1.register_admin('Admin3','AdminPass')
admin1.extract_students_info()
