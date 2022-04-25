import random

class User:

    def __init__(self):
        self.user_id = -1
        self.username = ""
        self.password = ""

    def generate_unique_user_id(self):
       self.user_id = ""
       user_id_existing = False
       while not user_id_existing:
          for each in range(0,10):
             self.user_id += str(random.randint(0,9))
          file_handle_admin = open('user_admin.txt', 'r')
          if self.user_id not in file_handle_admin:
              user_id_existing = False
          else:
              user_id_existing = True
          file_handle_instructor = open('user_instructor.txt', 'r')
          if self.user_id not in file_handle_instructor:
              user_id_existing = False
          else:
              user_id_existing = True
          file_handle_student = open('user_student.txt', 'r')
          if self.user_id not in file_handle_student:
              user_id_existing = False
              break
          else:
              user_id_existing = True

       print(self.user_id)
       return self.user_id

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
                encrypted += first_character + input_password[i] + first_character #if i = 1 then i % 3 is 1 which is range for 1st item
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
        print(encrypted)
        return encrypted

    def login(self):
        self.username = "Akash"
        self.password = "Akash123232"
        encrypted_password = self.encryption(self.password)
        file_handle_admin = open('user_admin.txt', 'r')
        for line in file_handle_admin:
          if self.username and encrypted_password in line:
              login_result = True
              login_user_role = "Admin"
              login_user_info = [self.user_id, self.username]
              return (login_result, login_user_role, login_user_info)
          else:
              login_result = False
              return login_result
        file_handle_admin.close()
        file_handle_instructor = open('user_instructor.txt','r')
        for line in file_handle_instructor:
            if self.username and encrypted_password in line:
                login_result = True
                login_user_role = "Instructor"
                login_user_info = [self.user_id, self.username]
                return (login_result, login_user_role, login_user_info)
            else:
                login_result = False
                return login_result
        file_handle_instructor.close()
        file_handle_student = open('user_student.txt','r')
        for line in file_handle_student:
            if self.username and encrypted_password in line:
                login_result = True
                login_user_role = "Student"
                login_user_info = [self.user_id, self.username]
                return (login_result, login_user_role, login_user_info)
            else:
                login_result = False
                return login_result
    
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
    
    def __str__(self):
        print(self.user_id)
        return str(self.user_id) + ";;;" + self.username + ";;;" + self.password








user1 = User()
user1.generate_unique_user_id()
user1.encryption("Password")
user1.login()
user1.extract_info()
user1.view_courses()
user1.__str__()


