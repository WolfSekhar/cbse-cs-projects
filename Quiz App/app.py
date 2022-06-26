import mysql.connector as sql

quequery = 'select * from question'
ansquery = 'select * from answer'

try:
    global connection, cr
    connection=sql.connect(
        user = 'root', password = '6454', host = 'localhost',database = 'quiz')
    connection.autocommit=True
    cr=connection.cursor(buffered = True)
except sql.Error as e:
    print(e)

cr.execute(quequery)
questions = cr.fetchall()

cr.execute(ansquery)
answers = cr.fetchall()

def selection(question):
    select = input("{}  (y/n) : ".format(question))
    if(select.lower() == 'y'):
        return True
    elif select.lower() == 'n':
        return False
    else:
        selection(question)

def startquiz():
    counter = 0
    for i in enumerate(questions):
        print("\n " + i[1][1])
        cans = str(i[1][2])
        mcq = answers[i[0]]
        print("\n")
        for j in range(1,5):
            print(str(j) + ". " + mcq[j])
        option = (input("Enter your choice : "))

        if option == cans:
            counter += 1
    print("Your total score is : " + str(counter))
    select = selection("Do you want to restart Quiz ? ")
    if(select):
        startquiz()
        

def mainmenu():
    print("\n*************** WELCOME TO QUIZ APP*************")
    print("")

    mainmenuoptions = "\n1.Start quiz \n2.Quit App"
    print(mainmenuoptions)
    option = input("Enter your options : ")
    if(option == '1'):
        startquiz()
    else:
        quit()

mainmenu()