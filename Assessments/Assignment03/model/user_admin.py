from model.user import User

class Admin:

    def __init__(self,uid = -1, username = "", password = "", register_time = "yyyy-MM-dd_HH:mm:ss.SSS", role = "admin"):
        self.uid = uid
        self.username = username
        self.password = password
        self.register_time = register_time
        self.role = role

    def register_admin(self):
        try:
            temp_password = self.password
            self.password = User.encrypt_password(self,temp_password)
            self.uid = User.generate_unique_user_id(self)
            with open("./data/user.txt", "a+", encoding="utf-8") as user_text:
                user_text.write(self.__str__())
                user_text.write("\n")
        except:
            return "Something went wrong while registering admin!"



    def __str__(self):
        return str(self.uid) + ";;;" + self.username + ";;;" + self.password + ";;;" + self.register_time \
               + ";;;" + self.role
