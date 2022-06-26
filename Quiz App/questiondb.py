import mysql.connector as sql
from mysql.connector import errorcode


database = "quiz"
tablequestions = "question"
tableanswers = 'answer'

createquestiontablequery = ("create table {}.{}("
"quid int primary key,"
"question varchar(100) NOT NULL,"
"ans int NOT NULL"
")".format(database,tablequestions))
createanswertablequery = ("create table {}.{}("
"quid int primary key,"
"o1 varchar(40) NOT NULL,"
"o2 varchar(40) NOT NULL,"
"o3 varchar(40) NOT NULL,"
"o4 varchar(40) NOT NULL"
")".format(database,tableanswers))

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
        cr.execute("DESC {}.{};".format(database,tablename))
    except sql.Error as e:
        if(e.errno == 1146):
            createtable(query)
            print("Table {} created".format(tablename))

def insertquizdata():
    queryq = ("insert into {}.{}(quid,question,ans) values "
    "(1,'Who developed Python Programming Language?',3),"
    "(2,'Which type of Programming does Python support?',4),"
    "(3,'Is Python case sensitive when dealing with identifiers?',2),"
    "(4,'Which of the following is the correct extension of the Python file?',3),"
    "(5,'What will be the value of the following Python expression? 3 * 4 - 5',1)".format(database,tablequestions))
    querya = ("insert into {}.{}(quid,o1,o2,o3,o4) values "
    "(1,'Wick van Rossum','Rasmus Lerdorf','Guido van Rossum','Niene Stom'),"
    "(2,'object orineted','structural','functional','all of the above'),"
    "(3,'no','yes','machine dependent','none of the above'),"
    "(4,'.python','.p','.py','.pl'),"
    "(5,'7','4','3','2')".format(database,tableanswers))

    cr.execute(queryq)
    cr.execute(querya)

try:
    global connection, cr
    connection=sql.connect(
        user = 'root', password = '6454', host = 'localhost')
    connection.autocommit=True
    cr=connection.cursor(buffered = True)
    checkdb()
    checktable(tablequestions,createquestiontablequery)
    checktable(tableanswers,createanswertablequery)
    insertquizdata()

except sql.Error as e:
    print(e)