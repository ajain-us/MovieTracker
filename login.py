from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QMainWindow, QStyleFactory, QTableWidgetItem, QTableWidget, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
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


        self.name = name;
        self.nameLabel = QLabel("Logged in as: " + name)
        self.logoutButton = QPushButton("Logout")
        self.addShow = QPushButton("Add")
        self.deleteShow = QPushButton("Delete")
        self.editButton = QPushButton("Edit")
        self.showsTable = QTableWidget()
        
        self.shows = []

        self.showsTable.setColumnCount(4)
        self.showsTable.setHorizontalHeaderLabels(["Name", "Status", "Rating", "Episodes"])

        queryString = "SELECT * FROM shows WHERE Username = '" + name + "'"
        cursor.execute(queryString)
        showsInfo = cursor.fetchall()

        #Item(show.Title, show.WatchStatus, show.Rating, show.TotalEpisodes, show.CurrentEpisode)

        for show in showsInfo:
            self.shows.append(Item(show.Title, show.WatchStatus, show.Rating, show.TotalEpisodes, show.CurrentEpisode))
            self.showsTable.setRowCount(self.showsTable.rowCount() + 1)
            tableWidgets = [QTableWidgetItem(show.Title),QTableWidgetItem(show.WatchStatus), QTableWidgetItem(str(show.Rating)), QTableWidgetItem(str(show.CurrentEpisode) + "/" + str(show.TotalEpisodes))]
            for aspect in tableWidgets:
                aspect.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                aspect.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.showsTable.setItem(self.showsTable.rowCount()-1, 0, tableWidgets[0])
            self.showsTable.setItem(self.showsTable.rowCount()-1, 1, tableWidgets[1])
            self.showsTable.setItem(self.showsTable.rowCount()-1, 2, tableWidgets[2])
            self.showsTable.setItem(self.showsTable.rowCount()-1, 3, tableWidgets[3])
        #tableWidget.cellDoubleClicked.connect(on_cell_double_clicked) and this function takes in (row: int, column: int)
        middleLayout = QHBoxLayout()
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.addShow)
        buttonLayout.addWidget(self.deleteShow)
        buttonLayout.addWidget(self.editButton)
        buttonLayout.addWidget(self.logoutButton)

        middleLayout.addWidget(self.showsTable)
        middleLayout.addLayout(buttonLayout)

        layout = QVBoxLayout()
        layout.addWidget(self.nameLabel)
        layout.addLayout(middleLayout)


        self.editButton.clicked.connect(self.editFunction)
        self.addShow.clicked.connect(self.addShowFunction)

        self.setLayout(layout)

    def addShowFunction(self):
        self.addShowWindow = addShowWindow(self.name, self.showsTable, self.shows)

    def editFunction(self):
        print("well we are on row " + str(self.showsTable.currentRow()))
        if(self.showsTable.currentRow() > 0):
            self.temp = editShowWindow(self.shows[self.showsTable.currentRow()])


