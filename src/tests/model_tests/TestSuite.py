import unittest

import databasehelper_test as db_helper
import quiz_test as quiz
import quiz_db_test as quiz_db

import question_test as question
import question_db_test as question_db

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(db_helper))
suite.addTest(loader.loadTestsFromModule(quiz))
suite.addTest(loader.loadTestsFromModule(quiz_db))
suite.addTest(loader.loadTestsFromModule(question))
suite.addTest(loader.loadTestsFromModule(question_db))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
