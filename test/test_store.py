import importlib
import unittest
import os
import pathlib
import store

class TestStore(unittest.TestCase):
    def tearDown(self):
        # delete test players from db
        cnx = store.mysql.connector.connect(\
            user=store.USER, password=store.PW, host=store.HOST, database=store.DB
        )
        cursor = cnx.cursor()
        sql = "DELETE FROM hitters WHERE name = %s"
        data = ("Test Player",)
        cursor.execute(sql, data)
        cnx.commit()
        cursor.close()
        cnx.close()

        # delete test csv file
        path = str(pathlib.Path(__file__).parent.absolute()) + "/PlayerTest.csv"
        if os.path.isfile(path):
            os.remove(path)

    def step1_establishConnection_raisesErrorWhenWrongPassword(self):
        print("Enter Incorrect Password")
        importlib.reload(store)

        with self.assertRaises(SystemExit) as cm:
            store.establishConnection()

        print("Enter Correct Password")
        importlib.reload(store)
        self.assertEqual(cm.exception.code, 1)

    def step1_establishConnection_establishesConnection(self):
        cnx, cursor = store.establishConnection()

        self.assertIsInstance(cursor, store.mysql.connector.cursor.MySQLCursor)

    def step2_execute_executesQuery(self):
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

    def step2_execute_raisesError(self):
        cnx, cursor = store.establishConnection()
        sql = "this is a test"
        data = ()

        with self.assertRaises(Exception) as cm:
            store.execute(cursor,sql,data)

        cursor.close()
        cnx.close()
        self.assertIsInstance(cm.exception, store.mysql.connector.Error)

    def step3_closeConnection_commitsChange(self):
        cnx, cursor = store.establishConnection()
        sql = "INSERT INTO hitters (name,rhp,lhp,hpflyball,hppower,hpavg,"
        sql += "hpfinesse,hphome,hpaway,hpgroundball)"
        sql += " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql = (sql)
        data = ("Test Player", 1, 2, 3, 4, 5, 6, 7, 8, 9)
        store.execute(cursor, sql, data)

        store.closeConnection(cnx, cursor)

        cnx, cursor = store.establishConnection()
        sql = "SELECT name FROM hitters"
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        cnx.close()
        self.assertEqual(results[0],("Test Player",))

    def step4_storeHitters_insertsIntoDatabase(self):
        with open("PlayerTest.csv","w") as f:
            header = "Player Name,HPRHP,HPLHP,HPHome,HPAway,HPPower,HPFinesse,HPFlyball,HPGroundball,HPAvg"
            print(header,file=f)
            hitter = "Test Player,0.2679324895,0.2763157895,0.2787878788,0.2601351351,0.3375796178,0.2315270936,0.2487804878,0.2595419847,0.2896551724"
            print(hitter,file=f)

        store.storeHitters("PlayerTest.csv")

        cnx, cursor = store.establishConnection()
        sql = "SELECT name FROM hitters"
        cursor.execute(sql)
        results = cursor.fetchall()
        self.assertEqual(results[0], ("Test Player",))

    def _steps(self):
        for name in dir(self):
            if name.startswith("step"):
                yield name, getattr(self, name)

    def test_steps(self):
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                self.fail("{} failed ({} : {})".format(step,type(e),e))

if __name__ == "__main__":
    unittest.main()