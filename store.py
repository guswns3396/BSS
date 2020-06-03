import csv
import mysql.connector
from Player import Hitter

def store(path):
    # establish connection
    user = "root"
    pw = input("password=")
    host = "localhost"
    db = "players_db"
    try:
        cnx = mysql.connector.connect(user=user,password=pw,host=host,database=db)
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("Could not establish connection")
            print(err)
        exit()

    # open file & read
    playerList = []
    with open(path) as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            # instantiate Player & append to list
            hitter = Hitter(row)
            playerList.append(hitter)

    # insert into db
