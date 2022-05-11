# importing other classes
from User import User
from Admin import Admin
from Instructor import Instructor
from Student import Student

# printing the menu
def show_menu():
    print("1. EXTRACT_DATA")
    print("2. VIEW_COURSES")
    print("3. VIEW_USERS")
    print("4. VIEW_REVIEWS")
    print("5. REMOVE_DATA")

# Controls the whole program
def process_operations(user_object):
    # logged_out is used to log out the user
    logged_out = False
    # if the user_object type is admin then executing the below
    if type(user_object) is Admin:
        # looping until log out
        while not logged_out:
            print("Please enter admin command for further service:")
            # printing menu
            show_menu()
            # getting input for the operations
            user_command = input()
            # splitting the [0] element as choice
            choice = user_command.split(" ")[0]
            # if choice 1 then calling the extract_info method from Admin class to extract all the data
            if choice == "1":
                user_object.extract_info()

            # choice 2 will print the requested course using the keyword and value
            elif choice == "2":
                # if no keyword and value passed then printing the total number of courses
                if len(user_command.split(" ")) == 1:
                    user_object.view_courses()
                # if argument passed then printing the  matched courses
                elif len(user_command.split(" ")) > 1:
                    keyword = user_command.split(" ")[1]
                    if len(keyword) != 0:
                        value = user_command.split(" ")[2].replace("\n", "")
                        user_args = [keyword, value]
                        user_object.view_courses(user_args)

            # choice 3 will print the total number of users
            elif choice == "3":
                user_object.view_users()

            # choice 4 will print the requested review using the keyword and value
            elif choice == "4":
                # if no args then printing the total no of reviews
                if len(user_command.split(" ")) == 1:
                    user_object.view_reviews()
                # if args passed printing the matched reviews
                elif len(user_command.split(" ")) > 1:
                    keyword = user_command.split(" ")[1]
                    if len(keyword) != 0:
                        value = user_command.split(" ")[2].replace("\n", "")
                        user_args = [keyword, value]
                        user_object.view_reviews(user_args)

            #  choice 5 will remove all writen data from the files by calling remove_data method from Admin class
            elif choice == "5":
                user_object.remove_data()

            #if the user entered logout or Logout then the user will be logged out.
            elif choice == "logout" or "Logout":
                print("Successfully logged out!")
                logged_out = True
                break

            # error message
            else:
                print("Enter valid choice!")

    # if the user_object type is admin then executing the below
    elif type(user_object) is Instructor:
        # looping until log out
        while not logged_out:
            print("Please enter instructor command for further service:")
            # printing menu and getting input for the operations
            show_menu()
            user_command = input()
            choice = user_command.split(" ")[0]

            # if choice 1 then calling the extract_info method from Instructor class to print not allowed message
            if choice == "1":
                user_object.extract_info()

            # choice 2 will print the course taught by this instructor
            elif choice == "2":
                if len(user_command.split(" ")) == 1:
                    user_object.view_courses()

                elif len(user_command.split(" ")) > 1:
                    print("No arguments are allowed!")

            # choice 3 will print not allowed message
            elif choice == "3":
                user_object.view_users()

            # choice 4 will print the reviews of the courses taught by this instructor
            elif choice == "4":
                if len(user_command.split(" ")) == 1:
                    user_object.view_reviews()

                elif len(user_command.split(" ")) > 1:
                    print("No arguments are allowed!")

            # choice 5 will print not allowed message
            elif choice == "5":
                user_object.remove_data()

            # if the user entered logout or Logout then the user will be logged out.
            elif choice == "logout" or "Logout":
                print("Successfully logged out!")
                logged_out = True
                break

            # error message
            else:
                print("Enter a valid choice!")

    elif type(user_object) is Student:
        # looping until logged out
        while not logged_out:
            print("Please enter student command for further service:")
            # printing menu and getting input
            show_menu()
            user_command = input()
            choice = user_command.split(" ")[0]

            # if choice 1 then printing not allowed message
            if choice == "1":
                user_object.extract_info()
            # this will print the courses enrolled by this student
            elif choice == "2":
                if len(user_command.split(" ")) == 1:
                    user_object.view_courses()

                elif len(user_command.split(" ")) > 1:
                    print("No arguments are allowed!")

            # if choice 3 then printing not allowed message
            elif choice == "3":
                user_object.view_users()

            # this will print the reviews posted by this student
            elif choice == "4":
                if len(user_command.split(" ")) == 1:
                    user_object.view_reviews()

                elif len(user_command.split(" ")) > 1:
                    print("No arguments are allowed!")

            # if choice 5 then printing not allowed message
            elif choice == "5":
                user_object.remove_data()

            # if the user entered logout or Logout then the user will be logged out.
            elif choice == "logout" or "Logout":
                print("Successfully logged out!")
                logged_out = True
                break

            # error message
            else:
                print("Enter a valid choice!")

# main method
def main():
    # is_exit used to exit the program
    is_exit = False
    # loopting until exit
    while not is_exit:
        # asking username and password
        user_input = input("Please input username and password to login:(format username password)\n")
        if len(user_input.split(" ")) == 1:
            # if it is exit then exit the code
            if user_input == "exit":
                print("Program exited!")
                is_exit = True
                exit()
            # if value is not valid then printing the message
            else:
                print("Enter valid username and password")
        # if empty printing message
        elif len(user_input.split(" ")) == 0:
            print("Enter valid username and password")

        # if valid values then doing the following
        else:
            input_username = user_input.split(" ")[0]
            input_password = user_input.split(" ")[1].replace("\n", "")
            temp_user = User(username=input_username, password=input_password)
            # creating a temp user to perform login to match his / her role
            login_result = temp_user.login()

            # if login failed printing message
            if login_result == False:
                print("Login failed!")
                print("Username or Password incorrect!")

            # if login is true
            else:
                if login_result[0] == True:
                    # for admin
                    if login_result[1] == "Admin":
                        user_object = Admin()
                        print("Admin login successful")
                        print("Welcome " + input_username + ". Your role is Admin.")
                        process_operations(user_object)

                    # for instructor
                    elif login_result[1] == "Instructor":
                        user_object = Instructor(username=input_username)
                        print("Instructor login successful")
                        print("Welcome " + input_username + ". Your role is Instructor.")
                        process_operations(user_object)

                    # for student
                    elif login_result[1] == "Student":
                        user_object = Student(username= input_username)
                        print("Student login successful")
                        print("Welcome " + input_username + ". Your role is student.")
                        process_operations(user_object)

                    # message for wrong input
                    else:
                        print("Input does not match with the records!")



# executing the main
if __name__ == "__main__":

    # print a welcome message
    print("Welcome to our system")

    # manually register admin
    temp_admin = Admin(username= "admin", password= "admin")
    temp_admin.register_admin()

    main()
