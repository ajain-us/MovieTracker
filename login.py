from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QMainWindow, QStyleFactory, QListWidget, QTableWidget
from PyQt6.QtCore import Qt
import sys, pyodbc



connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={'movie-tracker-aj.database.windows.net'};DATABASE={'movie tracker aj'};UID={'adminsql'};PWD={'&yHASu9NFf?87vz'}'
connection = pyodbc.connect(connectionString)
cursor = connection.cursor()

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
         self.centralWidget().loginButton.clicked.connect(self.loginButton)

    def loginButton(self):
        if not (self.centralWidget().userBox.text() and self.centralWidget().passwordBox.text()):
            self.centralWidget().statusLabel.setText("### Please enter a valid username and password")
            return
        queryString = "SELECT * FROM Logins WHERE Username = '" + self.centralWidget().userBox.text() + "'"
        #print(queryString)
        cursor.execute(queryString)
        loginRow = cursor.fetchall()
        # Need to run SQL query "Select * FROM logins WHERE Username = self.centralWidget().userBox.text()"
        if not loginRow:
            self.centralWidget().statusLabel.setText("### Username not found, please try again")
            return
        
        if self.centralWidget().passwordBox.text() == loginRow[0].Password:
            self.centralWidget().statusLabel.setText("### Logging you in!")
            self.centralWidget().close()
            self.setCentralWidget(InfoWindow(loginRow[0].Username))
            self.centralWidget().logoutButton.clicked.connect(self.logoutButton)
        else:
            self.centralWidget().statusLabel.setText("### That password is wrong")
        
        #print(loginRow[0].Password)
    def logoutButton(self):
        self.centralWidget().close()
        self.setCentralWidget(LoginWindow())
        self.centralWidget().registerButton.clicked.connect(self.registerButton)
        self.centralWidget().loginButton.clicked.connect(self.loginButton)



        



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
             self.registerButton.clicked.connect(self.register)

             self.setLayout(layout)

        def showPasswordToggle(self):
            if(self.passwordBox.echoMode() == QLineEdit.EchoMode.Password):
                self.passwordBox.setEchoMode(QLineEdit.EchoMode.Normal)
            else:
                self.passwordBox.setEchoMode(QLineEdit.EchoMode.Password)

             #self.show()
        def register(self):
            if not (self.userBox.text() and self.passwordBox.text()):
                self.statusLabel.setText("### Please enter a valid username and password")
                return
            queryString = "SELECT * FROM Logins WHERE Username = '" + self.userBox.text() + "'"
            #print(queryString)
            cursor.execute(queryString)
            loginRow = cursor.fetchall()
            if not loginRow:
                #add the login
                queryString = "INSERT INTO Logins (Username, Password) VALUES ('" + self.userBox.text() + "', '" + self.passwordBox.text() +"');"
                cursor.execute(queryString)
                connection.commit()
                self.statusLabel.setText("### User added, please return to login")
            else:
                self.statusLabel.setText("### This username is already taken")
                return


class InfoWindow(QWidget):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.nameLabel = QLabel("Logged in as: " + name)
        self.logoutButton = QPushButton("Logout")
        self.addShow = QPushButton("Add")
        self.deleteShow = QPushButton("Delete")
        self.saveButton = QPushButton("Save")
        self.list = QListWidget()
        self.shows = []

        queryString = "SELECT * FROM shows WHERE Username = '" + name + "'"
        cursor.execute(queryString)
        showsInfo = cursor.fetchall()

        for show in showsInfo:
            self.shows.append(Item(show.Title, show.WatchStatus, show.Rating, show.TotalEpisodes, show.CurrentEpisode))
            self.list.addItem(show.Title)

        


        #queryString = ""
        middleLayout = QHBoxLayout()
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.addShow)
        buttonLayout.addWidget(self.deleteShow)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.logoutButton)

        middleLayout.addWidget(self.list)
        middleLayout.addLayout(buttonLayout)

        layout = QVBoxLayout()
        layout.addWidget(self.nameLabel)
        layout.addLayout(middleLayout)
        
        

        self.setLayout(layout)

class addShowWindow(QWidget):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.titleLabel = QLabel("Title:")
        self.statusLabel = QLabel("Watch Status:")
        self.ratingLabel = QLabel("Rating:")
        self.totalEpisodesLabel = QLabel("Total Episodes:")
        self.currentEpisodeLabel = QLabel("Current Episode:")



class Item():
    def __init__(self, title, status, rating, totalEpisodes, currentEpisode):
        super().__init__()
        self.title = title
        self.status = status
        self.rating = rating
        self.totalEpisodes = totalEpisodes
        self.currentEpisode = currentEpisode
    

        

        


if __name__ == '__main__':
    

    app = QApplication(sys.argv)
    for x in QStyleFactory.keys():
        print(x)
    app.setStyle(QStyleFactory.create("fusion"))

    window = MainWindow()


    sys.exit(app.exec())