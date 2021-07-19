
#importing date and time 
# importing the current date, to display when the task was assigned. online resource: https://www.w3schools.com/python/python_datetime.asp 
import datetime

#opening user.txt for reading 
with open("user.txt","r") as userfile:
    userfile = userfile.read()


menu ="\nPlease select one of the following options:\nr: register user\na: add task\nva: view all tasks\nvm: view my tasks\nds: display statistics\ngr: generate reports\ne: exit"
menu1 = "\nPlease select one of the following options:\na: add task\nva: view all tasks\nvm: view my tasks\ne: exit  "

#while loop requesting username and password inputs from the user  
while True:
    user_name = input("Enter your username: ")
    pass_word = input("Enter your password: ")
    
 #if statement that displays the admin menu if their log in details match that of the admin.  
    if user_name == "admin" and pass_word == "adm1n":
        print("You are logged in as 'admin'")
        print(menu)
        break
       
 #if/else the general user menu is diplayed if the username and password are found in the user.txt file.
    elif user_name in userfile and pass_word in userfile:
        print("You are logged in")
        print(menu1)
        break
    

 #else if the login details are not found in the userfile anywhere, an error message is displayed and the loop will prompt the user to enter their details again
    else:
        print("invalid login details")


###
#Defining / creating Functions:  
#the below functions, except for generate reports are basically just ports from the orginal conditional statements from the first part of this capstone. 

#Register user function: 
def reg_user(): 
    with open("user.txt","r") as userfile:
        userfile = userfile.read()
        valid = False 
        while valid == False: 
            username = input("Enter a new username: ")
            
            if username in userfile: 
                print("User already exists. Please check your entry")
                valid = False
            else: 
                password = input("Enter a password for the new user: ")
                password_confirm = input("Confirm password: ")
                
            if password != password_confirm:
                print("Passwords do not match")
                password = input("Enter a password for the new user: ")
                password_confirm = input("Confirm password: ")

            if password_confirm == password:
                with open("user.txt","a+") as userfile:
                    userfile.write("\n{}, {}".format(username, password_confirm))
                    print("New user registered")
                    valid = True

#Add task function:                 
def add_task(): 
    task_user = input("Enter the user to assign the task to: ")
    task_name = input("Enter the task name: ")
    task_description = input("Enter task description: ")
    task_date = input("Enter task due date in the following numerical fromat; ('Year-month-day'): ")
    task_status = "No" 

    assign_date = date.today().strftime('%Y-%m-%d')
        
    #opening tasks.txt with "a+" so that it can be read, and written to wihtout worry of it being overwritten. 
    with open("tasks.txt","a+") as userfile:  
        userfile.write("\n{}, {}, {}, {}, {}, No".format(task_user, task_name, task_description, assign_date, task_date ))
        print("Task added")

#View all tasks function:
def view_all(): 
    with open("tasks.txt","r") as taskfile:
            task_data = taskfile.readlines()
            for line in task_data:
                task_data = line.split(", ")
                print(f"""
User:               {task_data[0]}
Task name:          {task_data[1]}
Task descritpion:   {task_data[2]}
Date assigned:      {task_data[3]}
Due date:           {task_data[4]} 
Complete?:          {task_data[5]}
""")

