from PyQt6.QtWidgets import QApplication

from src.model.Question import Question
from src.model.Quiz import Quiz
from src.model import Quiz as QuizFunc
from src.model import Question as QuestionFunc

from src.controller import DatabaseHelper

from src.view.quiz_mainwindow import QuizMainWindow

# Initialize the database by tyring to add a quiz and question table
path = "../app_data/quiz_app.db"
DatabaseHelper.create_table(
    path,
    "quiz",
    "id INTEGER PRIMARY KEY, name TEXT"
)
DatabaseHelper.create_table(
    path,
    "question",
    "id INTEGER PRIMARY KEY, quiz_id INTEGER, question TEXT, answer TEXT, choice1 TEXT, choice2, TEXT, choice3 TEXT, choice4 TEXT"
)


# Start the main view
if __name__ == "__main__":
    app = QApplication([])
    window = QuizMainWindow()
    window.show()
    app.exec()
