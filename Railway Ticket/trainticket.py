
import mysql.connector as sql

db = sql.connect(
    host='localhost',
    password='6454',
    database='train',
    user='root'
)
db.autocommit = True
cr = db.cursor()


def getTrainDetails():
    cr.execute("SELECT * FROM traindetails ORDER by ffrom;")
    return cr.fetchall()


def isTicketAvailable(ticket):
    cr.execute(
        "select count(*) from train.ticketrecords where ticketnumber=" + ticket)
    return cr.fetchone()[0] == 0


def isSeatAvailable(seatnumber, trainnumber, date):
    query = ("select * from train.ticketrecords where traindate='" + date
             + "' and seatnumber='" + str(seatnumber)
             + "' and trainnumber='"+ trainnumber + "';")
    cr.execute(query)
    return cr.fetchone() == None


def generateTicket(trainnumber, name,number):
    ticket = trainnumber + str(number) + name[-1:-4:-1]
    number += 1
    if(isTicketAvailable(ticket)):
        return ticket
    else:
        return generateTicket(trainnumber, name,number)

def generateSeat(trainnumber, date,mseat):
    if(isSeatAvailable(mseat, trainnumber, date)):
        return mseat
    else:
        mseat += 1
        return generateSeat(trainnumber, date,mseat)


def istrainFull(trainnumber, date):
    query = ("select count(*) from train.ticketrecords where traindate='" + date
             + "' and trainnumber='" + trainnumber + "';")
    cr.execute(query)
    return cr.fetchone()[0] == 180


def selection(question):
    select = input("{}  (y/n) : ".format(question))
    if(select.lower() == 'y'):
        return True
    elif select.lower() == 'n':
        return False
    else:
        selection(question)


def isTicketAvailable(ticketnumber):
    query = ("SELECT COUNT(*) FROM train.ticketrecords WHERE ticketnumber='" +
             ticketnumber + "';")
    cr.execute(query)
    return cr.fetchone()[0] == 0


def fetchTicketDetails(ticketnumber):
    if(isTicketAvailable(ticketnumber)):
        query = (
            "SELECT * FROM train.ticketrecords WHERE ticketnumber='" + ticketnumber + "';")
        cr.execute(query)
        print(cr.fetchone())
    else:
        print("\nNO DATA AVAILABLE")


def saveTicket(ticketnumber, coachtype, traindate, seatnumber, trainnum, pname):
    query = ("INSERT INTO train.ticketrecords values('"
             + ticketnumber + "','" + coachtype + "','" +
             traindate + "','" + str(seatnumber)
             + "','" + trainnum + "','" + pname + "');")
    cr.execute(query)
    db.commit()

    if(not isTicketAvailable(ticketnumber)):
        print("\ntrain booked successful with ticket number : ", ticketnumber)
    else:
        print("\ntrain booking failed")


def bookTicket():
    trains = getTrainDetails()
    while True:
        index = 1
        print("\n************************************")
        print("********* Booking Menu  ************")
        print("************************************")
        name = input("\nEnter name : ").upper()
        print("")

        for train in trains:
            print(str(index) + ". " + train[1] + ' to ' + train[2])
            index += 1
        selectedtrain = int(input("\nEnter train option : "))
        date = input("\nEnter date for departure (Format - YYYY-MM-DD ) : ")

        if(len(name) > 4 and selectedtrain > 0
                and selectedtrain < len(trains) + 1
                and len(date) == 10):

            trainchoosen = trains[selectedtrain - 1]
            trainnumber = trainchoosen[0]
            print("\n********" + "train Details" + "********")
            print("\nPassanger Name : " + name)
            print("train Number : " + trainchoosen[0])
            print("train From : " + trainchoosen[1])
            print("train To : " + trainchoosen[2])
            print("train Departure Time : " + str(trainchoosen[3]))
            print("platform Number : " + str(trainchoosen[4]))
            print("******************************************")

            compartmenttypes = ["GEN","2S","SL","CC","3A","2A"]
            print("\n Compartment Type")
            for i in enumerate(compartmenttypes):
                print(str(i[0]) + "." + i[1])
            coach = 'GEN'
            coachInput = int(input(
                "\n Enter option : (Default: GEN) : "))
            if(coachInput > 1):
                coach = compartmenttypes[coachInput - 1]

            if(not istrainFull(trainnumber, date)):
                ticketno = 1111
                seatno = 1
                seat = generateSeat(trainnumber, date,seatno)
                ticket = generateTicket(trainnumber, name,ticketno)
                saveTicket(ticket, coach, date, seat, trainnumber, name)
            break
        else:
            print("\n Something went wrong please choose again :")
            continue


def cancelTicket():
    ticketNumber = input("Please provide booking/ticket number : ")
    confirmation = selection("Do you really want to cancel the ticket")
    if(confirmation == True):
        if(not isTicketAvailable(ticketNumber)):
            query = (
                "DELETE FROM train.ticketrecords WHERE ticketnumber='" + ticketNumber + "'")
            cr.execute(query)
            db.commit()
            print("Ticket Successfully Cancelled")
        else:
            print("No ticket available with booking number " + ticketNumber)
    else:
        print("Cancel Process Terminated Successfully ")


def checkBookingDetails():
    ticket = input("Please provide booking/ticket number : ")
    if(not isTicketAvailable(ticket)):
    
        query = "select * from ticketrecords natural join traindetails where ticketnumber ='{}'".format(ticket)
        print(query)
        cr.execute(query)
        details = cr.fetchone()
        print("\n********" + "Ticket Details : " + details[1] + " ********")
        print("DATE : " + str(details[3]))
        print("Passanger Name : " + details[5])
        print("train Number : " + details[0])
        print("train Seat Number : " + str(details[4]))
        print("train From : " + details[6])
        print("train To : " + details[7])
        print("train Departure Time : " + str(details[8]))
        print("train platform Number : " + str(details[9]))
        print("\n******************************************")

    else:
        print("\nNo tickets found with ticket number : " + ticket)

def exit():
    cr.close()
    quit()
def mainMenu():

    while(True):
        print("\n****************************************************************")
        print("************************  Main Menu  ***************************")
        print("****************************************************************\n")
        print("1. Book Ticket ")
        print("2. Cancel Ticket ")
        print("3. Ticket Status Check ")
        print("4. Exit")

        choose = int(input("\nEnter an option : "))
        if choose == 1:
            bookTicket()
            confirm = selection("Do you want to return to the main menu ")
            if(confirm == False):
                exit()
        elif choose == 2:
            cancelTicket()
            confirm = selection("Do you want to return to the main menu ")
            if(confirm == False):
                exit()
        elif choose == 3:
            checkBookingDetails()
            confirm = selection("Do you want to return to the main menu ")
            if(confirm == False):
                exit()
        elif choose == 4:
            exit()
        else:
            print("Invalid Selection")


mainMenu()
