import unittest
from src.model.Question import Question


class MyTestCase(unittest.TestCase):
    def test_question_constructor(self):
        question_string = "Who invented Python?"
        answer = "Guido van Russom"
        choices = ["John Doe", "John Doe2", "John Doe3", answer]
        selected = -1
        question = Question(question_string, answer, choices, selected)

        self.assertEqual(question_string, question.question)


if __name__ == '__main__':
    unittest.main()
