import mysql.connector as sql
from mysql.connector import errorcode


database = "flight"
flightdetails = "flightdetails"
ticketrecords = "ticketrecords"

flightdetailsquery = ("CREATE TABLE flight.flightdetails("
    "flightnumber char(6) PRIMARY KEY,"
    "companyname varchar(20),"
    "ffrom varchar(15),"
    "fto varchar(15),"
    "departuretime TIME(0),"
    "boardingtime TIME(0),"
    "gate char(1))")
ticketrecordsquery=("CREATE TABLE flight.ticketrecords("
    "bookingnumber char(20) PRIMARY KEY,"
    "seatstatus char(8) NOT NULL DEFAULT 'Economy',"
    "flightdate date NOT NULL,"
    "seatnumber INT NOT NULL,"
    "flightnumber char(5) NOT NULL,"
    "pname varchar(30) NOT NULL"
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
        cr.execute("DESC flight.{};".format(tablename))
    except sql.Error as e:
        if(e.errno == 1146):
            createtable(query)
            print("Table {} created".format(tablename))

def insertflightdata():
    query = ("INSERT INTO flight.flightdetails(flightnumber,"
    "companyname,ffrom,fto,departuretime,boardingtime,gate)"
    "values"
    "('BJ111','Deccan','BBSR','Jeypore','02:30:00','03:10:00','1'),"
    "('MC684','AirAsia','Mumbai','Chennai','15:40:00','17:30:00','3'),"
    "('DB952','Air India','Delhi','Bengaluru','22:30:00','23:10:00','2'),"
    "('HA111','FlyBig','Hyderabad','Ahmedabad','14:20:00','15:15:00','2'),"
    "('LM222','TruJet','Luknow','Mangluru','06:30:00','07:25:00','5'),"
    "('BB125','Star Air','Bhopal','Bikaner','22:33:00','23:13:00','6'),"
    "('KA568','Club One Air','Kochi','Aurangabad','21:45:00','23:35:00','5'),"
    "('DD985','SpiceXpress','Darjelling','Dehradun','21:30:00','22:10:00','8'),"
    "('DN645','SpiceXpress','Diu','Nasik','13:30:00','14:10:00','7'),"
    "('GM785','Titan Aviation','Gaya','Mysore','01:10:00','02:05:00','5')")
    try:
        cr.execute(query)
        print("Flight Data Insertion successful")
    except sql.Error as error:
        print(error)
try:
    global connection, cr
    connection=sql.connect(
        user = 'root', password = '6454', host = 'localhost')
    connection.autocommit=True
    cr=connection.cursor(buffered = True)
    checkdb()
    checktable(flightdetails,flightdetailsquery)
    checktable(ticketrecords,ticketrecordsquery)
    insertflightdata()

except sql.Error as e:
    print(e)
