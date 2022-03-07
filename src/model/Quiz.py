import sqlite3

from src.model.Question import Question
from src.model import Question as QuesFunc
import src.controller.DatabaseHelper as db_helper


class Quiz:
    """
    An object to represent a Quiz object. This object consists of a list of Question objects.
    """

    def __init__(self, name: str, question_list: list):
        """
        Constructs a Quiz object given a name and a list of questions
        :param name: the name of the quiz
        :param question_list: the list of questions
        """

        self.name = name
        self.question_list = question_list

    def __str__(self) -> str:
        """
        Returns an easy-to-read string representation of this class
        :return: a string representation of this class
        """

        s = "Quiz Name: {}".format(self.name)
        for question in self.question_list:
            s += "\n\tQuestion: \"{}\"".format(question.question)
            s += "\n\t\tAnswer: \"{}\"".format(question.answer)
            s += "\n\t\tChoices: {}".format(question.choices)
            s += "\n\t\tSelected: {}\n".format(question.selected)

        return s


def get_quiz(path: str, quiz_name: str) -> 'Quiz' or None:
    # the select queries for both the quiz and questions
    quiz_query = "SELECT * FROM quiz WHERE name = :name"
    question_query = "SELECT * FROM question WHERE quiz_id = :id"

    # execute the queries to get the quiz and questions from the database
    try:
        quiz_result = db_helper.execute_query(path, quiz_query, {"name": quiz_name})

        try:
            question_result = db_helper.execute_query(path, question_query, {"id": quiz_result[0][0]})
        except sqlite3.OperationalError as ques_err:
            print("[GET QUESTION]: {}".format(ques_err))
            return None
    except sqlite3.OperationalError as quiz_err:
        print("[GET QUIZ]: {}".format(quiz_err))
        return None

    # start creating the quiz object
    questions = []
    for q in question_result:
        questions.append(Question(q[2], q[3], [q[4], q[5], q[6], q[7]], -1))

    return Quiz(quiz_result[0][1], questions)


def get_quiz_questions(path: str, quiz_name: str) -> list or None:
    # the select queries for both the quiz and questions
    quiz_query = "SELECT * FROM quiz WHERE name = :name"
    question_query = "SELECT * FROM question WHERE quiz_id = :id"

    # execute the queries to get the quiz and questions from the database
    try:
        quiz_result = db_helper.execute_query(path, quiz_query, {"name": quiz_name})

        try:
            return db_helper.execute_query(path, question_query, {"id": quiz_result[0][0]})
        except sqlite3.OperationalError as ques_err:
            print("[GET QUESTION]: {}".format(ques_err))
            return None
    except sqlite3.OperationalError as quiz_err:
        print("[GET QUIZ]: {}".format(quiz_err))
        return None


def get_all_quizzes(path: str) -> list or None:
    # the select queries for both the quiz and questions
    quiz_query = "SELECT * FROM quiz"

    # execute the queries to get the quiz and questions from the database
    try:
        quiz_result = db_helper.execute_query(path, quiz_query)
        try:
            quiz_question_result = []
            for quiz in quiz_result:
                quiz_question_result.append(get_quiz_questions(path, quiz[1]))
        except sqlite3.OperationalError as ques_err:
            print("[GET QUESTION]: {}".format(ques_err))
            return []
    except sqlite3.OperationalError as quiz_err:
        print("GET QUIZ]: {}".format(quiz_err))
        return []

    # a variable to hold a list of quiz objects
    quizzes = []

    # for each quiz in the database, create a quiz and add questions associated with it
    for i in range(len(quiz_result)):
        # construct a new quiz object
        quiz = Quiz(quiz_result[i][1], [])

        # add all the questions associated with this new quiz object
        for question in quiz_question_result[i]:
            quiz.question_list.append(
                Question(
                    question[2],
                    question[3],
                    [
                        question[4],
                        question[5],
                        question[6],
                        question[7]
                    ],
                    -1
                )
            )

        # add this newly created quiz object to the list of quizzes
        quizzes.append(quiz)

    # return the list of quizzes
    return quizzes


def insert_quiz(path: str, quiz_name: str) -> bool:
    # the query string and the arguments
    query = "INSERT INTO quiz VALUES(NULL, ?)"
    query_args = [quiz_name]

    # initialize the result boolean
    result = False

    # try to insert the quiz into the database, catch IntegrityError and OperationalError
    try:
        db_helper.execute_query(path, query, query_args)
        result = True
    except sqlite3.IntegrityError as err:
        print("[INSERT QUIZ - {}: {}]".format(type(err).__name__, err), end="")
    except sqlite3.OperationalError as err:
        print("[INSERT QUIZ -{}: {}]".format(type(err).__name__, err), end="")

    # return the resulting boolean
    return result


def update_quiz(quiz_name: str, question: Question):
    # execute an UPDATE statement to change a question in the quiz
    pass


def delete_quiz(quiz_name: str):
    # execute a DELETE statement to delete a quiz
    pass
