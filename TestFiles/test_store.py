import importlib
import unittest
import store

class TestStore(unittest.TestCase):
    def test_establishConnection_raisesErrorWhenWrongPassword(self):
        print("Enter Incorrect Password")
        importlib.reload(store)

        with self.assertRaises(SystemExit) as cm:
            store.establishConnection()

        print("Enter Correct Password")
        importlib.reload(store)
        self.assertEqual(cm.exception.code, 1)

    def test_establishConnection_establishesConnection(self):
        cnx, cursor = store.establishConnection()

        self.assertIsInstance(cursor, store.mysql.connector.cursor.MySQLCursor)

    def test_execute_executesQuery(self):
        cnx, cursor = store.establishConnection()
        sql = "INSERT INTO hitters (name,rhp,lhp,hpflyball,hppower,hpavg,"
        sql += "hpfinesse,hphome,hpaway,hpgroundball)"
        sql += " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql = (sql)
        data = ("Test Player", 1, 2, 3, 4, 5, 6, 7, 8, 9)

        store.execute(cursor, sql, data)

        sql = "SELECT name FROM hitters"
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        self.assertEqual(results[0],("Test Player",))

    def test_execute_raisesError(self):
        cnx, cursor = store.establishConnection()
        sql = "this is a test"
        data = ()

        with self.assertRaises(Exception) as cm:
            store.execute(cursor,sql,data)

        cursor.close()
        cnx.close()
        self.assertIsInstance(cm.exception, store.mysql.connector.Error)

    # def test_storeHitters_insertsIntoDatabase(self):
    #     importlib.reload(store)
    #     with open("PlayerTest.csv","w") as f:
    #         header = "Player Name,HPRHP,HPLHP,HPHome,HPAway,HPPower,HPFinesse,HPFlyball,HPGroundball,HPAvg"
    #         print(header,file=f)
    #         hitter = "David Ortiz,0.2679324895,0.2763157895,0.2787878788,0.2601351351,0.3375796178,0.2315270936,0.2487804878,0.2595419847,0.2896551724"
    #         print(hitter,file=f)
    #
    #     store.storeHitters("PlayerTest.csv")
    #
    #
    #     self.assertEqual(1,1)

if __name__ == "__main__":
    unittest.main()