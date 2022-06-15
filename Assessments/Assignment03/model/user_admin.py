#Name: AKash Balakrishnan
#Student ID: 32192886
#Description: This class registers admin to the user text file


from model.user import User

# child class to the user class
class Admin(User):

    # Constructor
    def __init__(self,uid = -1, username = "", password = "", register_time = "yyyy-MM-dd_HH:mm:ss.SSS", role = "admin"):
        super().__init__(uid, username, password, register_time)
        self.role = role

    # This method will register an admin to the user file without duplicates
    def register_admin(self):
        try:
            # assigning the encrypted password, and generating uid.
            temp_password = self.password
            self.password = User.encrypt_password(self,temp_password)
            self.uid = User.generate_unique_user_id(self)
            admin_list = [] # to store the admin details
            # reading the user text file
            with open("./data/user.txt", "r+", encoding="utf-8") as user_text:
                text_data = user_text.readlines()
                for each in text_data:
                    temp_role = (each.split(";;;")[4]).strip("\n")
                    if temp_role == "admin":
                        admin_list.append(each) # if any admin found this line will append the data to the list
            if len(admin_list) == 0:
                with open("./data/user.txt", "a+", encoding="utf-8") as user_text:
                    user_text.write(self.__str__()) # if no admin found this line will write the admin in the list
                    user_text.write("\n")
            else:
                for item in admin_list:
                    temp_username = item.split(";;;")[1]
                    temp_password = item.split(";;;")[2]
                    # if admin found in the admin list this method checks for the username and password.
                    if temp_username == self.username and temp_password == self.password:
                        print("User already existing") # if matched printing already existing
                    else:
                        with open("./data/user.txt", "a+", encoding="utf-8") as user_text:
                            user_text.write(self.__str__()) # else writing the admin to the text file.
                            user_text.write("\n")
        except:
            return "Something went wrong while registering admin!"

    # String return method
    def __str__(self):
        return super().__str__()