#View my task function: 
def view_mine(user_name):
    #creating blank list to append "count" to track the actual index of a task in the file - for later editing.. 
    # the '-1' is to account for the loop iterations so that first line becomes index[0]
    real_task_indexes=[]
    with open("tasks.txt","r") as taskfile:
            all_tasks = taskfile.readlines() 
            count = -1
            #displayed count is what will be displayed alongside the users individual tasks. 
            displayed_count = 0
            for task in all_tasks:
                count += 1
                #following the smae logic from view_all, the data read from the file is then split so that it can be printed in a readble format. 
                data_temp = task.split(", ")
                if user_name == data_temp[0]:
                    displayed_count += 1
                    real_task_indexes.append(count)
                    print(f"""Task no. {displayed_count}: 
User:               {data_temp[0]}
Task name:          {data_temp[1]}
Task descritpion:   {data_temp[2]}
Date assigned:      {data_temp[3]}
Due date:           {data_temp[4]} 
Complete?:          {data_temp[5]}
""")

    option = int(input("To select a task to edit, enter its corresponding number,\nor enter ('-1') to return to the menu: ")) 

    if option == "-1" and user_name != "admin": 
        print(menu1)
        return
    if option == "-1" and user_name == "admin": 
        print(menu)
        return
    else:
        #if a user selects a task, the displayed task number simply equals what they have entered,
        #  and the real_task_index within the user's individual tasks becomes dispalyed_count minus 1. 
        displayed_task_num = int(option)
        real_task_index = real_task_indexes[displayed_task_num - 1]
        if "Yes" in all_tasks[real_task_index]:
            print("This task has already been completed. Please check your selection")
            option = int(input("To select a task to edit enter its corresponding number,\n or enter ('-1') to return to the menu: ")) 
        else:
            option2 = input("To mark the task complete enter ('c')\nor to edit the username or due date, enter ('e')\nselection: ")
            if option2 == "c": 
                all_tasks[real_task_index] = all_tasks[real_task_index].replace("No","Yes")

            elif option2 == "e":  
                new_name = input("Enter the new username: ") 
                new_date = input("Enter a new due date: ")

                broken_up_task = all_tasks[real_task_index].split(', ')

                all_tasks[real_task_index] = f"{new_name}, {broken_up_task[1]}, {broken_up_task[2]}, {broken_up_task[3]}, {new_date}, {broken_up_task[5]}"

                print(all_tasks[real_task_index])

                #Below, .writelines is used as this is the only format of the write function that correctly allows for the all_tasks data to overwrite the file in the correct way
                #  to produce the desired output. 
                with open("tasks.txt","w") as f: 
                    f.writelines(all_tasks)

                return
                

def generate_reports(user_name):
        #reading in each line from the file as task_report_data 
        with open("tasks.txt","r") as f:
            task_report_data = f.readlines()
            #declaring count variables
            total_complete = 0 
            incomplete = 0 
            overdue = 0
            total_num_tasks = len(task_report_data)

            #for loop that breaks every line in "task_report_data" into "temp_data" which can be indexed - splitting the lines and the information into individual components.
            for i in task_report_data: 
                temp_data = i.split(", ")
                #if "Yes" appears in the 5th index (which is the "completed" status) the complete counter will be added to. 
                if "Yes" in temp_data[5]:
                    total_complete += 1
                if "No" in temp_data[5]: 
                    incomplete += 1 

                    #manipulating the current due date so that it can be numerically compared to the present date. 
                    #Online resources: https://www.programiz.com/python-programming/datetime/strptime ,
                    #  https://www.kite.com/python/answers/how-to-compare-two-dates-with-datetime-in-python 

                    # strptime is a built in python function which takes 2 arguments; a date or string, 
                    # and the format that the outputted datetime object will take. 
                    # The format codes used below can be found at: https://www.w3schools.com/python/python_datetime.asp 

                    # I experuimented with .now and strftime, but the version below seems to be the only correct way to reformat the data. 
                    # hardcoding the original task file was needed to change the dates so that they all followed the same format

                    comparrison_date = datetime.datetime.strptime(temp_data[4], "%Y-%m-%d") 
                    current_date = datetime.datetime.today()
                    if comparrison_date < current_date : 
                        overdue += 1 
 
                    #dividing the calcualtion's by 1 at the end removes unnessacry decimals at this stage of the code already. 
                    percentage_overdue = ((overdue/total_num_tasks)*100)/1
                    percentage_incomplete = ((incomplete/total_num_tasks)*100)/1
                    with open("task_overview.txt","w") as f: 
                        f.write(f"""Task overview report:\n\nTotal tasks: {total_num_tasks}\nCompleted tasks: {total_complete}
                        \nIncomplete tasks: {incomplete}\nOverdue tasks: {overdue}\nPercentage of tasks that are incomplete: %{round(percentage_incomplete,2)}
                        \nPercentage of taksks that are overdue: %{round(percentage_overdue,2)}""")

                    #reading in the user file and creating a blank list which will hold only the usernames and not passwords. 
                    with open("user.txt","r") as f2:
                        f2 = f2.readlines()
                        users = []
                        #the number of users crudely is equal to the length of the lines in the user file; 
                        num_of_users = len(f2)
                        #for every instance in f2, the line is bascially split by the comma to isolate the username from the password and this sis then appended to "users"
                        for i in f2: 
                            user_info = i.split(", ")
                            users.append(user_info[0])


                        
                        with open("user_overview.txt","w") as f3: 
                            #the below .write and fstring for the heading and the first statitistics is palced at the top
                            #  so that the loops used below wont repetadely show this information in the output file.
                            f3.write(f"\nUser overview report:\n\nNumber of users registered on the task manager: {num_of_users}\nTotal tasks assinged: {total_num_tasks}\n")
                            for i in users: #for every user in other words. 
                                individual_tasks = []
                                #opening the task file adn then appending every line from it to individual tasks where where i in users matches the first index in a task line.
                                with open("tasks.txt","r") as f:
                                    for line in f: 
                                        temp = line.split(", ")
                                        if temp[0] == i : 
                                            individual_tasks.append(line)
                                            individual_total = len(individual_tasks)  
                                    #declaring more variables 
                                    complete_individual = 0 
                                    overdue_individual = 0
                                    incomplete_indiviual = 0
                                    # now for every task in an individuals tasks: the lines are once again broken down using .split 
                                    # so that the completion and overdue status of each task can be compared to the "index variables"
                                    # that the task has been broken up into so to say. 
                                    for i in individual_tasks: 
                                        name, task, desc, assigned, due, status = i.split(", ")
                                        if "Yes" in status:
                                            complete_individual += 1
                                        if "No" in status: 
                                            incomplete_indiviual += 1 
                                            comparrison_date = datetime.datetime.strptime(due, "%Y-%m-%d") 
                                            current_date = datetime.datetime.today()
                                            if comparrison_date < current_date:
                                                overdue_individual += 1 

                                    assigned_percentage = ((individual_total / total_num_tasks)*100)/1
                                    complete_percent = ((complete_individual/individual_total)*100)/1
                                    incomplete_percent = ((incomplete_indiviual/individual_total)*100)/1
                                    overdue_percent = ((overdue_individual/individual_total)*100)/1

                                    f3.write(f"""\nUsername: {name}\nTasks assinged to user: {individual_total}
                                    \n\nPercentage of tasks assigned to this user: %{round(assigned_percentage,2)}\nPercentage completed: %{round(complete_percent,2)}
                                    \nPercentage incomplete: %{round(incomplete_percent,2)}\nPercentage of user's taks overdue: %{round(overdue_percent,2)}\n""")

            print("\nTask and user overview reports succesfully generated\n.")
                                        
        
