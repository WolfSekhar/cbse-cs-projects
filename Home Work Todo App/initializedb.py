import mysql.connector as sqlconnector
from mysql.connector import errorcode
connection = sqlconnector.connect(
    host = "localhost",
    user = "root",
    password = "6454"
    )
connection.autocommit = True
C = connection.cursor()

database = "todo"
table = "list"

query = ('create table todo.list('
    'tid INT PRIMARY Key AUTO_INCREMENT,'
    'tdate DATE NOT NULL,'
    'ttask varchar(200) NOT NULL,'
    'tstatus char(15) DEFAULT "pending")')



def createdb(C, database):
    try:
        C.execute("CREATE DATABASE {}".format(database))
        print("Database todo Created :)")
    except sqlconnector.Error as e:
        print(e)


def checkdb():
    try:
        C.execute("USE {}".format(database))
    except sqlconnector.Error as e:
        if(e.errno == errorcode.ER_BAD_DB_ERROR):
            createdb(C, database)
        else:
            print(e)

def createtable(query):
    try:
        C.execute(query)
    except sqlconnector.Error as error:
        print(error)

def checktable(tablename, query):
    try:
        C.execute("DESC {}.{};".format(database,tablename))
    except sqlconnector.Error as e:
        if(e.errno == 1146):
            createtable(query)
            print("Table {} created".format(tablename))

checkdb()
checktable(table,query)