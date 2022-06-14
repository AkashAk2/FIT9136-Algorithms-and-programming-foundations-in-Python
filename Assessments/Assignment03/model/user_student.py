from model.user import User


class Student:
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="student",
                 email=""):
        self.uid = uid
        self.username = username
        self.password = password
        self.register_time = register_time
        self.role = role
        self.email = email

    def __str__(self):
        return str(self.uid) + ";;;" + self.username + ";;;" + self.password + ";;;" + self.register_time + ";;;" + \
               self.role + ";;;" + self.email

    def get_students_by_page(self, page):
        try:
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_data = user_file.readlines()
                student_data = []
                for item in user_data:
                    split_list = item.split(";;;")
                    if split_list[4] == "student":
                        student_data.append(item)

                total_students = len(student_data)
                total_pages = round(total_students / 20)
                line_range = page * 20
                student_list = []
                for each in range(line_range - 20, line_range):
                    student = student_data[each]
                    student_split_list = student.split(";;;")
                    student_obj = Student(int(student_split_list[0]), student_split_list[1],
                                          student_split_list[2], student_split_list[3],
                                          student_split_list[4], student_split_list[5])
                    student_list.append(student_obj)
                result = (student_list, total_pages, total_students)
                print(result)
                print(total_students)
                print(total_pages)
                return result

        except:
            return "No student record found!"

    def get_student_by_id(self, id):
        try:
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_data = user_file.readlines()
                student_data = []
                for item in user_data:
                    split_list = item.split(";;;")
                    if split_list[4] == "student":
                        student_data.append(item)

                for each in student_data:
                    student_split_list = each.split(";;;")
                    id_in_text = int(student_split_list[0])
                    if id == id_in_text:
                        student_obj = Student(int(student_split_list[0]), student_split_list[1],
                                                student_split_list[2], student_split_list[3],
                                                student_split_list[4], student_split_list[5])
                        return student_obj
        except:
            return "No student data found!"


    def delete_student_by_id(self, id):
        try:
            is_deleted = False
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_data = user_file.readlines()
                student_data = []
                for item in user_data:
                    split_list = item.split(";;;")
                    if split_list[4] == "student":
                        student_data.append(item)
                for each in student_data:
                    student_split_list = each.split(";;;")
                    id_in_text = int(student_split_list[0])
                    if id == id_in_text:
                        user_data.remove(each)
                        is_deleted = True

                for line in user_data:
                    user_file.write(line)
                    user_file.truncate()

            return is_deleted

        except:
            return "No student record found!"




stud = Student()
# stud.get_students_by_page(1)
