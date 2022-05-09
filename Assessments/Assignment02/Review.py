class Review:

    def __init__(self, id = -1, content = "", rating = -1.0, course_id = -1):
        self.id = id
        self.content = content
        self.rating = rating
        self.course_id = course_id

    def find_review_by_id(self, review_id):
        with open("./data/result/review.txt", "r") as review_doc:
            review_data = review_doc.readlines()
            for line in review_data:
                review_id_in_doc = line.split(";;;")[0]
                if str(review_id) == review_id_in_doc:
                    review = line
                    break
                else:
                    review = None
        print(review)
        return review

    def find_review_by_keywords(self, keyword):
        review = []
        if len(keyword) > 0:
            with open("./data/result/review.txt", "r") as review_doc:
                review_data = review_doc.readlines()
                for line in review_data:
                    description = line.split(";;;")[1].lower()
                    if keyword in description:
                        review.append(line)
        else:
            print("Keyword cannot be empty!")

        return review

    def find_review_by_course_id(self, course_id):
        pass


review = Review()
# review.find_review_by_id(24238)
review.find_review_by_keywords("")