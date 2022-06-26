import mysql.connector as sql

db = sql.connect(
    host='localhost',
    password='6454',
    database='flight',
    user='root'
)

cr = db.cursor()

query = ("SELECT * from flight.ticketrecords ORDER BY flightdate"
",flightnumber;") 

cr.execute(query)
print("*" * 100)
print("Booking Number" + " | " + "Seat Status" + " | " 
    + "Flight Date "+" | " + "Seat Number"+ " | " 
    + "Flight Number"+ " | " + "Passanger Name")
print("*" * 100)
for record in cr.fetchall():
    print(record[0] + "      " + record[1] + "      " 
    + str(record[2])+"         " + str(record[3]) + "           " 
    + record[4]+ "        " + record[5])
print("*" * 100)
print("Total = {}".format(cr.rowcount))