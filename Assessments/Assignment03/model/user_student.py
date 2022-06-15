from model.user import User


class Student(User):
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="student",
                 email=""):
        super().__init__(uid, username, password, register_time)
        self.role = role
        self.email = email

    def __str__(self):
        return super().__str__() + self.role + ";;;" + self.email

    def get_students_by_page(self, page):
        try:
            if page > 0:
                with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                    user_data = user_file.readlines()
                    student_data = []
                    student_list = []
                    for item in user_data:
                        split_list = item.split(";;;")
                        if split_list[4] == "student":
                            student_data.append(item)
                    if len(student_data) != 0:
                        total_students = len(student_data)
                        if total_students % 20 == 0:
                            total_pages = total_students / 20
                        else:
                            total_pages = (total_students // 20) + 1
                        if page != total_pages:
                            line_range = page * 20
                            min_range = line_range - 20
                        elif total_pages == 1:
                            line_range = page * 20 - (20 - total_students % 20)
                            min_range = 0
                        else:
                            line_range = page * 20 - (20 - total_students % 20)
                            min_range = line_range - 20
                        for each in range(min_range, line_range):
                            student = student_data[each]
                            student_split_list = student.split(";;;")
                            student_obj = Student(int(student_split_list[0]), student_split_list[1],
                                          student_split_list[2], student_split_list[3],
                                          student_split_list[4], student_split_list[5])
                            student_list.append(student_obj)
                        result = (student_list, total_pages, total_students)
                    else:
                        result = (student_list, 0, 0)
                print(result)
                print(total_students)
                print(total_pages)
                return result
            else:
                print("Invalid page number")

        except:
            return ([None], 0, 0)

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
                    student_split_list = each.strip("\n").split(";;;")
                    id_in_text = int(student_split_list[0])
                    if int(id) == id_in_text:
                        student_obj = Student(int(student_split_list[0]), student_split_list[1],
                                                student_split_list[2], student_split_list[3],
                                                student_split_list[4], student_split_list[5])
                        return student_obj
        except:
            return "No student data found!"


    def delete_student_by_id(self, id):
        try:
            data_list = []
            is_deleted = False
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_data = user_file.readlines()
                for item in user_data:
                    split_list = item.strip("\n").split(";;;")
                    if split_list[4] == "student":
                        student_split_list = item.split(";;;")
                        id_in_text = int(student_split_list[0])
                        if int(id) == id_in_text:
                            user_data.remove(item)
                            is_deleted = True
                            break
                    else:
                        data_list.append(item)

            with open("./data/user.txt", "w+", encoding="utf-8") as user_file:
                for line in data_list:
                    user_file.write(line)
            return is_deleted

        except:
            return "No student record found!"


# stud = Student()
# stud.get_students_by_page(1)
