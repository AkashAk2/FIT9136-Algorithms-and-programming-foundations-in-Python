from asyncore import write
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
        # file_handle_raw_data = open("data/course_data/raw_data.txt", 'r')
        # pattern =
        # for line in file_handle_raw_data:
        # with open("./data/course_data/test.txt") as file_read:
        #     data = file_read.read()
        #     print(data)
        #
        #     print(extracted_item_data)
        #     # for each in data:
        #     #     for item in eval(each):
        #     #         print(item['id'], item['title'], item['price'])

        with open("./data/course_data/test.txt") as file_handle:
            data = file_handle.read()
            new_data = data.replace("\n", "").replace("\t", "")
            new_data




                # extracted_item_data = re.findall(pattern, line)
                # # print(extracted_item_data)
                # # course id
                # print(extracted_item_data)
                # pat = r"_class\":\"course\",\"id\":[0-9]*,"
                # ids = re.findall(pat, extracted_item_data[0])
                # # print(ids)
                # # for i in range(0, len(ids)):
                # #     # ids[i] = re.findall(r"[0-9]*", ids[i])
                # #     print(ids[i])
                # # print(ids[0])
                #
                # for each in ids:
                #     print(each)
                #     # for item in eval(each):
                #     #     print(item)

                # data.append(extracted_item_data)
        # print(data[3])

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
