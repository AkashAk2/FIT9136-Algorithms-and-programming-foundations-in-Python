#Author: Akash Balakrishnan
#Student ID: 32192886

#importing random to generate random numbers in below class
import random

class User:

    #Constructor with default values
    def __init__(self, id = -1, username = "", password = ""):
        self.id = id
        self.username = username
        self.password = password

    """ The method below will generate a 10 digit unique user id.
    This method also verifies that the user id generated is not present in the user_admin.txt, user_instructor.txt and
    user_student.txt """
    def generate_unique_user_id(self):
        # creating an empty string to store the generated user id.
        str_user_id = ""
        #Creating an empty list to store all the ids from the files.
        user_id_list = []
        user_id_existing = False

        #Opening the files to read and store the ids to match with the generated id.

        with open("./data/result/user_admin.txt", "r+") as file_handle_admin:
            admin_data = file_handle_admin.readlines()
            for each in admin_data:
                #storing the id from user_admin.txt to the admin_id variable using string methods
                admin_id = each.split(";;;")[0]
                user_id_list.append(admin_id)
        # Creating a blank file in the begening
        create_instructor = open("./data/result/user_instructor.txt", "a+")
        create_instructor.close()
        #Reading instructor file if data is availale in it.
        with open("./data/result/user_instructor.txt", "r+") as file_handle_instructor:
            instructor_data = file_handle_instructor.readlines()
            for each in instructor_data:
                # storing the id from user_instructor.txt to the instructor_id variable using string methods
                instructor_id = each.split(";;;")[0]
                user_id_list.append(instructor_id)

        #creating blank file
        create_student = open("./data/result/user_student.txt", "a+")
        create_student.close()
        # Reading instructor file if data is availale in it.
        with open("./data/result/user_student.txt", "r+") as file_handle_student:
            student_data = file_handle_student.readlines()
            for each in student_data:
                # storing the id from user_student.txt to the student_id variable using string methods
                student_id = each.split(";;;")[0]
                user_id_list.append(student_id)

        #Using while loop to generate user until a match is not found.
        while not user_id_existing:
            for i in range(0, 10):
                str_user_id += str(random.randint(0, 9))

            for each in user_id_list:
                if str_user_id == str(each).replace("\n",""):
                    user_id_existing = True
                    break
                else:
                    user_id_existing = False
                    break
            break

        # If the user id is not existing in other documents then returning the generated id.
        if user_id_existing == False:
            return str_user_id


    # Defining encyption function which encrypts the user password and return the encrypted password
    def encryption(self, input_password):
        #defining the all_punctuation variable from the task's decription
        all_punctuation ="""!"#$%&'()*+,-./:;<=>?@[]^_`{|}~"""
        #Getting length of the input_password to get the corresponding character from all_punctuation 
        input_str_len = len(input_password)
        #Getting all_punctuation's length
        all_punctuation_length = len(all_punctuation)
        #Based on the above description first character = all input_str_len % all_punctuation_length 
        first_character = all_punctuation[input_str_len % all_punctuation_length]
        #The second character is defined by all_punctuation[length of str % 5]
        second_character = all_punctuation[input_str_len % 5]
        #The second character is defined by all_punctuation[length of str % 10]
        third_character = all_punctuation[input_str_len % 10]
        #Start and end characters to add
        start_character = '^^^' 
        end_character = '$$$' 
        #empty encrypted string 
        encrypted = """""" 
        encrypted += start_character
        #Creating a loop to split the password into 3 a group
        for i in range(0,input_str_len):
        #if i = 0 then i % 3 is 0 which is a range for the first item. #if i = 3 then i % 3 is 0 and so on...
            if i % 3 == 0:
                #adding the characters according to the description
                encrypted += first_character + input_password[i] + first_character
            #if i = 4 then i % 3 results in 1 which is range for 4th item
            if i % 3 == 1:
                encrypted += (second_character*2) + input_password[i] + (second_character * 2)
            #if i = 2 then i % 3 is 2 which is range for 2nd item 
            # #if i = 5 then i % 3 is 2 which is range for 5th item 
            if i % 3 == 2:
                encrypted += (third_character * 3) + input_password[i] + (third_character * 3)
        #concatinating the end character with the encrypted string
        encrypted += end_character 
        #returning the encrypted string 
        return encrypted

    # Defining login method which verifies the username and password if it matches then the return the user type.
    def login(self):
        #Encrypting the user entered password to match the password stored in the text file.
        encrypted_password = self.encryption(str(self.password))
        is_logged_in = False
        #Opening the user_admin.txt to read the admin users
        file_handle_admin = open("./data/result/user_admin.txt", "r+")
        admin_data = file_handle_admin.readlines()
        # Iterating through each line in user_admin.txt file to find a match
        for line in admin_data:
            # storing the username and password from the user_admin.txt using string methods
            temp_username = line.split(";;;")[1]
            temp_password = line.split(";;;")[-1].replace("\n", "")
            # if condition to check whether the entered details are valid or not.
            # if it is valid then returning the user role and user info with login result.
            if self.username == temp_username and encrypted_password == temp_password:
                login_result = True
                login_user_role = "Admin"
                login_user_info = [self.id, self.username]
                is_logged_in = True
                return (login_result, login_user_role, login_user_info)
        file_handle_admin.close()

        # Opening user_instructor.txt to find a match
        file_handle_instructor = open("./data/result/user_instructor.txt", "r+")
        instructor_data = file_handle_instructor.readlines()
        for line in instructor_data:
            # storing the username and password from the user_admin.txt using string methods
            inst_username = line.split(";;;")[1]
            inst_password = line.split(";;;")[2]
            # if condition to check whether the entered details are valid or not.
            # if it is valid then returning the user role and user info with login result.
            if self.username == inst_username and encrypted_password == inst_password:
                login_result = True
                login_user_role = "Instructor"
                login_user_info = [self.id, self.username]
                is_logged_in = True
                return (login_result, login_user_role, login_user_info)
        file_handle_instructor.close()

        # Opening user_student.txt to find a match
        file_handle_student = open("./data/result/user_student.txt", "r+")
        student_data = file_handle_student.readlines()
        # Iterating though every line of user_student.txt
        for line in student_data:
            # storing the username and password from the user_admin.txt using string methods
            stud_username = line.split(";;;")[1]
            stud_password = line.split(";;;")[2]
            # if condition to check whether the entered details are valid or not.
            if self.username == stud_username and encrypted_password == stud_password:
                login_result = True
                login_user_role = "Student"
                login_user_info = [self.id, self.username]
                is_logged_in = True
                return (login_result, login_user_role, login_user_info)
        file_handle_student.close()

        #if the login attempt fails return the login_result as False
        if is_logged_in == False:
            login_result = False
            return login_result

    # Methods to print messages.
    def extract_info(self):
        print("You have no permission to extract information")
    
    def view_courses(self,args=[]):
        print("You have no permission to view courses")
    
    def view_users(self):
        print("You have no permission to view users")
    
    def view_reviews(self,args=[]):
        print("You have no permission to view reviews")
    
    def remove_data(self):
        print("You have no permission to remove data")

    # __str__ method returns the user data in a format writen below.
    def __str__(self):
        user_format = str(self.id) + ";;;" + self.username + ";;;" + self.password
        return user_format



