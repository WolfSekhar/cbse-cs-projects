import mysql.connector as sql
from mysql.connector import errorcode

database = "studentdb"
tablename = 'student'
createtablequery = 'create table studentdb.student (name varchar(30),roll int primary key)'

def createdb(cr, database):
    try:
        cr.execute("CREATE DATABASE {}".format(database))
    except sql.Error as e:
        print(e)

def checkdb():
    try:
        cr.execute("USE {}".format(database))
    except sql.Error as e:
        if(e.errno == errorcode.ER_BAD_DB_ERROR):
            createdb(cr, database)
        else:
            print(e)

def createtable(query):
    try:
        cr.execute(query)
    except sql.Error as error:
        print(error)

def checktable(tablename, query):
    try:
        cr.execute("DESC studentdb.{};".format(tablename))
    except sql.Error as e:
        if(e.errno == 1146):
            createtable(query)
            print("Table {} created".format(tablename))

try:
    global connection, cr
    connection=sql.connect(
        user = 'root', password = '6454', host = 'localhost')
    connection.autocommit=True
    cr=connection.cursor(buffered = True)
    checkdb()
    checktable(tablename,createtablequery)
except sql.Error as e:
    print(e)


def size(list):
    return len(list)

def isEmpty(list):
    return size(list) == 0 

def push(list,item):
    list.append(item)

def pop(list):
    if(not isEmpty(list)):
        list.pop(len(list) - 1)

def display(list):
    if(not isEmpty(list)):
        for i in list[::-1]:
            print(i)


def selection(question):
    select = input("{}  (y/n) : ".format(question))
    if(select.lower() == 'y'):
        return True
    elif select.lower() == 'n':
        return False
    else:
        selection(question)

def viewstudents():
    cr.execute("select * from studentdb.student")
    studentlist = cr.fetchall()
    if isEmpty(studentlist):
        print("No students available ")
    else:
        for item in enumerate(studentlist):
            print(str(item[0]) + ". " + item[1][0]  + " Rollnumber : " + str(item[1][1]))

def addstudent():
    name = input("Enter name : ")
    rollnumber = input("Enter roll number : ")
    query = "insert into studentdb.student(name,roll) values ('{}',{})".format(name,rollnumber)
    cr.execute(query)
    print("Student {} added successfully ".format(name))

def removestudent():
    viewstudents()
    option = input("Enter roll number to remove : ")
    select = selection("Do you really want to remove ? ")
    if(select):
        query = "delete from studentdb.student where roll='{}'".format(option)
        cr.execute(query)
        print("Student name removed succesfully")
    else:
        print("Operation Terminated")
def mainmenu():
    while True:
        print('''
        ---------------------------------------------------------------------------------
        *********************************************************************************
        *************************** WELCOME TO STUDENT MANAGEMENT APP********************
        *********************************************************************************
        ---------------------------------------------------------------------------------
        1. View Students 
        2. Add Student 
        3. Remove a student 
        4. Quit
        
        
        ''')
        option  = input("Enter your choice : ")
        if(option == "1"):
            viewstudents()
        elif option == "2":
            addstudent()
        elif option == "3":
            removestudent()
        else:
            quit()
        
mainmenu()
