import re
import os
from User import User
from Course import Course
from Review import Review


# Admin class is a child class of User class
class Admin(User):

    #Constructor
    def __init__(self, user_id = -1, username = "", password = ""):
        super().__init__(user_id, username, password)

    #Register admin function to create an admin initially
    def register_admin(self):
        #Creating a blank list to store all the usernames
        username_list = []
        #using boolean variables to perform tasks
        registered = False
        is_blank = False
        #creating a admin text file using a+
        file_creation_admin = open('./data/result/user_admin.txt', 'a+')
        #openning the user_admin text file in read mode
        file_handle_admin = open('./data/result/user_admin.txt', 'r')
        #reading all lines in the text file
        admin_data = file_handle_admin.readlines()
        #encrypting the user password by calling the encryption function from parent class User
        encrypted_pass = User.encryption(self,self.password)
        #iterating through each line in admin_data which holds all lines of the text file
        for each in admin_data:
            #using split method storing the username to username_data
            username_data = each.split(";;;")[1]
            #appending the username_data to the blank list  created above username_list[]
            username_list.append(username_data)
        #iterating through each item of username_list appended above
        for each in username_list:
            #if the username matches with each line print that the admin username is already registered and exit loop
            if self.username == each:
                registered = True
                print("Admin already registered")
                break
        #using registered boolean value to write the admin details if it is not matched above
        if registered == False:
            temp_userid = User.generate_unique_user_id(self)
            self.id = str(temp_userid)
            file_creation_admin.seek(0)
            file_creation_admin.write(self.id)
            file_creation_admin.write(";;;" + self.username + ";;;" + encrypted_pass)
            file_creation_admin.write("\n")
        #closing all the openned files
        file_creation_admin.close()
        file_handle_admin.close()

    # Extract course info method performed to extract the course detais from raw_data.txt
    def extract_course_info(self):
        #openning the raw_data text file to read
        with open("./data/course_data/raw_data.txt", "r+") as file_handle:
            #storing all the lines in the data variable
            data = file_handle.readlines()
            #for each line in data extract the needed items using re.findall method
            for each in data:
                pattern = r'\_class\":\"course\"\,\"id\":([0-9]*).*?\"title\":\"(.*?)\"' \
                          r'.*?\"headline\":\"(.*?)\".*?\"num_subscribers.*?\":(.*?)\,\"caption_locales' \
                          r'.*?\"avg_rating\":(.*?)\,\"avg_rating_recent' \
                          r'.*?\"image_100x100\":\"(.*?)\"' \
                          r'.*?\"content_info\":\"([0-9.]*)'
                extracted_data = re.findall(pattern, each)
                #openning the course.txt file using a+ (it also creates the file)
                with open("./data/result/course.txt", "a+") as course_file:
                    #for each line in extracted data writing the items in the format given below
                    for line in extracted_data:
                        course_id = line[0]
                        course_title = line[1]
                        course_image = line[5]
                        course_headline = line[2]
                        course_subscribers = line[3]
                        course_rating = line[4]
                        course_length = line[6]
                        write_format = course_id + ";;;" + course_title + ";;;" + course_image + ";;;" \
                                       + course_headline + ";;;" + course_subscribers + ";;;" \
                                       + course_rating + ";;;" + course_length
                        course_file.write(write_format)
                        course_file.write("\n")


    # function to extract the review informations to review.txt
    def extract_review_info(self):
        #changing the folder path using os
        folder_path = './data/review_data'
        # iterating through each file in the review_data folder
        for file in os.listdir(folder_path):
            # checking whether the reading file is ending with .json
            if file.endswith('.json'):
                #creating the file path using os.path.join
                file_path = os.path.join(folder_path, file)
                course_id = os.path.basename(file).split('.')[0]
                # reading each file in that path
                with open(file_path,'r') as f:
                    data = f.readlines()
                    # for each line extracting the details using re.findall
                    for each in data:
                        pattern = r'\"_class\": \"course_review\", \"id\":.([0-9]*)\, \"content\":\ \"(.*?)\",' \
                                r'.*? \"rating\": (.*?)\,'
                        extracted_data = re.findall(pattern, each)
                        #opening review.txt file using a+ (to append and also to create the file if it doesn't exist)
                        with open('./data/result/review.txt','a+') as review_file:
                            #for each line in extracted data variable
                            for line in extracted_data:
                                num = 0
                                data_list = list(line)
                                # writing the data list created above to the text file.
                                for item in data_list:
                                    review_file.write(item)
                                    if num < len(data_list):
                                        review_file.write(";;;")
                                        num += 1
                                review_file.write(course_id)
                                review_file.write("\n")

    # extract_students_info function will create a file for students with data from the review_data folder files.
    def extract_students_info(self):
        id_existing = False
        # folder path
        folder_path = './data/review_data'
        # iterating through each file in folder path
        for file in os.listdir(folder_path):
            # checking for .json if exists then creating file path
            if file.endswith('.json'):
                file_path = os.path.join(folder_path, file)
                course_id = os.path.basename(file).split('.')[0]
                # opening file path to read
                with open(file_path, 'r') as f:
                    data = f.readlines()
                    # for each item in the data created above by reading lines extract info using re.findall
                    for each in data:
                        all_pattern = r'\"_class\": \"course_review\", \"id\": ([0-9]*)\,' \
                                      r'.*?\"_class\": \"user\",(.*?) \"title\": \"(.*?)\",' \
                                      r'.*?\"image_50x50\": \"(.*?)\",.*?\"initials\": \"(.*?)\"'
                        extracted_data = re.findall(all_pattern, each)
                        # opening user_student.txt to write the extracted data in the format writen below
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
                                # the regex will give "id" text so splitting the digits only and adding it to stud_id
                                for digit in extracted_user_id:
                                    if digit.isdigit() == True:
                                        stud_id += str(digit)
                                # if length of stud_id is 0 then generating unique user id for the student
                                if len(stud_id) == 0:
                                    stud_id += str(User.generate_unique_user_id(self))
                                extracted_user_title = str(ordered_list[3]).lower()
                                stud_password = extracted_user_title + stud_id + extracted_user_title
                                encrypted_pass = User.encryption(self,stud_password)
                                user_name_password = [stud_user_name, encrypted_pass]
                                ordered_list[0] = stud_id
                                # the extracted list is not in the correct format as required to rearraging them
                                final_list = [ordered_list[0], user_name_password[0], user_name_password[1],
                                              ordered_list[1], ordered_list[2], ordered_list[3], ordered_list[4]]
                                # writing the final ordered list to the text file
                                for item in final_list:
                                    student_file.write(item)
                                    if num < len(final_list):
                                        student_file.write(";;;")
                                        num += 1
                                student_file.write("\n")

    # extract_instructor_info function extracts all the instructors from raw_data.txt
    def extract_instructor_info(self):
        # opening raw data text file to read
        with open("./data/course_data/raw_data.txt") as file_handle:
            data = file_handle.readlines()
            # iterating each line to extract data using re.findall
            for line in data:
                pattern = r'\"_class\":\"course\",\"id\":(.*?)\,.*?\"visible_instructors\":\[(.*?)\]'
                extracted_data = re.findall(pattern, line)

                # after splitting visible_instructors from raw data extracting instructors details using findall
                for item in extracted_data:
                    course_id = item[0]
                    instructors_data = item[1]
                    instructors_pattern = r'{(.*?)}'
                    instructors_info = re.findall(instructors_pattern, instructors_data)

                    # writing each instructor in the extracted data to the text using the required format
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

                        # opening the user_instructor text file to write and at the same time to avoid duplicates
                        with open("./data/result/user_instructor.txt", "a+") as instructor_append:
                            is_already_existing = False
                            with open("./data/result/user_instructor.txt", "r+") as instructor_read:
                                instructor_read_data = instructor_read.readlines()
                                instructor_data_list = []
                                # spliting the instructor id and appending it to the list created above
                                for each in instructor_read_data:
                                    instructor_temp_id = each.split(";;;")[0]
                                    instructor_data_list.append(instructor_temp_id)

                                # if instructor id is already exisiting then append the course id to that line.
                                if instructor_id in instructor_data_list:
                                    is_already_existing = True
                                    get_instructor_line = instructor_data_list.index(instructor_id)
                                    single_instructor = instructor_read_data[get_instructor_line].strip("\n")
                                    single_instructor += "--" + course_id + "\n"
                                    instructor_read_data[get_instructor_line] = single_instructor
                                    with open("./data/result/user_instructor.txt", "w+") as instructor_doc:
                                        instructor_doc.writelines(instructor_read_data)
                                # if not then write the entire line.
                                if is_already_existing == False:
                                    instructor_append.write(result)
                                    instructor_append.write("\n")

    # extracting_info method calls the methods defined above to extract the data
    def extract_info(self):
        self.extract_course_info()
        self.extract_instructor_info()
        self.extract_students_info()
        self.extract_review_info()

    # remove data method deletes everything inside the text file
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

    #view courses method will produce the requested course detail by keyword, id, instructor_id
    def view_courses(self, args=[]):
        # checking the length of the args if 0 or 2 then execute else printing invalid input
        if len(args) == 0 or len(args) == 2:
            # if the length of arguments is 2
            if len(args) == 2:
                # assinging the args[1] as keyword
                keyword = args[1]
                # if args[0] is TITLE_KEYWORD then calling the find_course_by_title_keyword from Course class
                if args[0] == "TITLE_KEYWORD":
                    title_matched_courses = Course.find_course_by_title_keyword(self,str(keyword))
                    # if the matched courses are greater than 10 then printing only 10 of them and total no of matches
                    if len(title_matched_courses) > 10:
                        for each in title_matched_courses[:10]:
                            print(each)
                        print("Total returned course: ", len(title_matched_courses))
                    # if not then printing everything
                    else:
                        for each in title_matched_courses:
                            print(each)
                # this part is executed if the arg[0] is ID and print the id matched course
                elif args[0] == "ID":
                    id_matched_courses = Course.find_course_by_id(self, keyword)
                    print(id_matched_courses)
                # this is for finding course by INSTRUCTOR_ID if match found printing the match courses
                elif args[0] == "INSTRUCTOR_ID":
                    instructor_matched_courses = Course.find_course_by_instructor_id(self, keyword)
                    if len(instructor_matched_courses) > 10:
                        for each in instructor_matched_courses[:10]:
                            print(each)
                    else:
                        for each in instructor_matched_courses:
                            print(each)
                #if the arg[0] is not one of the things stated above then printing invalid input
                else:
                    print("Invalid input please only enter TITLE_KEYWORD, ID, or INSTRUCTOR_ID as command")
            # if there is no arg passed then printing the total number of courses
            elif len(args) == 0:
                all_courses = Course.course_overview(self)
                print("The total number of courses are: ", all_courses)
        else:
            print("Invalid input")

    # view users method will print the total number of admins, instructors and students
    def view_users(self):
        with open("./data/result/user_admin.txt", "r") as admin_file:
            admin_data = admin_file.readlines()
            admin_count = len(admin_data)
            print("Total number of admins: ", admin_count)

        with open("./data/result/user_instructor.txt", "r") as instructor_file:
            instructor_data = instructor_file.readlines()
            instructor_count = len(instructor_data)
            print("Total number of instructors: ", instructor_count)

        with open("./data/result/user_student.txt", "r") as student_file:
            student_data = student_file.readlines()
            student_count = len(student_data)
            print("Total number of students: ", student_count)

    # view reviews will print the reviews for the course id
    def view_reviews(self, args=[]):
        # checking the length of the args if 0 or 2 then execute else printing invalid input
        if len(args) == 0 or len(args) == 2:
            # if the length of arguments is 2
            if len(args) == 2:
                keyword = args[1]
                # if args[0] is ID then calling the find_review_by_id from Review class
                if args[0] == "ID":
                    id_matched_reviews = Review.find_review_by_id(self, keyword)
                    if id_matched_reviews != None:
                        print(id_matched_reviews)
                    else:
                        print(None)
                # if the arg is KEYWORD then calling the find_review_by_keyword function from the Review class
                elif args[0] == "KEYWORD":
                    keyword_matched_reviews = Review.find_review_by_keywords(self, keyword)
                    # printing 10 reviews only if the match is more than that
                    if len(keyword_matched_reviews) > 10:
                        for each in keyword_matched_reviews[:10]:
                            print(each)
                        print("Total returned reviews: ", len(keyword_matched_reviews))
                # if the arg is COURSE_ID calling the find_review_by_course_id function from Review
                elif args[0] == "COURSE_ID":
                    course_id_matched_reviews = Review.find_review_by_course_id(self, keyword)
                    if len(course_id_matched_reviews) > 10:
                        for each in course_id_matched_reviews[:10]:
                            print(each)
                        print("Total returned reviews: ", len(course_id_matched_reviews))
                else:
                    print("Invalid input please only enter (ID or KEYWORD or COURSE_ID) as command")
            # if no arg is passed then printing the total number of reviews in review.txt file.
            elif len(args) == 0:
                all_reviews = Review.reviews_overview(self)
                print("Total number of reviews are: ", all_reviews)
        else:
            print("Invalid input please enter command and value only!")

    # str method inherited from parent class
    def __str__(self):
        return User.__str__(self)

