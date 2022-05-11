# importing classes
from User import User
from Course import Course
from Review import Review

# child class of User
# this class will print the courses taught by the instructor and reviews of the courses
class Instructor(User):

    # constructor
    def __init__(self, id=-1, username="", password="", display_name="", job_title="", image_100x100="",
                 course_id_list=[]):
        super().__init__(id, username, password)
        self.id = id
        self.username = username
        self.password = password
        self.display_name = display_name
        self.job_title = job_title
        self.image_100x100 = image_100x100
        self.course_id_list = course_id_list

    # this method will print the courses taught by the instructor
    def view_courses(self, args = []):
        # opening user_instructor.txt to read the lines
        with open("./data/result/user_instructor.txt", "r") as instructor_file:
            instructor_data = instructor_file.readlines()
            for each in instructor_data:
                inst_username = each.split(";;;")[1]
                inst_id = each.split(";;;")[0]
                # assigning the self.id if the seld.username matches with the username in the doc
                if self.username == inst_username:
                    self.id = inst_id
        # finding the course using find_course_by_instructor method from Course class by passing the self.id
        courses = Course.find_course_by_instructor_id(self, self.id)
        # if the lenght of the courses is greater than 10 we are printing 10 only else print everything
        if len(courses) > 10:
            for each in courses[:10]:
                print(each)
        else:
            for each in courses:
                print(each)

    # This method will print the review of the courses taught by the instructor
    def view_reviews(self, args = []):
        # opening the file to read lines
        with open("./data/result/user_instructor.txt", "r") as instructor_file:
            instructor_data = instructor_file.readlines()
            for each in instructor_data:
                inst_username = each.split(";;;")[1]
                inst_id = each.split(";;;")[0]
                # if the self.username matches with the username in docs then assigning the self.id to the id in doc
                if self.username == inst_username:
                    self.id = inst_id
        # using self.id calling the find_course_by_instructor_id method from course class to get the course id
        courses = Course.find_course_by_instructor_id(self, self.id)
        result = []
        for each in courses:
            # appending the matched course_id to the self.course_id_list
            self.course_id_list.append(each.course_id)
            # iterating through the self.course_id_list appended above
            for line in self.course_id_list:
                # calling the find_review_by_course_id method from the Review class to find the review using course id
                review = Review.find_review_by_course_id(self,line)
                for each in review:
                    # appending the matches to the result list.
                    result.append(each)
        # if matches are more than 10 we are printing only 10 otherwise print everything
        if len(result) > 10:
            sliced_list = result[0:10]
            for each in sliced_list:
                print(each)
            print("\nThe total reviews for the instructor are: ", len(result))

        else:
            for each in result:
                print(each)
            print("\nThe total reviews for the instructor are: ", len(result))

    # these methods are printing the not allowed message, all are inherited from the parent User class
    def extract_info(self):
        super(Instructor, self).extract_info()
    
    def view_users(self):
        super(Instructor, self).view_users()
        
    def remove_data(self):
        super(Instructor, self).remove_data()

    # str return function formats the output as shown below
    def __str__(self):
        instructor_format = ";;;" + self.display_name + ";;;" + self.job_title + ";;;" + self.image_100x100 \
                            + ";;;" + self.course_id_list
        return User.__str__(self) + instructor_format









