import datetime
import mysql.connector as sqlconnector


connection = sqlconnector.connect(
    host = "localhost",
    user = "root",
    password = "6454",
    database  = "todo"
    )
connection.autocommit = True
C = connection.cursor(buffered = True)


def selection(question):
    select = input("{}  (y/n) : ".format(question))
    if(select.lower() == 'y'):
        return True
    elif select.lower() == 'n':
        return False
    else:
        selection(question)

def createtask():
    task = input(" \nEnter a task : ")
    select = selection("Do you want to set this [task] for today : ")
    if(select):
        global date
        date = str(datetime.date.today())
    else:
        date = input(" Completion date (Eg: 2012-01-28) [YYYY-MM-DD]: ")
    
    queryCreateTask = ("INSERT INTO todo.list(tdate,ttask)"
    " values('{}','{}')").format(date,task)
    
    C.execute(queryCreateTask)
    print("\n Task created Successfully ")

def changestatus():
    option = selection("Do u want to mark a task completed ? :")
    if(option):
        tnumber= int(input("Enter the task number :"))
        tid = listtasks()[tnumber][0]
        query = ("UPDATE todo.list set tstatus ='Completed' where tid = {};").format(tid)
        C.execute(query)
        
def listtasks():
    queryListAllTasks = "SELECT * FROM todo.list ORDER BY tdate"

    C.execute(queryListAllTasks)
    return C.fetchall()

def printtasks():
    print("\n")
    tasks = listtasks()
    if(len(tasks) == 0):
        print("\n No tasks found . Try creating a new Task from main menu :)")
    else:
        for task in enumerate(tasks):
            print("["+str(task[0]) + "] ->  "+ str(task[1][1])+ " " + task[1][2]+ "  (" + task[1][3] + ")")

def deletetask():
    printtasks()
    option = int(input("\nEnter a task number to delte : "))
    tid = listtasks()[option][0]

    queryDeleteATask = "DELETE FROM todo.list WHERE tid = {}".format(tid)
    C.execute(queryDeleteATask)

def deletealltasks():
    selected = selection("\nDo you really want to delete all the tasks ? :( ")
    if(selected):
        queryDeleteAllTasks = "DELETE FROM todo.list WHERE tid > 0 "
        C.execute(queryDeleteAllTasks)
    else:
        print("\nTask cancelled successfully ")
    


def mainmenu():
    print("****************************************************")
    print("****************************************************")
    print("****************      WEL COME      ****************")
    print("*************   ->Homework Todo App <-   ************")
    print("****************************************************")
    
    while True:
        print("\n")
        options = [" Create a task",
        " View all tasks",
        " Delete a task",
        " Delete all Tasks",
        " Exit"]
        for i in enumerate(options):
            print("[" + str(i[0] + 1)+ "]" + i[1])
        selectedoption = str(input(" Choose an option : "))
        if(selectedoption == "1"):
            createtask()
        elif(selectedoption == "2"):
            printtasks()
            changestatus()
        elif(selectedoption == "3"):
            deletetask()
        elif(selectedoption == "4"):
            deletealltasks()
        elif(selectedoption == "5"):
            quit()
        else:
            print(" Input a valid option")
mainmenu()