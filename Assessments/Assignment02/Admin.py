import re
from User import User



class Admin(User):
    
    def __init__(self, user_id = -1, username = "", password = ""):
        super().__init__(user_id, username, password)

    def register_admin(self, username, password):
        print('register admin function is openned')
        registered = False
        file_handle_admin = open('user_admin.txt', 'r+')
        encrypted_pass = User.encryption(self,password)
        for line in file_handle_admin:
            print("file handle for is open", line)
            line_list = [line.split(';;;')]
            print("line_list", line_list)
            for each in line_list:
                print("In for loop of line_list")
                print("each", each)
                print(each[1])
                print(each[2])
                if username == each[1] and encrypted_pass == each[2]:
                    print("User is already registered as admin!")
                    registered = True
                    break

        if registered == False:
            write_admin = open("user_admin.txt", "a+")
            temp_userid = User.generate_unique_user_id(self)
            str_user_id = str(temp_userid)
            write_admin.write("\n")
            write_admin.write(str_user_id)
            write_admin.write(";;;" + username + ";;;" + encrypted_pass)
            write_admin.close()

        file_handle_admin.close()

    def extract_course_info(self):

        with open("./data/course_data/raw_data.txt") as file_handle:
            data = file_handle.readlines()
            i = 0
            for each in data:
                # # new_data = data.replace("\n", "").replace("\t", "")
                # pattern = r'\_class":"course"\,(.*?)\,"url".*?"visible_instructors":\[\{(.*?)\,"id".*?"tracking_id":' \
                #         r'.*?,(.*?)\,"caption_locales".*?,\{"_class":"locale".*?]\,(.*?)\,"avg_rating_recent"' \
                #         r'.*?"instructor_name":.*?\,(.*?)\,"content_info_short"'
                # extracted_class_course = re.findall(pattern, each)
                # second_pattern = r'\"id\":([0-9]*)\,.*?\"title\":\"(.*?)\".*?\"image_100x100\":\"(.*?)\"' \
                #                 r'.*?\"headline\":\"(.*?)\".*?\"num_subscribers\":(.*?)\',.*?\"avg_rating\":(.*?)\',' \
                #                 r'.*?\'\"content_info\":\"([0-9.]*)'
                # extracted_data = re.findall(second_pattern, ((str)(extracted_class_course)))
                pattern = r'\_class\":\"course\"\,\"id\":([0-9]*).*?\"title\":\"(.*?)\"' \
                          r'.*?\"headline\":\"(.*?)\".*?\"num_subscribers.*?\":(.*?)\,\"caption_locales' \
                          r'.*?\"avg_rating\":(.*?)\,\"avg_rating_recent' \
                          r'.*?\"image_100x100\":\"(https://img-c.udemycdn.com/course.*?)\"' \
                          r'.*?\"content_info\":\"([0-9.]*)'
                extracted_data = re.findall(pattern, each)
                # course_file = open("./data/course_data/course.txt", 'w')
                i += 1
                print(extracted_data)
                print(i)
                with open("./data/course_data/course.txt", "a+") as course_file:
                    num = 0
                    for line in extracted_data:
                        data_list = list(line)
                        list_order = [0,1,5,2,3,4,6]
                        ordered_list = [data_list[i] for i in list_order]
                        for each in ordered_list:
                            course_file.write(each)
                            if num < len(each):
                                course_file.write(";;;")
                                num += 1
                        course_file.write("\n")



    def extract_review_info(self):
        pass

    def extract_students_info(self):
        pass

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
admin1.extract_course_info()
