from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QStackedLayout, QLineEdit, QHBoxLayout, QMainWindow
from PyQt6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Movie Tracker")
        self.setGeometry(100, 100, 500, 300)

        #self.layout = QVBoxLayout()
        self.currentWindow = LoginWindow()
        #self.layout.addWidget(self.currentWindow)

        self.currentWindow.registerButton.clicked.connect(self.registerButton)

        self.setCentralWidget(self.currentWindow)
        self.show()


    def registerButton(self):
        self.currentWindow.close()
        self.currentWindow = RegisterWindow()
        self.setCentralWidget(self.currentWindow)
        self.currentWindow.button.clicked.connect(self.registerReturn)

    def registerReturn(self):
         self.currentWindow.close()
         self.currentWindow = LoginWindow()
         self.setCentralWidget(self.currentWindow)
         self.currentWindow.registerButton.clicked.connect(self.registerButton)



class LoginWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.statusLabel = QLabel("Welcome!")
        self.userLabel = QLabel("Username")
        self.passwordLabel = QLabel("Password")
        self.userBox = QLineEdit(self, placeholderText = "please enter your username", clearButtonEnabled=True, maxLength = 25)
        self.passwordBox = QLineEdit(self, placeholderText = "Please enter your password", clearButtonEnabled = True, echoMode = QLineEdit.EchoMode.Password)
        self.loginButton = QPushButton("Enter")
        self.registerButton = QPushButton("Register")
        self.showPasswordButton = QPushButton("Show Password")

        self.layout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.userLayout = QHBoxLayout()
        self.passwordLayout = QHBoxLayout()

        self.userLayout.addWidget(self.userLabel)
        self.userLayout.addWidget(self.userBox)

        self.passwordLayout.addWidget(self.passwordLabel)
        self.passwordLayout.addWidget(self.passwordBox)
        self.passwordLayout.addWidget(self.showPasswordButton)

        self.buttonLayout.addWidget(self.loginButton)
        self.buttonLayout.addWidget(self.registerButton)
        
        self.layout.addWidget(self.statusLabel)
        self.layout.addLayout(self.userLayout)
        self.layout.addLayout(self.passwordLayout)
        self.layout.addLayout(self.buttonLayout)

        self.showPasswordButton.clicked.connect(self.showPasswordToggle)

        self.setLayout(self.layout)

        #self.setAttribute(Qt.WA_DeleteOnClose)
    def showPasswordToggle(self):
        if(self.passwordBox.echoMode() == QLineEdit.EchoMode.Password):
            self.passwordBox.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordBox.setEchoMode(QLineEdit.EchoMode.Password)

                

class RegisterWindow(QWidget):
        def __init__(self, *args, **kwargs):
             super().__init__(*args,**kwargs)

             self.label = QLabel("This is the register window")
             self.button = QPushButton("Go back")

             layout = QVBoxLayout()

             layout.addWidget(self.label)
             layout.addWidget(self.button)

             self.setLayout(layout)

             #self.show()


        


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()


    sys.exit(app.exec())