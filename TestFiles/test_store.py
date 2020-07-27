import importlib
import unittest
import store
from io import StringIO
from unittest.mock import patch

class TestStore(unittest.TestCase):

    def test_establishConnection_establishesConnection(self):
        print("Enter Correct Password")
        importlib.reload(store)

        cnx, cursor = store.establishConnection()

        self.assertIsInstance(cursor, store.mysql.connector.cursor.MySQLCursor)

    def test_establishConnection_raisesErrorWhenWrongPassword(self):
        print("Enter Incorrect Password")
        importlib.reload(store)
        msg_expected = "Something is wrong with your user name or password\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            cnx, cursor = store.establishConnection()
            msg_output = fake_out.getvalue()

        self.assertEqual(msg_expected, msg_output)



if __name__ == "__main__":
    unittest.main()