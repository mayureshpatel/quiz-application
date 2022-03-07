import src.controller.DatabaseHelper as db_helper
from src.model.Quiz import Quiz
from src.model.Question import Question
from src.model import Quiz as QuizFunc
import unittest

path = "../../app_data/test.db"
question_table_create_params = """
    id INTEGER PRIMARY KEY,
    quiz_id INTEGER NOT NULL,
    question TEXT NOT NULL,
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
        "What does Na stand for on the periodic table?",
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
        'What does Na stand for on the periodic table?',
        'Sodium',
        'Potassium',
        'Zinc',
        'Sodium',
        'Hydrogen'
    )
]

quiz_db_expected = Quiz(
    "Random Quiz",
    [
        Question(question_examples[0][0], question_examples[0][1], question_examples[0][2], -1),
        Question(question_examples[1][0], question_examples[1][1], question_examples[1][2], -1),
        Question(question_examples[2][0], question_examples[2][1], question_examples[2][2], -1),
        Question(question_examples[3][0], question_examples[3][1], question_examples[3][2], -1)
    ]
)

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

    def test_quiz_db_get_quiz00(self):
        self.assertEqual(['quiz', 'question'], db_helper.get_tables(path))
        self.assertEqual(
            question_db_expected,
            db_helper.execute_query(path, "SELECT * FROM question WHERE (quiz_id = ?)", [1])
        )

        # use the get_quiz function from the Quiz file
        quiz = QuizFunc.get_quiz(path, "Random Quiz")

        # test the resulting quiz object
        self.assertEqual("Random Quiz", quiz.name)
        self.assertEqual(quiz_db_expected.question_list[0], quiz.question_list[0])
        self.assertEqual(quiz_db_expected.question_list[1], quiz.question_list[1])
        self.assertEqual(quiz_db_expected.question_list[2], quiz.question_list[2])
        self.assertEqual(quiz_db_expected.question_list[3], quiz.question_list[3])

    def test_quiz_db_get_all_quizzes00(self):
        self.assertEqual(['quiz', 'question'], db_helper.get_tables(path))
        self.assertEqual(
            question_db_expected,
            db_helper.execute_query(path, "SELECT * FROM question WHERE (quiz_id = ?)", [1])
        )

        # add another quiz to the table and test to make sure there are 2 quizzes in the quiz table
        db_helper.execute_query(path, "INSERT INTO quiz VALUES(NULL, ?)", ["Harry Potter"])
        self.assertEqual(
            [(1, "Random Quiz"), (2, "Harry Potter")],
            db_helper.execute_query(path, "SELECT * FROM quiz")
        )

        # insert all the questions into the new 'Random Quiz' quiz
        q1 = Question(
            question_examples[1][0],
            question_examples[1][1],
            question_examples[1][2],
            -1
        )
        q2 = Question(
            question_examples[2][0],
            question_examples[2][1],
            question_examples[2][2],
            -1
        )

        insert_query = """INSERT INTO question VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)"""
        for question in [q1, q2]:
            db_helper.execute_query(
                path,
                insert_query,
                [
                    2,
                    question.question,
                    question.answer,
                    question.choices[0],
                    question.choices[1],
                    question.choices[2],
                    question.choices[3],
                ]
            )

        # use the get_all_quizzes function from the Quiz file
        quizzes = QuizFunc.get_all_quizzes(path)


if __name__ == "__main__":
    unittest.main()
