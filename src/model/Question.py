import sqlite3
import src.controller.DatabaseHelper as db_helper


class Question:
    def __init__(self, question: str, answer: str, choices: list, selected: int):
        """
        Constructs a Question object given the question text, answer, a list of
        choices, and the currently selected answer.
        :param question: question text
        :param answer: answer text
        :param choices: choice list, includes the answer
        :param selected: selected choice, -1 for none
        """

        self.question = question
        self.answer = answer
        self.choices = choices
        self.selected = selected

    def __str__(self) -> str:
        """
        Returns the easy-to-read string representation of this class
        :return: the string representation of a Question object
        """

        return "question={}\nanswer={}\nchoices={}\nselected={}"\
            .format(self.question, self.answer, self.choices, self.selected)

    def __eq__(self, other):
        """
        Compares two Question objects
        :param other: the other Question object
        :return: true if both are the same
        """

        # compare the two questions based on their question text, answer text, and choices
        if self.question == other.question and self.answer == other.answer and self.choices == other.choices:
            return True
        else:
            return False


def insert_question(path: str, quiz_id: int, question: str, answer: str, choices: list) -> bool:
    """
    Inserts a question into the question database
    :param path: the database path
    :param quiz_id: the quiz id to associate the question with
    :param question: the question text
    :param answer: the answer text
    :param choices: list of choices, including the answer
    :return: True if the insertion was successful, otherwise False
    """

    # the query string and the arguments
    query = "INSERT INTO question VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)"
    query_args = [quiz_id, question, answer, choices[0], choices[1], choices[2], choices[3]]

    # initialize the result boolean
    result = False

    # try to insert the question into the database, catch IntegrityError and OperationalError
    try:
        db_helper.execute_query(path, query, query_args)
        result = True
    except sqlite3.IntegrityError as err:
        pass
        # print("[INSERT QUESTION - {}: {}] ".format(type(err).__name__, err), end="")
    except sqlite3.OperationalError as err:
        pass
        # print("[INSERT QUESTION - {}: {}] ".format(type(err).__name__, err), end="")

    # return the resulting boolean
    return result


def get_all(path: str) -> list:
    """
    Gets all the questions in the question table of the main database
    :param path: the database path
    :return: a list of questions from the database
    """

    # the select query
    query = "SELECT * FROM question"

    # initialize the result list
    result = []

    # try to insert the question into the database, catch an OperationalError
    try:
        result = db_helper.execute_query(path, query)
    except sqlite3.OperationalError as err:
        print("[SELECT QUESTION - OperationalError: {}] ".format(err), end="")

    # return the resulting list
    return result
