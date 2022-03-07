from PyQt6.QtWidgets import QWidget, QPushButton, QFrame, QVBoxLayout, QLabel, QMainWindow, QApplication, \
    QHBoxLayout, QSizePolicy, QComboBox, QFormLayout, QLineEdit, QDialog, QDialogButtonBox, QGroupBox, QRadioButton
from PyQt6.QtCore import QRect, Qt, QSize
from PyQt6.QtGui import QFont

from src.model import Quiz as QuizFunc
from src.model import Question as QuesFunc
from src.controller import DatabaseHelper as db_helper


class QuizMainWindow(QMainWindow):
    def __init__(self):
        # normal setup
        super().__init__()
        self.path = "../app_data/quiz_app.db"
        self.all_quizzes = QuizFunc.get_all_quizzes(self.path)
        self.current_quiz = None

        # Attributes for the MainWindow
        self.setObjectName("mainWindow")
        self.setWindowTitle("QA - MGA Quiz Application")
        self.setFixedSize(QSize(1000, 650))

        # Central Widget
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralWidget")

        """
        ===================================================================
        START HEADER SECTION
        ===================================================================
        """
        # Vertical Box geometry
        self.vbox_widget = QWidget(self.centralwidget)
        self.vbox_widget.setGeometry(QRect(20, 10, 200, 80))
        self.vbox_widget.setObjectName("widget")

        # Vertical Box Layout for Logo
        self.logo_verticalLayout = QVBoxLayout(self.vbox_widget)
        self.logo_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.logo_verticalLayout.setObjectName("logo_verticalLayout")

        # Font to be used for the big logo
        font = QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setItalic(True)

        # Big Logo Label
        self.big_logo_label = QLabel(self.vbox_widget)
        self.big_logo_label.setFont(font)
        self.big_logo_label.setAlignment(
            Qt.AlignmentFlag.AlignLeading |
            Qt.AlignmentFlag.AlignLeft |
            Qt.AlignmentFlag.AlignTop
        )
        self.big_logo_label.setText("QA")
        self.big_logo_label.setObjectName("big_logo_label")

        # Sub Logo Label
        self.sub_logo_label = QLabel(self.vbox_widget)
        self.sub_logo_label.setObjectName("sub_logo_label")
        self.sub_logo_label.setText("Quiz Application")

        # Add the two logos to the vertical layout
        self.logo_verticalLayout.addWidget(self.big_logo_label)
        self.logo_verticalLayout.addWidget(self.sub_logo_label)

        # Header Separator Line
        self.header_line = QFrame(self.centralwidget)
        self.header_line.setGeometry(QRect(10, 90, 980, 20))
        self.header_line.setFrameShape(QFrame.Shape.HLine)
        self.header_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.header_line.setObjectName("header_line")
        """
        END HEADER SECTION
        """

        """
        START BODY SECTION
        =====================================================================================================
            This section will consist of a couple of different views:
                Select Quiz
                New Quiz/New Question
                Questions
        =====================================================================================================
        """
        """
        ================================================================================================================
            SELECT QUIZ SECTION
        ================================================================================================================
        """
        # Central Widget Attributes
        self.quizSelect_centralwidget = QWidget(self)
        self.quizSelect_centralwidget.setGeometry(QRect(25, 0, 950, 500))
        self.quizSelect_centralwidget.setObjectName("quizSelect_centralwidget")

        # Main Vertical Layout Attributes
        self.main_verticalLayout = QVBoxLayout(self.quizSelect_centralwidget)
        self.main_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_verticalLayout.setObjectName("main_verticalLayout")

        """
        Horizontal Layout Attributes
            Question Label
        """
        self.questionLabel_horizontalLayout = QHBoxLayout()
        self.questionLabel_horizontalLayout.setObjectName("questionLabel_horizontalLayout")

        # Question Label Attributes - Child of above horizontal layout
        self.question_label = QLabel(self.quizSelect_centralwidget)
        question_size_policy = QSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred
        )
        question_size_policy.setHeightForWidth(
            self.question_label.sizePolicy().hasHeightForWidth()
        )
        self.question_label.setSizePolicy(question_size_policy)
        self.question_label.setMinimumSize(QSize(0, 0))
        self.question_label.setMaximumSize(QSize(800, 100))
        font = QFont()
        font.setPointSize(16)
        self.question_label.setFont(font)
        self.question_label.setScaledContents(False)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setObjectName("question_label")
        self.question_label.setText("Select a Quiz or Add a New One")

        # Add question label to horizontal layout
        self.questionLabel_horizontalLayout.addWidget(self.question_label)

        # Add question label horizontal layout to main vertical layout
        self.main_verticalLayout.addLayout(self.questionLabel_horizontalLayout)

        """
        Horizontal Layout Attributes
            Choices ComboBox
        """
        self.combobox_horizontalLayout = QHBoxLayout()
        self.combobox_horizontalLayout.setObjectName("combobox_horizontalLayout")

        # ComboBox Attributes
        self.choice_comboBox = QComboBox(self.quizSelect_centralwidget)
        choice_size_policy = QSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )
        choice_size_policy.setHeightForWidth(
            self.choice_comboBox.sizePolicy().hasHeightForWidth()
        )
        self.choice_comboBox.setSizePolicy(choice_size_policy)
        self.choice_comboBox.setMinimumSize(QSize(400, 35))
        font = QFont()
        font.setPointSize(12)
        self.choice_comboBox.setFont(font)
        self.choice_comboBox.setObjectName("comboBox")
        self.choice_comboBox.setPlaceholderText("Select-One")
        self.choice_comboBox.currentIndexChanged.connect(self.load_quiz)
        for item in QuizFunc.get_all_quizzes(self.path):
            self.choice_comboBox.addItem(item.name)

        # Add combobox to horizontal layout and then add the horizontal layout
        # to the main vertical layout
        self.combobox_horizontalLayout.addWidget(self.choice_comboBox)
        self.main_verticalLayout.addLayout(self.combobox_horizontalLayout)

        """
        Horizontal Layout Attributes
            PushButton
            PushButton
        """
        self.prev_next_pushButton_hlayout = QHBoxLayout()
        self.prev_next_pushButton_hlayout.setObjectName("prev_next_pushButton_hlayout")

        # PushButton Attributes
        self.start_pushButton = QPushButton(self.quizSelect_centralwidget)
        start_sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )
        start_sizePolicy.setHeightForWidth(self.start_pushButton.sizePolicy().hasHeightForWidth())
        self.start_pushButton.setSizePolicy(start_sizePolicy)
        self.start_pushButton.setMinimumSize(QSize(110, 25))
        self.start_pushButton.setObjectName("start_pushButton")
        self.start_pushButton.setText("Start")

        # Add the START button to the hlayout
        self.prev_next_pushButton_hlayout.addWidget(self.start_pushButton)

        # Set up the NEW QUIZ button
        self.new_quiz_pushButton = QPushButton(self.quizSelect_centralwidget)
        new_quiz_sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )
        new_quiz_sizePolicy.setHeightForWidth(self.new_quiz_pushButton.sizePolicy().hasHeightForWidth())
        self.new_quiz_pushButton.setSizePolicy(new_quiz_sizePolicy)
        self.new_quiz_pushButton.setMinimumSize(QSize(110, 25))
        self.new_quiz_pushButton.setObjectName("new_quiz_pushButton")
        self.new_quiz_pushButton.setText("New Quiz")
        self.new_quiz_pushButton.clicked.connect(self.show_new_quiz_screen)

        # Add the NEW QUIZ button to the hlayout
        self.prev_next_pushButton_hlayout.addWidget(self.new_quiz_pushButton)

        # Add the hlayout to the main vertical layout
        self.main_verticalLayout.addLayout(self.prev_next_pushButton_hlayout)

        """
        ================================================================================================================
            NEW QUIZ/QUESTION SECTION
        ================================================================================================================
        """
        self.new_quiz_ques_layoutWidget = QWidget(self)
        self.new_quiz_ques_layoutWidget.setGeometry(QRect(20, 130, 861, 411))
        self.new_quiz_ques_layoutWidget.setObjectName("new_quiz_ques_layoutWidget")
        self.new_quiz_ques_layoutWidget.setVisible(False)

        self.new_quiz_ques_vLayout = QVBoxLayout(self.new_quiz_ques_layoutWidget)
        self.new_quiz_ques_vLayout.setContentsMargins(0, 0, 0, 0)
        self.new_quiz_ques_vLayout.setObjectName("new_quiz_ques_vLayout")

        self.new_quiz_ques_hLayout = QHBoxLayout()
        self.new_quiz_ques_hLayout.setObjectName("new_quiz_ques_hLayout")

        self.new_quiz_ques_label = QLabel(self.new_quiz_ques_layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.new_quiz_ques_label.setMinimumSize(0, 200)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_quiz_ques_label.sizePolicy().hasHeightForWidth())
        self.new_quiz_ques_label.setSizePolicy(sizePolicy)
        self.new_quiz_ques_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.new_quiz_ques_label.setObjectName("new_quiz_ques_label")
        self.new_quiz_ques_label.setText("New Quiz or Question?")
        self.new_quiz_ques_hLayout.addWidget(self.new_quiz_ques_label)

        self.new_quiz_ques_vLayout.addLayout(self.new_quiz_ques_hLayout)

        """
        New Question Form
        """
        self.question_form = QFormLayout()
        self.question_form.setObjectName("question_form")

        self.question_form_quiz_label = QLabel(self.new_quiz_ques_layoutWidget)
        self.question_form_quiz_label.setObjectName("question_form_quiz_label")
        self.question_form_quiz_label.setText("Quiz:")
        self.question_form.setWidget(0, QFormLayout.ItemRole.LabelRole, self.question_form_quiz_label)

        self.question_form_quiz_comboBox = QComboBox(self.new_quiz_ques_layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.question_form_quiz_comboBox.sizePolicy().hasHeightForWidth())
        self.question_form_quiz_comboBox.setSizePolicy(sizePolicy)
        self.question_form_quiz_comboBox.setMinimumSize(QSize(300, 0))
        self.question_form_quiz_comboBox.setObjectName("question_form_quiz_comboBox")
        for item in QuizFunc.get_all_quizzes(self.path):
            self.question_form_quiz_comboBox.addItem(item.name)
        self.question_form.setWidget(0, QFormLayout.ItemRole.FieldRole, self.question_form_quiz_comboBox)

        self.question_form_question_label = QLabel(self.new_quiz_ques_layoutWidget)
        self.question_form_question_label.setObjectName("question_form_question_label")
        self.question_form_question_label.setText("Question:")
        self.question_form.setWidget(1, QFormLayout.ItemRole.LabelRole, self.question_form_question_label)

        self.question_form_question_lineEdit = QLineEdit(self.new_quiz_ques_layoutWidget)
        self.question_form_question_lineEdit.setObjectName("question_form_question_lineEdit")
        self.question_form.setWidget(1, QFormLayout.ItemRole.FieldRole, self.question_form_question_lineEdit)

        self.question_form_answer_label = QLabel(self.new_quiz_ques_layoutWidget)
        self.question_form_answer_label.setObjectName("question_form_answer_label")
        self.question_form_answer_label.setText("Answer")
        self.question_form.setWidget(2, QFormLayout.ItemRole.LabelRole, self.question_form_answer_label)

        self.question_form_answer_lineEdit = QLineEdit(self.new_quiz_ques_layoutWidget)
        self.question_form_answer_lineEdit.setObjectName("question_form_answer_lineEdit")
        self.question_form.setWidget(2, QFormLayout.ItemRole.FieldRole, self.question_form_answer_lineEdit)

        self.question_form_choice1_label = QLabel(self.new_quiz_ques_layoutWidget)
        self.question_form_choice1_label.setObjectName("question_form_choice1_label")
        self.question_form_choice1_label.setText("Choice1:")
        self.question_form.setWidget(3, QFormLayout.ItemRole.LabelRole, self.question_form_choice1_label)

        self.question_form_choice1_lineEdit = QLineEdit(self.new_quiz_ques_layoutWidget)
        self.question_form_choice1_lineEdit.setObjectName("question_form_choice1_lineEdit")
        self.question_form.setWidget(3, QFormLayout.ItemRole.FieldRole, self.question_form_choice1_lineEdit)

        self.question_form_choice2_label = QLabel(self.new_quiz_ques_layoutWidget)
        self.question_form_choice2_label.setObjectName("question_form_choice2_label")
        self.question_form_choice2_label.setText("Choice2:")
        self.question_form.setWidget(4, QFormLayout.ItemRole.LabelRole, self.question_form_choice2_label)

        self.question_form_choice2_lineEdit = QLineEdit(self.new_quiz_ques_layoutWidget)
        self.question_form_choice2_lineEdit.setObjectName("question_form_choice2_lineEdit")
        self.question_form.setWidget(4, QFormLayout.ItemRole.FieldRole, self.question_form_choice2_lineEdit)

        self.question_form_choice3_label = QLabel(self.new_quiz_ques_layoutWidget)
        self.question_form_choice3_label.setObjectName("question_form_choice3_label")
        self.question_form_choice3_label.setText("Choice3:")
        self.question_form.setWidget(5, QFormLayout.ItemRole.LabelRole, self.question_form_choice3_label)

        self.question_form_choice3_lineEdit = QLineEdit(self.new_quiz_ques_layoutWidget)
        self.question_form_choice3_lineEdit.setObjectName("question_form_choice3_lineEdit")
        self.question_form.setWidget(5, QFormLayout.ItemRole.FieldRole, self.question_form_choice3_lineEdit)

        self.question_form_choice4_label = QLabel(self.new_quiz_ques_layoutWidget)
        self.question_form_choice4_label.setObjectName("question_form_choice4_label")
        self.question_form_choice4_label.setText("Choice4:")
        self.question_form.setWidget(6, QFormLayout.ItemRole.LabelRole, self.question_form_choice4_label)

        self.question_form_choice4_lineEdit = QLineEdit(self.new_quiz_ques_layoutWidget)
        self.question_form_choice4_lineEdit.setObjectName("question_form_choice4_lineEdit")
        self.question_form.setWidget(6, QFormLayout.ItemRole.FieldRole, self.question_form_choice4_lineEdit)

        self.new_quiz_ques_vLayout.addLayout(self.question_form)

        self.new_ques_submit_pushButton = QPushButton(self.new_quiz_ques_layoutWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_ques_submit_pushButton.sizePolicy().hasHeightForWidth())
        self.new_ques_submit_pushButton.setSizePolicy(sizePolicy)
        self.new_ques_submit_pushButton.setMinimumSize(QSize(150, 35))
        self.new_ques_submit_pushButton.setObjectName("new_quiz_ques_submit_pushButton")
        self.new_ques_submit_pushButton.setText("Add New Question:")
        self.new_ques_submit_pushButton.clicked.connect(self.add_new_question)

        self.new_quiz_ques_vLayout.addWidget(self.new_ques_submit_pushButton)

        """
        ================================================================================================================
            QUESTIONS SECTION
        ================================================================================================================
        """
        self.take_quiz_widget = QWidget(self.centralwidget)
        self.take_quiz_widget.setGeometry(QRect(210, 150, 561, 391))
        self.take_quiz_widget.setObjectName("take_quiz_widget")
        self.take_quiz_widget.setVisible(False)


        self.quiz_question_main_vLayout = QVBoxLayout(self.take_quiz_widget)
        self.quiz_question_main_vLayout.setContentsMargins(0, 0, 0, 0)
        self.quiz_question_main_vLayout.setObjectName("quiz_question_main_vLayout")

        self.question_label = QLabel(self.take_quiz_widget)
        self.question_label.setObjectName("question_label")
        self.quiz_question_main_vLayout.addWidget(self.question_label)

        self.choices_groupBox = QGroupBox(self.take_quiz_widget)
        self.choices_groupBox.setTitle("")
        self.choices_groupBox.setObjectName("choices_groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.choices_groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.choice1_radioButton = QRadioButton(self.choices_groupBox)
        self.choice1_radioButton.setObjectName("choice1_radioButton")
        self.verticalLayout_2.addWidget(self.choice1_radioButton)

        self.choice2_radioButton = QRadioButton(self.choices_groupBox)
        self.choice2_radioButton.setObjectName("choice2_radioButton")
        self.verticalLayout_2.addWidget(self.choice2_radioButton)

        self.choice3_radioButton = QRadioButton(self.choices_groupBox)
        self.choice3_radioButton.setObjectName("choice3_radioButton")
        self.verticalLayout_2.addWidget(self.choice3_radioButton)

        self.choice4_radioButton = QRadioButton(self.choices_groupBox)
        self.choice4_radioButton.setObjectName("choice4_radioButton")
        self.verticalLayout_2.addWidget(self.choice4_radioButton)

        self.quiz_question_main_vLayout.addWidget(self.choices_groupBox)

        self.prev_next_hLayout = QHBoxLayout()
        self.prev_next_hLayout.setObjectName("prev_next_hLayout")

        self.previous_pushButton = QPushButton(self.take_quiz_widget)
        self.previous_pushButton.setObjectName("previous_pushButton")
        self.prev_next_hLayout.addWidget(self.previous_pushButton)

        self.next_pushButton = QPushButton(self.take_quiz_widget)
        self.next_pushButton.setObjectName("next_pushButton")
        self.prev_next_hLayout.addWidget(self.next_pushButton)

        self.quiz_question_main_vLayout.addLayout(self.prev_next_hLayout)

        self.finish_pushButton = QPushButton(self.take_quiz_widget)
        self.finish_pushButton.setObjectName("finish_pushButton")

        self.quiz_question_main_vLayout.addWidget(self.finish_pushButton)

        """
        END BODY SECTION
        """

        """
        START FOOTER SECTION
        """
        # Footer Separator Line
        self.footer_line = QFrame(self.centralwidget)
        self.footer_line.setGeometry(QRect(10, 580, 980, 20))
        self.footer_line.setFrameShape(QFrame.Shape.HLine)
        self.footer_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.footer_line.setObjectName("footer_line")

        # Home Push Button
        self.home_pushButton = QPushButton(self.centralwidget)
        self.home_pushButton.setGeometry(QRect(450, 600, 100, 30))
        self.home_pushButton.setObjectName("home_pushButton")
        self.home_pushButton.setText("Home")
        self.home_pushButton.clicked.connect(self.show_main_screen)

        # Feedback label when adding new items to the database
        self.feedback_label = QLabel(self.centralwidget)
        self.feedback_label.setObjectName("feedback_label")
        self.feedback_label.setGeometry(QRect(10, 600, 150, 20))
        self.feedback_label.setText("Good")

        """
        END FOOTER SECTION
        """

        """
        FINAL REQUIRED CODE
        """
        # Set the central widget for the main window
        self.setCentralWidget(self.centralwidget)

    """
    When the home button is clicked, change the view to show the main screen
    """
    def show_main_screen(self):
        self.new_quiz_ques_layoutWidget.setVisible(False)
        self.question_form_quiz_comboBox.setCurrentText("")
        self.question_form_question_lineEdit.setText("")
        self.question_form_answer_lineEdit.setText("")
        self.question_form_choice1_lineEdit.setText("")
        self.question_form_choice2_lineEdit.setText("")
        self.question_form_choice3_lineEdit.setText("")
        self.question_form_choice4_lineEdit.setText("")

        self.quizSelect_centralwidget.setVisible(True)

    def show_new_quiz_screen(self):
        self.quizSelect_centralwidget.setVisible(False)
        self.new_quiz_ques_layoutWidget.setVisible(True)

    def add_new_question(self):
        quiz = self.question_form_quiz_comboBox.currentIndex()
        question = self.question_form_question_lineEdit.text()
        answer = self.question_form_answer_lineEdit.text()
        choice1 = self.question_form_choice1_lineEdit.text()
        choice2 = self.question_form_choice2_lineEdit.text()
        choice3 = self.question_form_choice3_lineEdit.text()
        choice4 = self.question_form_choice4_lineEdit.text()

        if quiz == "" or \
            question == "" or \
            answer == "" or \
            choice1 == "" or \
            choice2 == "" or \
            choice3 == "" or \
            choice4 == "":
            self.feedback_label.setText("Bad Input: Try Again.")
        else:
            result = QuesFunc.insert_question(
                self.path,
                quiz,
                question,
                answer,
                [choice1, choice2, choice3, choice4]
            )

            self.feedback_label.setText("Adding question: {}".format(result))

    def load_quiz(self, index):
        self.current_quiz = self.all_quizzes[index]
        questions = db_helper.execute_query(self.path, "SELECT * FROM question WHERE quiz_id = :qid", {"qid": index + 1})
        print(questions)


if __name__ == "__main__":
    app = QApplication([])
    window = QuizMainWindow()
    window.show()
    app.exec()
