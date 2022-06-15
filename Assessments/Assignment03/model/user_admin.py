from model.user import User

class Admin(User):

    def __init__(self,uid = -1, username = "", password = "", register_time = "yyyy-MM-dd_HH:mm:ss.SSS", role = "admin"):
        super().__init__(uid, username, password, register_time)
        self.role = role

    def register_admin(self):
        try:
            temp_password = self.password
            self.password = User.encrypt_password(self,temp_password)
            self.uid = User.generate_unique_user_id(self)
            admin_list = []
            with open("./data/user.txt", "r+", encoding="utf-8") as user_text:
                text_data = user_text.readlines()
                for each in text_data:
                    temp_role = (each.split(";;;")[4]).strip("\n")
                    if temp_role == "admin":
                        admin_list.append(each)
            if len(admin_list) == 0:
                with open("./data/user.txt", "a+", encoding="utf-8") as user_text:
                    user_text.write(self.__str__())
                    user_text.write("\n")
            else:
                for item in admin_list:
                    temp_username = item.split(";;;")[1]
                    temp_password = item.split(";;;")[2]
                    if temp_username == self.username and temp_password == self.password:
                        print("User already existing")
                    else:
                        with open("./data/user.txt", "a+", encoding="utf-8") as user_text:
                            user_text.write(self.__str__())
                            user_text.write("\n")
        except:
            return "Something went wrong while registering admin!"

    def __str__(self):
        return super().__str__()
