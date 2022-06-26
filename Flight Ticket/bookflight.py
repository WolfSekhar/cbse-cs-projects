
import mysql.connector as sql

db = sql.connect(
    host='localhost',
    password='6454',
    database='flight',
    user='root'
)
db.autocommit = True
cr = db.cursor(buffered = True)


def getFlightDetails():
    cr.execute("SELECT * FROM flightdetails ORDER by ffrom;")
    return cr.fetchall()


def isTicketAvailable(ticket):
    cr.execute(
        "select count(*) from flight.ticketrecords where bookingnumber=" + ticket)
    return cr.fetchone()[0] == 0


def isSeatAvailable(seatnumber, flightnumber, date):
    query = ("select * from flight.ticketrecords where flightdate='" + date
             + "' and seatnumber='" + str(seatnumber)
             + "' and flightnumber='"+ flightnumber + "';")
    cr.execute(query)
    return cr.fetchone() == None


def generateTicket(flightnumber, name,number):
    ticket = flightnumber + str(number) + name[-1:-4:-1]
    number += 1
    if(isTicketAvailable(ticket)):
        return ticket
    else:
        return generateTicket(flightnumber, name,number)

def generateSeat(flightnumber, date,mseat):
    if(isSeatAvailable(mseat, flightnumber, date)):
        return mseat
    else:
        mseat += 1
        return generateSeat(flightnumber, date,mseat)


def isFlightFull(flightnumber, date):
    query = ("select count(*) from flight.ticketrecords where flightdate='" + date
             + "' and flightnumber='" + flightnumber + "';")
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
    query = ("SELECT COUNT(*) FROM flight.ticketrecords WHERE bookingnumber='" +
             ticketnumber + "';")
    cr.execute(query)
    return cr.fetchone()[0] == 0


def fetchTicketDetails(ticketnumber):
    if(isTicketAvailable(ticketnumber)):
        query = (
            "SELECT * FROM flight.ticketrecords WHERE bookingnumber='" + ticketnumber + "';")
        cr.execute(query)
        print(cr.fetchone())
    else:
        print("\n NO DATA AVAILABLE")


def saveTicket(ticketnumber, seatstatus, flightdate, seatnumber, flightnum, pname):
    query = ("INSERT INTO flight.ticketrecords values('"
             + ticketnumber + "','" + seatstatus + "','" +
             flightdate + "','" + str(seatnumber)
             + "','" + flightnum + "','" + pname + "');")
    cr.execute(query)
    db.commit()

    if(not isTicketAvailable(ticketnumber)):
        print("\n Flight booked successful with ticket number : ", ticketnumber)
        print("\n Please do the payment at Airport")
    else:
        print("\n Flight booking failed")


def bookTicket():
    flights = getFlightDetails()
    while True:
        index = 1
        print("\n************************************")
        print("********* Booking Menu  ************")
        print("************************************")
        name = input("\nEnter name : ").upper()
        print("")

        for flight in flights:
            print(str(index) + ". " + flight[2] + ' to ' + flight[3])
            index += 1
        selectedflight = int(input("\n Enter flight option : "))
        date = input("\n Enter date for departure (Eg - 2020-10-11 ) : ")

        if(len(name) > 4 and selectedflight > 0
                and selectedflight < len(flights) + 1
                and len(date) == 10):

            flightchoosen = flights[selectedflight - 1]
            flightnumber = flightchoosen[0]
            print("\n********" + "Flight Details" + "********")
            print("\n Passanger Name : " + name)
            print(" Flight Number : " + flightchoosen[0])
            print(" Flight Name : " + flightchoosen[1])
            print(" Flight From : " + flightchoosen[2])
            print(" Flight To : " + flightchoosen[3])
            print(" Flight Boarding Time : " + str(flightchoosen[4]))
            print(" Flight Departure Time : " + str(flightchoosen[5]))
            print(" Gate Number : " + str(flightchoosen[6]))
            print("******************************************")

            print("\n Seat Status \n 1. Economy\n 2. Business")
            status = 'Economy'
            statusInput = input(
                "\n Enter status option : (Default: Economy) : ")

            if(statusInput == '2'):
                status = "Business"

            if(not isFlightFull(flightnumber, date)):
                ticketno = 1111
                seatno = 1
                seat = generateSeat(flightnumber, date,seatno)
                ticket = generateTicket(flightnumber, name,ticketno)
                saveTicket(ticket, status, date, seat, flightnumber, name)
            break
        else:
            print("\n Something went wrong please choose again :")
            continue


def cancelTicket():
    ticketNumber = input(" Please provide booking/ticket number : ")
    confirmation = selection(" Do you really want to cancel the ticket")
    if(confirmation == True):
        if(not isTicketAvailable(ticketNumber)):
            query = (
                "DELETE FROM flight.ticketrecords WHERE bookingnumber='" + ticketNumber + "'")
            cr.execute(query)
            db.commit()
            print(" Ticket Successfully Cancelled")
        else:
            print(" No ticket available with booking number " + ticketNumber)
    else:
        print(" Cancel Process Terminated Successfully ")


def checkBookingDetails():
    ticket = input(" Please provide booking/ticket number : ")
    if(not isTicketAvailable(ticket)):
        query = ("SELECT * FROM flight.ticketrecords natural join flight.flightdetails" +
                 " WHERE bookingnumber ='" + ticket + "';")
        cr.execute(query)
        details = cr.fetchone()
        print("\n********" + "Ticket Details : " + details[1] + " ********")
        print(" DATE - " + str(details[3]))
        print("\n Passanger Name : " + details[5])
        print(" Flight Number : " + details[0])
        print(" Flight Name : " + details[6])
        print(" Flight Seat Number : " + str(details[4]))
        print(" Flight From : " + details[7])
        print(" Flight To : " + details[8])
        print(" Flight Boarding Time : " + str(details[9]))
        print(" Flight Departure Time : " + str(details[10]))
        print(" Flight Gate Number : " + str(details[11]))
        print("\n******************************************")

    else:
        print("\n No tickets found with ticket number : " + ticket)


def mainMenu():

    while(True):
        print("\n****************************************************************")
        print("************************  Main Menu  ***************************")
        print("****************************************************************\n")
        print(" 1. Book Ticket ")
        print(" 2. Cancel Ticket ")
        print(" 3. Ticket Status Check ")
        print(" 4. Exit")

        choose = int(input("\n Enter an option : "))
        if choose == 1:
            bookTicket()
            confirm = selection(" Do you want to return to the main menu ")
            if(confirm == False):
                quit()
        elif choose == 2:
            cancelTicket()
            confirm = selection(" Do you want to return to the main menu ")
            if(confirm == False): 
                quit()
        elif choose == 3:
            checkBookingDetails()
            confirm = selection(" Do you want to return to the main menu ")
            if(confirm == False): 
                quit()
        elif choose == 4:
            quit()
        else:
            print(" Invalid Selection")


mainMenu()

