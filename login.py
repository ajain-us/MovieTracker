from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QMainWindow, QStyleFactory
from PyQt6.QtCore import Qt
import sys, os, pyodbc, struct, pandas as pd
from pydantic import BaseModel


#connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
#connection = pyodbc.connection(connectionString)
#cursor = connection.cursor()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Movie Tracker")
        self.setGeometry(100, 100, 350, 100)

        
        self.setCentralWidget(LoginWindow())
        self.centralWidget().registerButton.clicked.connect(self.registerButton)
        self.centralWidget().loginButton.clicked.connect(self.loginButton)

        self.show()


    def registerButton(self):
        self.centralWidget().close()
        self.setCentralWidget(RegisterWindow())
        self.centralWidget().returnButton.clicked.connect(self.registerReturn)

    def registerReturn(self):
         self.centralWidget().close()
         self.setCentralWidget(LoginWindow())
         self.centralWidget().registerButton.clicked.connect(self.registerButton)

    def loginButton(self):
        if not (self.centralWidget().userBox.text() and self.centralWidget().passwordBox.text()):
            self.centralWidget().statusLabel.setText("### Please enter a valid username and password")
        # Need to run SQL query "Select * FROM logins WHERE Username = self.centralWidget().userBox.text()"
        # 

        
        



class LoginWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.statusLabel = QLabel("# Login")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.statusLabel.setTextFormat(Qt.TextFormat.MarkdownText)

        self.userLabel = QLabel("Username")
        self.passwordLabel = QLabel("Password")
        self.userBox = QLineEdit(self, placeholderText = "please enter your username", clearButtonEnabled=True, maxLength = 25)
        self.passwordBox = QLineEdit(self, placeholderText = "Please enter your password", clearButtonEnabled = True, echoMode = QLineEdit.EchoMode.Password)
        self.loginButton = QPushButton("Enter")
        self.registerButton = QPushButton("Register")
        self.showPasswordButton = QPushButton("Show Password")

        layout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        userLayout = QHBoxLayout()
        passwordLayout = QHBoxLayout()

        userLayout.addWidget(self.userLabel)
        userLayout.addWidget(self.userBox)

        passwordLayout.addWidget(self.passwordLabel)
        passwordLayout.addWidget(self.passwordBox)
        passwordLayout.addWidget(self.showPasswordButton)

        buttonLayout.addWidget(self.loginButton)
        buttonLayout.addWidget(self.registerButton)
        
        layout.addWidget(self.statusLabel)
        layout.addLayout(userLayout)
        layout.addLayout(passwordLayout)
        layout.addLayout(buttonLayout)

        self.showPasswordButton.clicked.connect(self.showPasswordToggle)

        self.setLayout(layout)

        #self.setAttribute(Qt.WA_DeleteOnClose)
    def showPasswordToggle(self):
        if(self.passwordBox.echoMode() == QLineEdit.EchoMode.Password):
            self.passwordBox.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordBox.setEchoMode(QLineEdit.EchoMode.Password)

                

class RegisterWindow(QWidget):
        def __init__(self, *args, **kwargs):
             super().__init__(*args,**kwargs)

             self.statusLabel = QLabel("# Registration")
             self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
             self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
             self.statusLabel.setTextFormat(Qt.TextFormat.MarkdownText)

             self.userLabel = QLabel("Username")
             self.passwordLabel = QLabel("Password")

             self.userBox = QLineEdit(self, placeholderText = "please enter your username", clearButtonEnabled=True, maxLength = 25)
             self.passwordBox = QLineEdit(self, placeholderText = "Please enter your password", clearButtonEnabled = True, echoMode = QLineEdit.EchoMode.Password)

             self.showPasswordButton = QPushButton("Show Password")
             self.returnButton = QPushButton("Return to Login")
             self.registerButton = QPushButton("Register")

             layout = QVBoxLayout()
             buttonLayout = QHBoxLayout()
             userLayout = QHBoxLayout()
             passwordLayout = QHBoxLayout()

             userLayout.addWidget(self.userLabel)
             userLayout.addWidget(self.userBox)

             passwordLayout.addWidget(self.passwordLabel)
             passwordLayout.addWidget(self.passwordBox)
             passwordLayout.addWidget(self.showPasswordButton)

             buttonLayout.addWidget(self.returnButton)
             buttonLayout.addWidget(self.registerButton)

             layout = QVBoxLayout()

             layout.addWidget(self.statusLabel)
             layout.addLayout(userLayout)
             layout.addLayout(passwordLayout)
             layout.addLayout(buttonLayout)

             self.showPasswordButton.clicked.connect(self.showPasswordToggle)

             self.setLayout(layout)

        def showPasswordToggle(self):
            if(self.passwordBox.echoMode() == QLineEdit.EchoMode.Password):
                self.passwordBox.setEchoMode(QLineEdit.EchoMode.Normal)
            else:
                self.passwordBox.setEchoMode(QLineEdit.EchoMode.Password)

             #self.show()


        


if __name__ == '__main__':
    

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Windows"))

    window = MainWindow()


    sys.exit(app.exec())