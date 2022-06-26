import mysql.connector as sql
from mysql.connector import errorcode
import random

database = "bank"
tablename = "account"
createtablequery = ("create table bank.account("
"accountnumber char(6) PRIMARY KEY,"
"aname varchar(30) NOT NULL,"
"balance int default 0,"
"password varchar(50) NOT NULL"
")")

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
        cr.execute("DESC bank.{};".format(tablename))
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

def generate_accountnumber():
    acno = ""
    alphaDigit = ["a","b","c","g","e","h",'I',"j","k","l","m","n",1,2,3,4,5,6,7,8,9,0]
    for i in range(6):
        n = random.randint(0,len(alphaDigit)-1)
        acno  = acno + str(alphaDigit[n])
    return acno


def user(accno):
    query = ("select accountnumber from bank.account where accountnumber='{}'").format(accno)
    cr.execute(query)
    if(cr.fetchone()[0]==0):
        return False
    else:
        return True

def selection(question):
    select = input("{}  (y/n) : ".format(question))
    if(select.lower() == 'y'):
        return True
    elif select.lower() == 'n':
        return False
    else:
        selection(question)

def balancedebit(amount,price,ac):
    amount -= price
    query = ("UPDATE bank.account set balance='{}' where accountnumber='{}'").format(amount,ac)
    cr.execute(query)
    print("\n Amount changed successfully ")
    
def balancecredit(amount,price,ac):
    amount += price
    query = ("UPDATE bank.account set balance='{}' where accountnumber='{}'").format(amount,ac)
    cr.execute(query)
    print("\n Amount changed successfully ")

def login(username,password):
    query = "select password from bank.account where accountnumber='{}'".format(username)
    query2 = "select aname,balance from bank.account where accountnumber='{}'".format(username)
    cr.execute(query)
    if(cr.fetchone()[0]==password):
        print("\nLogin successful")
        while True:
            cr.execute(query2)
            data = cr.fetchall()
            print("\n ************* Welcome " + str(data[0][0]) + "*************")
            print("Account Number : " + username)
            print("Balance : " + str(data[0][1]))
            option = selection("\nDo you want to debit or credit money ?")
            if(option == True):
                select = input(" 1. Debit \n 2. Credit \n 3. exit \n :-- > ")
                price = int(input("Enter amaount : "))
                if(select == "1"):
                    balancedebit(data[0][1],price,username)
                elif(select == "2"):
                    balancecredit(data[0][1],price,username)
                else:
                    break
            else:
                break

def register():
    name = input("Enter name: ")
    password = input("Enter password : ")
    amount = int(input("enter amount to deposit: "))
    accountnumber = generate_accountnumber()
    query = ("insert into bank.account(accountnumber,aname,balance,password) values "
    "('{}','{}','{}','{}')").format(accountnumber,name,amount,password)
    cr.execute(query)
    print("\nAccount Created successfully with accoun number : {} and password : {}".format(accountnumber,password))

def mainmenu():

    mainoptions = ["login","Create account","exit"]
    
    
    while True:
        print("\n")
        for item in enumerate(mainoptions):
            print(str(item[0] + 1) + ". " + item[1])

        option = input("Enter your choice : ")
        if(option == "1"):
            username = input("account number: ")
            password = input("password : ")
            if(user(username)):
                login(username,password)
            else:
                print("\n Account not available . Try creating one ")
        elif(option == "2"):
            register()

        elif(option == "3"):
            quit()
        else:
            print("Entered option in invalid")

mainmenu()