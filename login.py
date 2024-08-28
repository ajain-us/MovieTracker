from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QStackedLayout, QLineEdit, QHBoxLayout
import sys

class LoginWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.setGeometry(0,0,500,500)

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

        self.show()



        


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = LoginWindow()


    sys.exit(app.exec())