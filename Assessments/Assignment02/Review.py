# Review class will find the review by using id, keyword and course id
class Review:
    #constructors
    def __init__(self, id = -1, content = "", rating = -1.0, course_id = -1):
        self.id = id
        self.content = content
        self.rating = rating
        self.course_id = course_id

    #find review_by_id function will return the corresponding review as review object
    def find_review_by_id(self, review_id):
        # opening the file to read
        with open("./data/result/review.txt", "r") as review_doc:
            review_data = review_doc.readlines()
            for line in review_data:
                # splitting the review ids in the doc
                review_id_in_doc = line.split(";;;")[0]
                # matching the review id provided with the id in the text file
                if str(review_id) == review_id_in_doc:
                    id = review_id_in_doc
                    content = line.split(";;;")[1]
                    rating = line.split(";;;")[2]
                    course_id = line.split(";;;")[3].replace("\n", "")
                    # if match found then returning the values as Review object
                    review = Review(int(id), content, float(rating), int(course_id))
                    break
                else:
                    review = None

        return review

    # find review_by_keyword function will return the corresponding review as review object
    def find_review_by_keywords(self, keyword):
        #creating an empty review list to append the matched review objects
        review = []
        # validating the keyword is not empty
        if len(keyword) > 0:
            # opening the file to read
            with open("./data/result/review.txt", "r") as review_doc:
                review_data = review_doc.readlines()
                for line in review_data:
                    content = line.split(";;;")[1].lower()
                    # matching the keyword with the review content of the review text file
                    if keyword in content:
                        id = line.split(";;;")[0]
                        content = line.split(";;;")[1]
                        rating = line.split(";;;")[2].replace(";", "")
                        course_id = line.split(";;;")[3].replace("\n", "")
                        # match founded then appending the object to the review list.
                        review.append(Review(int(id), content, float(rating), int(course_id)))

        # if keyword is empty printing the message
        else:
            print("Keyword cannot be empty!")
        # returning the review list
        return review

    # This function will return the reviews matched with the course_id
    def find_review_by_course_id(self, course_id):
        # creating empty list to append the match later
        review = []
        file_creation = open("./data/result/review.txt", "a+")
        file_creation.close()
        with open("./data/result/review.txt", "r") as review_doc:
            review_data = review_doc.readlines()
            for line in review_data:
                # splitting doc course ids from each line in review text file
                doc_course_ids = line.split(";;;")[-1].replace("\n", "")
                # if match found then appending the review object to the review list
                if str(course_id) == doc_course_ids:
                    id = line.split(";;;")[0]
                    content = line.split(";;;")[1]
                    rating = float(line.split(";;;")[2].replace(";", ""))
                    course_id = line.split(";;;")[3].replace("\n", "")
                    review.append(Review(int(id), content, rating, int(course_id)))
        # returning the review list if no match found then the list will be empty
        return review

    # review overview method will print the total review lines
    def reviews_overview(self):
        with open("./data/result/review.txt", "r") as review_doc:
            review_data = review_doc.readlines()
            total_lines = len(review_data)
            return total_lines

    # formating the review object and returning
    def __str__(self):
        review_format = str(self.id) + ";;;" + self.content + ";;;" + str(self.rating) + ";;;" + str(self.course_id)
        return review_format

