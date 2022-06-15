#Name: AKash Balakrishnan
#Student ID: 32192886
#Description: This class manages the student data



from model.user import User

# Child to User class
class Student(User):

    # Constructor
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS", role="student",
                 email=""):
        super().__init__(uid, username, password, register_time)
        self.role = role
        self.email = email

    # String return method
    def __str__(self):
        return super().__str__() + self.role + ";;;" + self.email

    # This method will return a tuple of student object and total pages and total students.
    def get_students_by_page(self, page):
        try:
            # if page is greater than 0 the following will execute
            if page > 0:
                # reading the user.text file
                with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                    user_data = user_file.readlines()
                    student_data = [] #list to store the student data
                    student_list = [] #list to store the student objects
                    for item in user_data:
                        split_list = item.split(";;;")
                        if split_list[4] == "student": # splitting the student data from user.text
                            student_data.append(item) # appending the student data to the list
                    # if student data is found calculating the total students, total pages
                    if len(student_data) != 0:
                        total_students = len(student_data)

                        # if total_students / 20 remainder is 0 setting the total pages like below
                        if total_students % 20 == 0:
                            total_pages = total_students / 20
                        # else increasing one page to accommodate the student data
                        else:
                            total_pages = (total_students // 20) + 1

                        # if current page is not last page setting the range(index for list)
                        if page != total_pages:
                            line_range = page * 20
                            min_range = line_range - 20
                        # if total pages is 1 then minimum range is 0 max is the count of students
                        elif total_pages == 1:
                            line_range = page * 20 - (20 - total_students % 20)
                            min_range = 0
                        # else setting up the line range as follows
                        else:
                            line_range = page * 20 - (20 - total_students % 20)
                            min_range = line_range - 20
                        # iterating through the list to retrieve the student data
                        for each in range(min_range, line_range):
                            student = student_data[each]
                            student_split_list = student.split(";;;")
                            # Creating student objects
                            student_obj = Student(int(student_split_list[0]), student_split_list[1],
                                          student_split_list[2], student_split_list[3],
                                          student_split_list[4], student_split_list[5])
                            # appending the student objects to the list
                            student_list.append(student_obj)
                        result = (student_list, total_pages, total_students)
                    else:
                        result = (student_list, 0, 0)
                # returning a tuple contains (student_list, total_pages, total_students)
                return result
            # if page is not greater than 0 then page number is not valid.
            else:
                print("Invalid page number")

        except:
            return ([None], 0, 0)

    # This method will return the student object by id.
    def get_student_by_id(self, id):
        try:
            # reading the file
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_data = user_file.readlines()
                student_data = [] # list to store the student data
                for item in user_data:
                    split_list = item.split(";;;")
                    if split_list[4] == "student": # splitting student data from the user file
                        student_data.append(item) # appending student data
                # iterating through student data list
                for each in student_data:
                    student_split_list = each.strip("\n").split(";;;")
                    id_in_text = int(student_split_list[0]) # splitting id
                    if int(id) == id_in_text: # matching id
                        # creating matched student object
                        student_obj = Student(int(student_split_list[0]), student_split_list[1],
                                                student_split_list[2], student_split_list[3],
                                                student_split_list[4], student_split_list[5])
                        # returning student object
                        return student_obj
        except:
            return "No student data found!"

    # This method will delete the student data from the user file using id
    def delete_student_by_id(self, id):
        try:
            data_list = [] # list to store all lines from the  user file
            is_deleted = False
            # reading
            with open("./data/user.txt", "r+", encoding="utf-8") as user_file:
                user_data = user_file.readlines()
                for item in user_data:
                    split_list = item.strip("\n").split(";;;")
                    if split_list[4] == "student": # splitting students from the user text file
                        student_split_list = item.split(";;;")
                        id_in_text = int(student_split_list[0]) # matching id
                        if int(id) == id_in_text: # if id matched then removing the student data
                            user_data.remove(item)
                            is_deleted = True
                            break
                    else:
                        data_list.append(item) # if not found appending it again

            # writing the modified user data to the user file
            with open("./data/user.txt", "w+", encoding="utf-8") as user_file:
                for line in data_list:
                    user_file.write(line)

            # returns boolean
            return is_deleted

        except:
            return "No student record found!"