#Inside the following while loop is a prompt to enter the menu selection, this is so that the user has an opportunity to continue to select actions from
#the menu if they want to perform subsequent operations in the task manager program after each conditional statment has run
#the loop will take the user back to the "select" input.  
#the if and elif statements which follow are to account for the different menu selections the user might make.    
# in each of the following conditonal statements pertaining to the user selection, a relevant fucntion is called, except when the user wants to display stats or exit the program.                 

while True :
    select = input("Enter your selection: ")
    # if statement that prevents a general user from selecting 'r' to register a user 
    if user_name != "admin" and select == "r":
        print("Invalid menu selection")
        break 

    if select == "r":
        reg_user()
                   
    elif select == "a": 
        add_task()
        
    
    #the elif statment below executes the following if the user chooses to view all tasks; 
    #tasks.txt is opened to read as "taskfile" - variable task_data is created and is created with the data read from every line in the text file 
    #the for loop esnures that every line in task_data is split so that each line becomes a list with indices. 
    #Due to how the tasks.txt file is formatted the same indices on each line correspond with the same descriptions, "user, task name" etc. and therefore,
    #for every line, the indices are printed which will accurately show the tasks. 

    elif select == "va": 
        view_all()

   #Below the same code is used to read from the tasks file, store the data in 'task_data' and split every line in 'task_data' into a list with indices.
   # if the user_name is equal to what is found in index[0] of a line, then every index in the line (or in the task) is printed.           

    elif select == "vm": 
        view_mine(user_name)
        
    #in the elif statement below, 2 variables are declared and initialized to zero, these will be used as counting variables. 
    # as the text files are formatted to hold only one task or one user's info per line, 
    # for loops can simply be used to add to the count variables for every line to coun the number of users and tasks respectively.                   

    elif select == "ds": 
        #if the admin selects "ds" this firts calls the fucntion to generate reports. These reports are them simply printed out as they contain the required stats. 
        generate_reports(user_name)
        with open("task_overview.txt","r") as f1: 
            f1 = f1.read()
            print(f1)
        with open("user_overview.txt","r") as f2: 
            f2 = f2.read()
            print(f2)
            
    elif select == "gr":
        generate_reports(user_name)
        
    #if option 'e' is selected the program will exit. online resource: https://www.askpython.com/python/examples/exit-a-python-program 
    elif select == "e": 
        exit()
