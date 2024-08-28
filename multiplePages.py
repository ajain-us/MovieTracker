from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QStackedLayout
import sys


class LoginScreen(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        layout = QVBoxLayout()
        self.label = QLabel("Logged In!")
        self.button = QPushButton("Log Out")
        self.button.clicked.connect(self.hide)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.setWindowTitle("Movie Tracker")
        self.setGeometry(700, 350, 500, 500)
        self.button = QPushButton("Login")
        self.button.clicked.connect(self.loginPressed)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.show()


        self.show()
    def loginPressed(self):
        self.login = LoginScreen()
        self.login.show()
        


class Main(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.mainPage = MainWindow()
        self.loginPage = LoginScreen()

        self.setWindowTitle("Testing 1 2 3")

        self.stackedLayout = QStackedLayout()
        self.stackedLayout.addWidget(self.mainPage)
        self.stackedLayout.addWidget(self.loginPage)   

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.stackedLayout)
        self.setLayout(self.mainLayout)

        self.show()     

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Main()

    print("hello world")

    sys.exit(app.exec())