#importing other classes
from User import User
from Course import Course
from Review import Review

# student class will print the courses enrolled by the student and reviews posted by the student
class Student(User):

    # constructor
    def __init__(self, id=-1, username="", password="", user_title="", user_image_50x50="", user_initials="",
                 review_id=-1):
        super().__init__(id, username, password)
        self.id = id
        self.username = username
        self.password = password
        self.user_title = user_title
        self.user_image_50x50 = user_image_50x50
        self.user_initials = user_initials
        self.review_id = review_id

    # This method will print the course enrolled by the student.
    def view_courses(self, args = []):
        # empty course id string
        course_id = ""
        # opening the student text to read lines
        with open("./data/result/user_student.txt", "r") as student_doc:
            student_details = student_doc.readlines()
            for each in student_details:
                # splitting the username and id of the students from the text file
                stud_username = each.split(";;;")[1]
                student_id_in_doc = each.split(";;;")[0]
                # if the  self.username and username in the doc are matching then assigning the self.id to the id in doc
                if self.username == stud_username:
                    self.id = student_id_in_doc
                # matching self.id to the student id in the doc if match found then taking the review_id
                if str(self.id) == student_id_in_doc:
                    review_id = each.split(";;;")[-1].replace("\n","")

            # opening the review text to match the courses
            with open("./data/result/review.txt", "r") as review_doc:
                review_data = review_doc.readlines()
                for line in review_data:
                    review_id_in_doc = line.split(";;;")[0]
                    #  matching the review id taken above with the review ids in the doc
                    if review_id == review_id_in_doc:
                        temp_course_id = line.split(";;;")[-1].replace("\n", "")
                        # concatenating the matched course id
                        course_id += temp_course_id
        # finding the course using the course id found above
        course_details = Course.find_course_by_id(self,course_id)
        print(course_details)

    # This method will print the reviews wrote by the student
    def view_reviews(self, args = []):
        # opening the student text to read lines
        with open("./data/result/user_student.txt", "r") as student_doc:
            student_details = student_doc.readlines()
            for each in student_details:
                student_id_in_doc = each.split(";;;")[0]
                stud_username = each.split(";;;")[1]
                # if the self.username matches with the student username in the file assigning the id to self.id
                if self.username == stud_username:
                    self.id = student_id_in_doc
                # if the self.id is matching with stud id in the docs splitting the review id to find the review
                if str(self.id) == student_id_in_doc:
                    review_id = each.split(";;;")[-1].replace("\n","")
            # using review id calling the find_review_by_id function from Review class to print the review
            review = Review.find_review_by_id(self, review_id)
            print(review)

    # These methods will print not allowed message, inherited from User class.
    def extract_info(self):
        super(Student, self).extract_info()

    def view_users(self):
        super(Student, self).view_users()

    def remove_data(self):
        super(Student, self).remove_data()

    # return str method formats the output as shown below
    def __str__(self):
        student_format = str(self.id) + ";;;" + self.username + ";;;" + self.password + ";;;" + self.user_title + ";;;" \
                         + self.user_image_50x50 + ";;;" + self.user_initials + ";;;" + str(self.review_id)

        return User.__str__(student_format)

