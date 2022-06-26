import mysql.connector as sql
from mysql.connector import errorcode


database = "train"
traindetails = "traindetails"
ticketrecords = "ticketrecords"

traindetailsquery = ("CREATE TABLE {}.{}("
    "trainnumber char(6) PRIMARY KEY,"
    "ffrom varchar(20),"
    "fto varchar(20),"
    "departuretime TIME(0),"
    "platform char(2))").format(database,traindetails)
ticketrecordsquery=("CREATE TABLE {}.{}("
    "ticketnumber char(20) PRIMARY KEY,"
    "coachtype char(8) NOT NULL DEFAULT 'GEN',"
    "traindate date NOT NULL,"
    "seatnumber INT NOT NULL,"
    "trainnumber char(5) NOT NULL,"
    "pname varchar(30) NOT NULL"
    ")").format(database,ticketrecords)


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

def inserttraindata():
    query = ("INSERT INTO {}.{}(trainnumber,ffrom,fto,departuretime,platform)"
    "values"
    "('52111','BBSR','Jeypore','02:30:00','5'),"
    "('95684','Mumbai','Chennai','15:40:00','3'),"
    "('63952','Delhi','Bengaluru','22:30:00','8'),"
    "('85111','Hyderabad','Ahmedabad','14:20:00','6'),"
    "('23222','Luknow','Mangluru','06:30:00','5'),"
    "('45125','Bhopal','Bikaner','22:33:00','7'),"
    "('96568','Kochi','Aurangabad','21:45:00','5'),"
    "('25985','Darjelling','Dehradun','21:30:00','4'),"
    "('88645','Diu','Nasik','13:30:00','7'),"
    "('36785','Gaya','Mysore','01:10:00','3')").format(database,traindetails)
    try:
        cr.execute(query)
        print("Train Data Insertion successful")
    except sql.Error as error:
        print("From data insertion " + str(error))
try:
    global connection, cr
    connection=sql.connect(
        user = 'root', password = '6454', host = 'localhost')
    connection.autocommit=True
    cr=connection.cursor(buffered = True)
    checkdb()
    checktable(traindetails,traindetailsquery)
    checktable(ticketrecords,ticketrecordsquery)
    inserttraindata()
    
except sql.Error as e:
    print(e)
cr.close()
