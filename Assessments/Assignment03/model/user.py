#Name: AKash Balakrishnan
#Student ID: 32192886
#Description: This class is the parent class to Admin, Instructor, and Student classes.

import re
import random


class User:

    # Variable to store the current login user object
    current_login_user = None

    # Constructor
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role=""):
        self.uid = uid
        self.username = username
        self.password = password
        self.register_time = register_time
        self.role = role

    # String return method
    def __str__(self):
        return str(self.uid) + ";;;" + self.username + ";;;" + self.password + ";;;" + \
               self.register_time + ";;;" + self.role

    # Validating username using regular expression
    def validate_username(self, username):
        try:
            # Regex pattern returns true only if the values are between A-Z, a-z and _ else return false
            username_pattern = "^[A-Za-z_]*$"
            is_username_valid = bool(re.match(username_pattern, username))
            # returning the boolean value
            return is_username_valid
        except:
            return "Something went wrong while validating username"

    # Validating the password
    def validate_password(self, password):
        try:
            # Boolean value
            is_valid_password = False
            # if the password length is greater than or equal to 5 returning true
            if len(password) >= 5:
                is_valid_password = True
            # else returning false
            else:
                is_valid_password = False
            # returning the boolean value
            return is_valid_password
        except:
            return "Something went wrong while validating password"

    # validating email
    def validate_email(self, email):
        try:
            # validating the email using regex
            email_pattern = "^[A-Za-z0-9.-_]+[@]+[A-Za-z0-9-]+.com{1,3}$"
            is_valid_email = False
            if (bool(re.match(email_pattern, email)) == True) and len(email) > 8:
                is_valid_email = True
            else:
                is_valid_email = False
            # returning the boolean value
            return is_valid_email
        except:
            return "Something went wrong while validating email"

    # Deleting all data in user.text file
    def clear_user_data(self):
        try:
            # opening the file to delete
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_file.seek(0)
                user_file.truncate() # deleted
        except:
            return "Something went wrong while clearing user data!"

    #This method checks whether username and password can be matched with users saved in user.txt data file.
    # returns boolean and string
    def authenticate_user(self, username, password):
        try:
            # opening the user.text file to read
            with open("./data/user.txt", "r+", encoding="utf-8") as file_handle_user:
                user_data = file_handle_user.readlines() # storing the lines to a list
                is_authenticated = False
                encrypted_pass = self.encrypt_password(password) # encrypting entered password to authenticate
                user_info_string = "" # empty string to store the user data
                for each in user_data:
                    text_username = each.strip().split(";;;")[1]
                    text_password = each.strip().split(";;;")[2]
                    if text_username == username and text_password == encrypted_pass: # matching the values
                        is_authenticated = True
                        user_info_string += each.strip("\n")
                result = (is_authenticated, user_info_string)

                # returing the authentication result as boolean and user information as a string
                return result

        except:
            return "Something went wrong while authenticating user!"

    # This method checks whether the username is already existing in the user.text file
    def check_username_exist(self, username):
        try:
            # reading the user.text file
            with open("./data/user.txt", "r+", encoding="utf-8") as file_handle_user:
                user_data = file_handle_user.readlines()
                is_username_exist = False
                for each in user_data: # iterating through each line
                    text_username = each.split(";;;")[1]
                    if username == text_username: # matching the values
                        is_username_exist = True
                if is_username_exist == True: # if matched returns true else false
                    return True
                else:
                    return False
        except:
            return "Something went wrong while checking username!"

    # This method is generating and returning a 6 digit unique user id which is not in the user.txt file.
    def generate_unique_user_id(self):
        try:
            # creating an empty string to store the generated user id.
            str_user_id = ""
            # Creating an empty list to store all the ids from the files.
            user_id_list = []
            user_id_existing = False

            # Opening the files to read and store the ids to match with the generated id.

            with open("./data/user.txt", "r+", encoding="utf-8") as file_handle_user:
                user_data = file_handle_user.readlines()
                for each in user_data:
                    # storing the id from user_admin.txt to the admin_id variable using string methods
                    admin_id = each.split(";;;")[0]
                    user_id_list.append(admin_id)
            # Using while loop to generate user until a match is not found.
            while not user_id_existing:
                for i in range(0, 10):
                    str_user_id += str(random.randint(0, 9))

                for each in user_id_list:
                    if str_user_id == str(each).replace("\n", ""):
                        user_id_existing = True
                        break
                    else:
                        user_id_existing = False
                        break
                break

            # If the user id is not existing in other documents then returning the generated id.
            if user_id_existing == False:
                return str_user_id
        except:
            return "Something went wrong while generating a new user id!"

    def encrypt_password(self, password):
        # defining the all_punctuation variable from the task's decription
        all_punctuation = """!"#$%&'()*+,-./:;<=>?@[]^_`{|}~"""
        # Getting length of the input_password to get the corresponding character from all_punctuation
        input_str_len = len(password)
        # Getting all_punctuation's length
        all_punctuation_length = len(all_punctuation)
        # Based on the above description first character = all input_str_len % all_punctuation_length
        first_character = all_punctuation[input_str_len % all_punctuation_length]
        # The second character is defined by all_punctuation[length of str % 5]
        second_character = all_punctuation[input_str_len % 5]
        # The second character is defined by all_punctuation[length of str % 10]
        third_character = all_punctuation[input_str_len % 10]
        # Start and end characters to add
        start_character = '^^^'
        end_character = '$$$'
        # empty encrypted string
        encrypted = """"""
        encrypted += start_character
        # Creating a loop to split the password into 3 a group
        for i in range(0, input_str_len):
            # if i = 0 then i % 3 is 0 which is a range for the first item. #if i = 3 then i % 3 is 0 and so on...
            if i % 3 == 0:
                # adding the characters according to the description
                encrypted += first_character + password[i] + first_character
            # if i = 4 then i % 3 results in 1 which is range for 4th item
            if i % 3 == 1:
                encrypted += (second_character * 2) + password[i] + (second_character * 2)
            # if i = 2 then i % 3 is 2 which is range for 2nd item
            # #if i = 5 then i % 3 is 2 which is range for 5th item
            if i % 3 == 2:
                encrypted += (third_character * 3) + password[i] + (third_character * 3)
        # concatenating the end character with the encrypted string
        encrypted += end_character
        # returning the encrypted string
        return encrypted

    # This method registers (writing) the given user information to the user.text file
    def register_user(self, username, password, email, register_time, role):
        try:
            is_registered = False
            # checking if the username is already existing or not
            is_username_existing = self.check_username_exist(username)
            if is_username_existing == False: # if not existing
                temp_user_id = self.generate_unique_user_id() # generating id by calling the generate_unique_user_id()
                time = self.date_conversion(register_time) # converting the unix time to human readable format
                temp_password = self.encrypt_password(password) # encrypting the password
                write_format = str(temp_user_id) + ";;;" + username + ";;;" + temp_password + ";;;" + str(time) + ";;;" + \
                           role + ";;;" + email # creating a string to write
                with open("./data/user.txt", "a+", encoding="utf-8") as file_handle_user:
                    file_handle_user.write(write_format) # writing the user details to the text
                    file_handle_user.write("\n")
                    is_registered = True
            # returning boolean
            return is_registered
        except:
            return "Something went wrong while registering user!"

    # Reference:
    # Convert Unix timestamp to DD/MM/YYYY HH:MM:SS format - GeeksforGeeks. (2022).
    # Retrieved 10 June 2022, from https://www.geeksforgeeks.org/convert-unix-timestamp-to-dd-mm-yyyy-hhmmss-format/
    def date_conversion(self, register_time):
        converted_time = ""
        given_time = 0
        milli_seconds = 0

        # splitting the last 3 digits of the unix time and saving it as milliseconds
        print(len(str(register_time)))
        if len(str(register_time)) > 10:
            given_time = int(str(register_time)[0:10])
            milli_seconds = int(str(register_time)[10:])
        else:
            given_time = register_time

        # Number of days in a month in a year
        num_of_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        (present_year, days_till_now, extra_time, extra_days,
         index, date, month, hours, minutes, seconds, flag) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        # calculating total days from Unix time
        days_till_now = given_time // (24 * 60 * 60)
        extra_time = given_time % (24 * 60 * 60)
        present_year = 1970

        # calculating present year
        while (days_till_now >= 365):
            if present_year % 400 == 0 or (present_year % 4 == 0 and present_year % 100 != 0):
                days_till_now -= 366
            else:
                days_till_now -= 365
            present_year += 1

        # Updating extra days
        extra_days = days_till_now + 1

        if present_year % 400 == 0 or (present_year % 4 == 0 and present_year % 100 != 0):
            flag = 1

        # Calculating date and month
        month = 0
        index = 0
        if flag == 1:
            while True:
                if index == 1:
                    if extra_days - 29 < 0:
                        break
                    month += 1
                    extra_days -= 29
                else:
                    if extra_days - num_of_days[index] < 0:
                        break
                    month += 1
                    extra_days -= num_of_days[index]
                index += 1
        else:
            while True:
                if extra_days - num_of_days[index] < 0:
                    break
                month += 1
                extra_days -= num_of_days[index]
                index += 1

        # Calculating current month
        if extra_days > 0:
            month += 1
            date = extra_days
        else:
            if month == 2 and flag == 1:
                date = 29
            else:
                date = num_of_days[month - 1]

        # Calculating hours, minutes and seconds
        hours = (extra_time // 3600) + 11
        minutes = (extra_time % 3600) // 60
        seconds = (extra_time % 3600) % 60

        # result format string
        result = str(present_year) + "-" + str(month) + "-" + str(date) + "_" + str(hours) + ":" + str(minutes) \
                 + ":" + str(seconds) + "." + str(milli_seconds)
        converted_time += result

        #returning the converted time
        return converted_time

