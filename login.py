from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QStackedLayout, QLineEdit, QHBoxLayout, QMainWindow
from PyQt6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Movie Tracker")
        self.setGeometry(460, 40, 500, 500)

        self.layout = QVBoxLayout()
        self.currentWindow = LoginWindow()
        self.layout.addWidget(self.currentWindow)

        self.currentWindow.loginButton.clicked.connect(self.loginEnter)

        self.setLayout(self.layout)
        self.show
    def loginEnter(self):
        print("wow does this work")
        self.currentWindow.close()
        self.currentWindow = SecondWindow()


class LoginWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        #self.setGeometry(0,0,500,500)

        self.userBox = QLineEdit(self, placeholderText = "please enter your username", clearButtonEnabled=True, maxLength = 25)
        self.passwordBox = QLineEdit(self, placeholderText = "Please enter your password", clearButtonEnabled = True, echoMode = QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.loginButton = QPushButton("Enter")
        self.registerButton = QPushButton("Register")

        self.layout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.buttonLayout.addWidget(self.loginButton)
        self.buttonLayout.addWidget(self.registerButton)
        

        self.layout.addWidget(self.userBox)
        self.layout.addWidget(self.passwordBox)
        self.layout.addLayout(self.buttonLayout)

        self.setLayout(self.layout)

        #self.setAttribute(Qt.WA_DeleteOnClose)

        self.show()

class SecondWindow(QWidget):
        def __init__(self, *args, **kwargs):
             super().__init__(*args,**kwargs)

             label = QLabel("this is a label!")
             button = QPushButton("Hide and Show!")

             layout = QVBoxLayout()

             layout.addWidget(label)
             layout.addWidget(button)

             self.setLayout(layout)

             self.show()


        


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()


    sys.exit(app.exec())