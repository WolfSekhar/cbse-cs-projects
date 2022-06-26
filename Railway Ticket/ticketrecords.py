import mysql.connector as sql

db = sql.connect(
    host='localhost',
    password='6454',
    database='train',
    user='root'
)

cr = db.cursor()

query = ("SELECT * from train.ticketrecords ORDER BY traindate") 

cr.execute(query)
print("*" * 100)
print("Ticket Number" + " | " + "Compartment Status" + " | " 
    + "Train Date "+" | " + "Seat Number"+ " | " 
    + "Train Number"+ " | " + "Passanger Name")
print("*" * 100)
for record in cr.fetchall():
    print(record[0] + "      " + record[1] + "             " 
    + str(record[2])+"         " + str(record[3]) + "           " 
    + record[4]+ "        " + record[5])
print("*" * 100)
print("Total = {}".format(cr.rowcount))
cr.close()