class addShowWindow(QWidget):
    def __init__(self, name, table, shows, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exitButton = QPushButton("add")

        self.statusLabel = QLabel("Edit")
        self.titleLabel = QLabel("Title:")
        self.watchStatusLabel = QLabel("Watch Status:")
        self.ratingLabel = QLabel("Rating:")
        self.episodesLabel = QLabel("Episode: ")
        self.tepisodeLabel = QLabel("Total Episodes: ")

        self.titleBox = QLineEdit()
        self.watchStatusDrop = QComboBox()
        self.watchStatusDrop.addItems(['P','W','C'])
        self.ratingDrop = QComboBox()
        self.ratingDrop.addItems(['1','2','3','4','5','6','7','8','9','10'])
        self.episodeBox = QLineEdit()
        self.tepisodeBox = QLineEdit()
        

        labelsLayout = QVBoxLayout()
        labelsLayout.addWidget(self.titleLabel)
        labelsLayout.addWidget(self.watchStatusLabel)
        labelsLayout.addWidget(self.ratingLabel)
        labelsLayout.addWidget(self.episodesLabel)
        labelsLayout.addWidget(self.tepisodeLabel)

        editablesLayout = QVBoxLayout()
        editablesLayout.addWidget(self.titleBox)
        editablesLayout.addWidget(self.watchStatusDrop)
        editablesLayout.addWidget(self.ratingDrop)
        editablesLayout.addWidget(self.episodeBox)
        editablesLayout.addWidget(self.tepisodeBox)

        itemsLayout = QHBoxLayout()
        itemsLayout.addLayout(labelsLayout)
        itemsLayout.addLayout(editablesLayout)

        layout = QVBoxLayout()
        layout.addWidget(self.statusLabel)
        layout.addLayout(itemsLayout)
        layout.addWidget(self.exitButton)

        self.exitButton.clicked.connect(lambda: self.addButtonFunction(table, name, shows))

        self.setLayout(layout)
        self.show()
    def addButtonFunction(self, table, name, shows):
        if(self.titleBox.text() == ""):
            self.statusLabel.setText("Please enter a title")
        elif(int(self.episodeBox.text()) > int(self.tepisodeBox.text())):
            self.statusLabel.setText("Please enter a valid episode amount")
        else:
            for item in shows:
                if self.titleBox.text() == item.title:
                    self.statusLabel.setText("This title already exists!")
                    return
            shows.append(Item(self.titleBox.text(), self.watchStatusDrop.currentText(), self.ratingDrop.currentText(), self.tepisodeBox.text(), self.episodeBox.text()))

            tableWidgets = [QTableWidgetItem(self.titleBox.text()),
                            QTableWidgetItem(self.watchStatusDrop.currentText()), 
                            QTableWidgetItem(str(self.ratingDrop.currentText())), 
                            QTableWidgetItem(str(self.episodeBox.text()) + "/" + str(self.tepisodeBox.text()))]
            for aspect in tableWidgets:
                aspect.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                aspect.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            table.setItem(table.rowCount()-1, 0, tableWidgets[0])
            table.setItem(table.rowCount()-1, 1, tableWidgets[1])
            table.setItem(table.rowCount()-1, 2, tableWidgets[2])
            table.setItem(table.rowCount()-1, 3, tableWidgets[3])
            self.close()
        print("Well this should work!")


class editShowWindow(QWidget):
    def __init__(self, item, name, table, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exitButton = QPushButton("exit")

        self.statusLabel = QLabel("Edit")
        self.titleLabel = QLabel("Title:")
        self.watchStatusLabel = QLabel("Watch Status:")
        self.ratingLabel = QLabel("Rating:")
        self.episodesLabel = QLabel("Episode: ")

        self.titleBox = QLineEdit()
        self.titleBox.setText(item.title)
        self.watchStatusDrop = QComboBox()
        self.watchStatusDrop.addItems(['P','W','C'])
        if(item.status == 'P'):
            self.watchStatusDrop.setCurrentIndex(0)
        elif(item.status == 'W'):
            self.watchStatusDrop.setCurrentIndex(1)
        else:
            self.watchStatusDrop.setCurrentIndex(2)
        self.ratingDrop = QComboBox()
        self.ratingDrop.addItems(['1','2','3','4','5','6','7','8','9','10'])
        self.ratingDrop.setCurrentIndex(item.rating-1)
        self.episodeBox = QLineEdit()
        self.episodeBox.setText(str(item.currentEpisode))
        self.episodeBox.setValidator(QIntValidator(0, int(item.totalEpisodes)+1))

        labelsLayout = QVBoxLayout()
        labelsLayout.addWidget(self.titleLabel)
        labelsLayout.addWidget(self.watchStatusLabel)
        labelsLayout.addWidget(self.ratingLabel)
        labelsLayout.addWidget(self.episodesLabel)

        editablesLayout = QVBoxLayout()
        editablesLayout.addWidget(self.titleBox)
        editablesLayout.addWidget(self.watchStatusDrop)
        editablesLayout.addWidget(self.ratingDrop)
        editablesLayout.addWidget(self.episodeBox)

        itemsLayout = QHBoxLayout()
        itemsLayout.addLayout(labelsLayout)
        itemsLayout.addLayout(editablesLayout)

        layout = QVBoxLayout()
        layout.addWidget(self.statusLabel)
        layout.addLayout(itemsLayout)
        layout.addWidget(self.exitButton)

        self.setLayout(layout)
        self.show()

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