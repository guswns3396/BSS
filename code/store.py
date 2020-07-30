import csv
import sys
import mysql.connector

USER = "root"
PW = input("password=")
HOST = "localhost"
DB = "players_db"

def establishConnection():
    """
    establishes connection with the db
    :return: connection & cursor objects
    """
    global USER
    global PW
    global HOST
    global DB
    try:
        cnx = mysql.connector.connect(user=USER, password=PW, host=HOST, database=DB)
        cursor = cnx.cursor()
        return cnx, cursor
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("Could not establish connection")
            print(err)
        sys.exit(1)
    except:
        print("Could not establish connection")
        sys.exit(1)

def execute(cursor, sql, data):
    """
    executes the sql command
    :param cursor: cursor object
    :param sql: string for sql command
    :param data: tuple for data
    :return: None
    """
    try:
        cursor.execute(sql, data)
    except mysql.connector.Error:
        print("Something went wrong executing SQL statement")
        raise

def closeConnection(cnx, cursor):
    """
    closes connection from db
    :param cnx: cnx object
    :param cursor: cursor object
    :return: None
    """
    cnx.commit()
    cursor.close()
    cnx.close()

def storePlayersToDB(pathToCSV, type):
    """
    given path to csv containing stats of hitters,
    store them into database
    :param path: path to csv file containing stats of hitters
    :param type: string 'hitter' or 'pitcher
    :return: None
    """
    # check for valid arguments
    if type != "hitter" and type != "pitcher":
        raise ValueError("argument 'type' must either be 'hitter' or 'pitcher'")

    # establish connection
    cnx, cursor = establishConnection()

    # open file & read & store as list of ordered dicts
    players = []
    with open(pathToCSV) as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            players.append(row)

    # do for type
    if type == 'hitter':
        # insert into db
        sql = "INSERT INTO hitters (name,rhp,lhp,hppower,hpavg,hpfinesse,"
        sql += "hpgroundball,hpflyball,hphome,hpaway)"
        sql += " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql = (sql)

        for player in players:
            data = (\
                player["Player Name"], player["RHP"], player["LHP"], \
                player["HPPower"], player["HPAvg"], player["HPFinesse"], \
                player["HPGroundball"], player["HPFlyball"], player["HPHome"], player["HPAway"], \
                    )
            execute(cursor, sql, data)
    elif type == 'pitcher':
        pass

    # commit changes & close connection
    closeConnection(cnx, cursor)