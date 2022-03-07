import src.controller.DatabaseHelper as db_helper
import src.model.Question as QuesFunc
from src.model.Question import Question
import unittest

path = "../../app_data/test.db"
question_table_create_params = """
    id INTEGER PRIMARY KEY,
    quiz_id INTEGER NOT NULL,
    question TEXT UNIQUE NOT NULL,
    answer TEXT NOT NULL,
    choice1 TEXT NOT NULL,
    choice2 TEXT NOT NULL,
    choice3 TEXT NOT NULL,
    choice4 TEXT NOT NULL
"""
question_examples = [
    [
        "Where is the Great Barrier Reef located?",
        "Australia",
        ["Australia", "China", "Finland", "Denmark"]
    ],
    [
        "Which house was Harry Potter almost sorted into?",
        "Slytherin",
        ["First House", "Slytherin", "Hufflepuff", "Sonoma"]
    ],
    [
        "What sport does Christiano Ronaldo play?",
        "Soccer",
        ["Tennis", "Cricket", "Lacrosse", "Soccer"]
    ],
    [
        "What doe Na stand for on the periodic table?",
        "Sodium",
        ["Potassium", "Zinc", "Sodium", "Hydrogen"]
    ]
]
question_db_expected = [
    # question 1
    (
        1,
        1,
        'Where is the Great Barrier Reef located?',
        'Australia',
        'Australia',
        'China',
        'Finland',
        'Denmark'
    ),
    # question 2
    (
        2,
        1,
        'Which house was Harry Potter almost sorted into?',
        'Slytherin',
        'First House',
        'Slytherin',
        'Hufflepuff',
        'Sonoma'
    ),
    # question 3
    (
        3,
        1,
        'What sport does Christiano Ronaldo play?',
        'Soccer',
        'Tennis',
        'Cricket',
        'Lacrosse',
        'Soccer'
    ),
    # question 4
    (
        4,
        1,
        'What doe Na stand for on the periodic table?',
        'Sodium',
        'Potassium',
        'Zinc',
        'Sodium',
        'Hydrogen'
    )
]

class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        # start with a clean slate and drop all existing tables in the test database
        db_helper.clear_tables(path)

        # create a quiz and question table
        db_helper.create_table(path, "quiz", "id INTEGER PRIMARY KEY, name TEXT")
        db_helper.create_table(path, "question", question_table_create_params)

        # insert a new quiz into the 'quiz' table
        db_helper.execute_query(path, "INSERT INTO quiz VALUES(NULL, ?)", ["Random Quiz"])

        # insert all the questions into the new 'Random Quiz' quiz
        q2 = Question(question_examples[1][0], question_examples[1][1], question_examples[1][2], -1)
        q3 = Question(question_examples[2][0], question_examples[2][1], question_examples[2][2], -1)
        q1 = Question(question_examples[0][0], question_examples[0][1], question_examples[0][2], -1)
        q4 = Question(question_examples[3][0], question_examples[3][1], question_examples[3][2], -1)
        insert_query = """INSERT INTO question VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)"""
        for question in [q1, q2, q3, q4]:
            db_helper.execute_query(
                path,
                insert_query,
                [
                    1,
                    question.question,
                    question.answer,
                    question.choices[0],
                    question.choices[1],
                    question.choices[2],
                    question.choices[3],
                ]
            )

    def test_question_db_create_table(self):
        expected = ['quiz', 'question']
        self.assertEqual(expected, db_helper.get_tables(path))

    def test_question_db_insert_question00(self):
        expected = ['quiz', 'question']
        self.assertEqual(expected, db_helper.get_tables(path))
        self.assertEqual(
            [(1, "Random Quiz")],
            db_helper.execute_query(path, "SELECT * FROM quiz")
        )

        # test the questions that were inserted
        self.assertEqual(question_db_expected, db_helper.execute_query(path, "SELECT * FROM question"))

    def test_question_db_get_all00(self):
        # use the get_all function from the Question file
        questions = QuesFunc.get_all(path)
        self.assertEqual(question_db_expected, questions)

    def test_question_db_insert_fail00(self):
        # try inserting a question that is already in the Question database
        q1 = Question(question_examples[0][0], question_examples[0][1], question_examples[0][2], -1)
        self.assertEqual(False, QuesFunc.insert_question(path, 1, q1.question, q1.answer, q1.choices))


if __name__ == "__main__":
    unittest.main()
