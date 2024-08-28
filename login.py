from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QMainWindow, QStyleFactory
from PyQt6.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Movie Tracker")
        self.setGeometry(100, 100, 350, 100)

        
        self.setCentralWidget(LoginWindow())
        self.centralWidget().registerButton.clicked.connect(self.registerButton)

        self.show()


    def registerButton(self):
        self.centralWidget().close()
        self.setCentralWidget(RegisterWindow())
        self.centralWidget().returnButton.clicked.connect(self.registerReturn)

    def registerReturn(self):
         self.centralWidget().close()
         self.setCentralWidget(LoginWindow())
         self.centralWidget().registerButton.clicked.connect(self.registerButton)



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

             self.layout = QVBoxLayout()
             self.buttonLayout = QHBoxLayout()
             self.userLayout = QHBoxLayout()
             self.passwordLayout = QHBoxLayout()

             self.userLayout.addWidget(self.userLabel)
             self.userLayout.addWidget(self.userBox)

             self.passwordLayout.addWidget(self.passwordLabel)
             self.passwordLayout.addWidget(self.passwordBox)
             self.passwordLayout.addWidget(self.showPasswordButton)

             self.buttonLayout.addWidget(self.returnButton)
             self.buttonLayout.addWidget(self.registerButton)

             layout = QVBoxLayout()

             layout.addWidget(self.statusLabel)
             layout.addLayout(self.userLayout)
             layout.addLayout(self.passwordLayout)
             layout.addLayout(self.buttonLayout)

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