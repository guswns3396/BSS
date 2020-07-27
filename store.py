import csv
import mysql.connector

USER = "root"
PW = input("password=")
HOST = "localhost"
DB = "players_db"

def storeHitters(path):
    """
    given path to csv containing stats of hitters,
    store them into database
    :param path: path to csv file containing stats of hitters
    :return: None
    """
    # establish connection
    global USER
    global PW
    global HOST
    global DB
    try:
        cnx = mysql.connector.connect(user=USER,password=PW,host=HOST,database=DB)
        cursor = cnx.cursor()
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("Could not establish connection")
            print(err)
        exit()

    # open file & read & store as list of ordered dicts
    players = []
    with open(path) as fh:
        rd = csv.DictReader(fh, delimiter=',')
        for row in rd:
            players.append(row)

    # insert into db
    sql = "INSERT INTO hitters (name,rhp,lhp,hpflyball,hppower,hpavg,"
    sql += "hpfinesse,hphome,hpaway,hpgroundball)"
    sql += " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sql = (sql)

    for player in players:
        data = (\
            player["Player Name"], player["HPRHP"], player["HPLHP"], \
            player["HPFlyball"], player["HPPower"], player["HPAvg"], \
            player["HPFinesse"], player["HPHome"], player["HPAway"], \
            player["HPGroundball"]
                )
        try:
            cursor.execute(sql, data)
        except mysql.connector.Error:
            print("Something went wrong executing SQL statement")
            raise

    cnx.commit()
    cursor.close()
    cnx.close()