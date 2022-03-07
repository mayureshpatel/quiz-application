import src.controller.DatabaseHelper as db_helper
import unittest
import sqlite3
import os

path = "../../app_data/test.db"

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        db_helper.clear_tables(path)

    def test_db_create_table00(self):
        # create a table and check if it was created correctly
        p1 = "id INTEGER PRIMARY KEY, name TEXT"
        db_helper.create_table(path, "quiz", p1)

        expected = ['quiz']
        actual = db_helper.get_tables(path)
        self.assertEqual(expected, actual)

    def test_db_create_table01(self):
        # create a table and check if it was created correctly
        p1 = "id INTEGER PRIMARY KEY, name TEXT"
        p2 = "id INTEGER PRIMARY KEY, name TEXT, value INTEGER, fire TEXT"

        db_helper.create_table(path, "quiz", p1)
        db_helper.create_table(path, 'flame', p2)
        db_helper.create_table(path, "ques", p1)
        db_helper.create_table(path, "cheese", p2)

        expected = ['quiz', 'flame', 'ques', 'cheese']
        actual = db_helper.get_tables(path)
        self.assertEqual(expected, actual)

    def test_db_is_table_in_db00(self):
        # create a table and check if it was created correctly
        p1 = "id INTEGER PRIMARY KEY, name TEXT"
        p2 = "id INTEGER PRIMARY KEY, name TEXT, value INTEGER, fire TEXT"

        db_helper.create_table(path, "quiz", p1)
        db_helper.create_table(path, 'flame', p2)
        db_helper.create_table(path, "ques", p1)
        db_helper.create_table(path, "cheese", p2)

        self.assertEqual(True, db_helper.is_table_in_db(path, "quiz"))
        self.assertEqual(True, db_helper.is_table_in_db(path, "flame"))
        self.assertEqual(False, db_helper.is_table_in_db(path, "hazel"))
        self.assertEqual(False, db_helper.is_table_in_db(path, "halo"))
        self.assertEqual(True, db_helper.is_table_in_db(path, "cheese"))

    def test_db_drop_table00(self):
        # create a table and check if it was created correctly
        p1 = "id INTEGER PRIMARY KEY, name TEXT"
        p2 = "id INTEGER PRIMARY KEY, name TEXT, value INTEGER, fire TEXT"

        db_helper.create_table(path, "quiz", p1)
        db_helper.create_table(path, 'flame', p2)
        db_helper.create_table(path, "ques", p1)
        db_helper.create_table(path, "cheese", p2)

        self.assertEqual(False, db_helper.drop_table(path, "tango"))
        self.assertEqual(True, db_helper.drop_table(path, "flame"))
        self.assertEqual(False, db_helper.drop_table(path, "charlie"))
        self.assertEqual(True, db_helper.drop_table(path, "quiz"))
        self.assertEqual(True, db_helper.drop_table(path, "ques"))

        expected = ['cheese']
        actual = db_helper.get_tables(path)
        self.assertEqual(expected, actual)

    def test_db_execute_query_insert00(self):
        # create a table
        p1 = "id INTEGER PRIMARY KEY, question TEXT, answer TEXT"
        db_helper.create_table(path, "question", p1)

        # using the execute_query method, insert a record for the question table
        insert_query = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args = ["What is 1 + 1?", "2"]
        db_helper.execute_query(path, insert_query, insert_args)

        expected = [(1, insert_args[0], insert_args[1])]
        actual = db_helper.execute_query(path, "SELECT * from question")
        self.assertEqual(expected, actual)

    def test_db_execute_query_insert01(self):
        # create a table
        p1 = "id INTEGER PRIMARY KEY, question TEXT, answer TEXT"
        db_helper.create_table(path, "question", p1)

        # using the execute_query method, insert a record for the question table
        insert_query1 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args1 = ["What is 1 + 1?", "2"]
        db_helper.execute_query(path, insert_query1, insert_args1)

        insert_query2 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args2 = ["What is 4 * 1?", "4"]
        db_helper.execute_query(path, insert_query2, insert_args2)

        insert_query3 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args3 = ["What is 99 + 1?", "100"]
        db_helper.execute_query(path, insert_query3, insert_args3)

        expected = [(1, insert_args1[0], insert_args1[1]),
                    (2, insert_args2[0], insert_args2[1]),
                    (3, insert_args3[0], insert_args3[1])
                    ]

        actual = db_helper.execute_query(path, "SELECT * from question")
        self.assertEqual(expected, actual)

    def test_db_execute_query_insert02(self):
        # create a table
        p1 = "id INTEGER PRIMARY KEY, question TEXT, answer TEXT"
        db_helper.create_table(path, "question", p1)

        # using the execute_query method, insert a record for the question table
        insert_query1 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args1 = ["What is 1 + 1?", "2"]
        db_helper.execute_query(path, insert_query1, insert_args1)

        db_helper.execute_query(path, insert_query1, insert_args1)

        insert_query3 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args3 = ["What is 99 + 1?", "100"]
        db_helper.execute_query(path, insert_query3, insert_args3)

        expected = [(1, insert_args1[0], insert_args1[1]),
                    (2, insert_args1[0], insert_args1[1]),
                    (3, insert_args3[0], insert_args3[1])
                    ]

        actual = db_helper.execute_query(path, "SELECT * from question")
        self.assertEqual(expected, actual)

    def test_db_execute_query_insert03(self):
        # create a table
        p1 = "id INTEGER PRIMARY KEY, question TEXT UNIQUE, answer TEXT"
        db_helper.create_table(path, "question", p1)

        # using the execute_query method, insert a record for the question table
        insert_query1 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args1 = ["What is 1 + 1?", "2"]
        db_helper.execute_query(path, insert_query1, insert_args1)

        self.assertRaises(sqlite3.IntegrityError, db_helper.execute_query, path, insert_query1, insert_args1)

        insert_query3 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args3 = ["What is 99 + 1?", "100"]
        db_helper.execute_query(path, insert_query3, insert_args3)

        expected = [(1, insert_args1[0], insert_args1[1]),
                    (2, insert_args3[0], insert_args3[1]),
                    ]

        actual = db_helper.execute_query(path, "SELECT * from question")
        self.assertEqual(expected, actual)

    def test_db_execute_query_update00(self):
        # create a table
        p1 = "id INTEGER PRIMARY KEY, question TEXT, answer TEXT"
        db_helper.create_table(path, "question", p1)

        # using the execute_query method, insert a record for the question table
        insert_query1 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args1 = ["What is 1 + 1?", "2"]
        db_helper.execute_query(path, insert_query1, insert_args1)

        insert_query2 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args2 = ["What is 4 * 1?", "4"]
        db_helper.execute_query(path, insert_query2, insert_args2)

        insert_query3 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args3 = ["What is 99 + 1?", "100"]
        db_helper.execute_query(path, insert_query3, insert_args3)

        expected = [
            (1, insert_args1[0], insert_args1[1]),
            (2, insert_args2[0], insert_args2[1]),
            (3, insert_args3[0], insert_args3[1])
        ]

        actual = db_helper.execute_query(path, "SELECT * FROM question")
        self.assertEqual(expected, actual)

        # update a record from the table
        update_query = "UPDATE question SET question = (?), answer = (?) WHERE id = (?)"
        update_args = ["What is 9 * 4?", "36", 2]
        db_helper.execute_query(path, update_query, update_args)

        expected = [
            (1, insert_args1[0], insert_args1[1]),
            (2, "What is 9 * 4?", "36"),
            (3, insert_args3[0], insert_args3[1])
        ]
        actual = db_helper.execute_query(path, "SELECT * FROM question")
        # print(db_helper.execute_query(path, "SELECT * from question"))
        self.assertEqual(expected, actual)

    def test_db_execute_query_update01(self):
        # create a table
        p1 = "id INTEGER PRIMARY KEY, question TEXT, answer TEXT"
        db_helper.create_table(path, "question", p1)

        # using the execute_query method, insert a record for the question table
        insert_query1 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args1 = ["What is 1 + 1?", "2"]
        db_helper.execute_query(path, insert_query1, insert_args1)

        insert_query2 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args2 = ["What is 4 * 1?", "4"]
        db_helper.execute_query(path, insert_query2, insert_args2)

        insert_query3 = "INSERT INTO question VALUES(NULL, ?, ?)"
        insert_args3 = ["What is 99 + 1?", "100"]
        db_helper.execute_query(path, insert_query3, insert_args3)

        expected = [
            (1, insert_args1[0], insert_args1[1]),
            (2, insert_args2[0], insert_args2[1]),
            (3, insert_args3[0], insert_args3[1])
        ]

        actual = db_helper.execute_query(path, "SELECT * FROM question")
        self.assertEqual(expected, actual)

        # update a record from the table
        update_query = "UPDATE question SET question = (?), answer = (?) WHERE id = (?)"
        update_args = ["What is 9 * 4?", "36", 2]
        db_helper.execute_query(path, update_query, update_args)

        update_args = ["What is 2 + 3?", "5", 3]
        db_helper.execute_query(path, update_query, update_args)

        expected = [
            (1, insert_args1[0], insert_args1[1]),
            (2, "What is 9 * 4?", "36"),
            (3, "What is 2 + 3?", "5")
        ]
        actual = db_helper.execute_query(path, "SELECT * FROM question")
        # print(db_helper.execute_query(path, "SELECT * FROM question"))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
