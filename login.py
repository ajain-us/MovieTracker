from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QMainWindow, QStyleFactory, QTableWidgetItem, QTableWidget, QComboBox, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QScreen
import sys, pyodbc, time


#This is the connection string, you can change this to make it work with your own SQL server
#if you try to connect with current login information it will not work as I have depricated the SQL server
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={'movie-tracker-aj.database.windows.net'};DATABASE={'movie tracker aj'};UID={'adminsql'};PWD={'&yHASu9NFf?87vz'}'
#handling if the connection can be established
try:
    #creates the connection
    connection = pyodbc.connect(connectionString)
    #creates a cursor that can be used to edit the tables
    cursor = connection.cursor()
# if we cannot connect to the server create a popup and shutdown the program
except TimeoutError as e:
    dialog = QMessageBox()
    dialog.setText("Could not establish a connection to server")
    dialog.setIcon(QMessageBox.Icon.Warning)
    dialog.exec()
    time.sleep(10)
    sys.exit()

#Class that extends QMainWindow, handles all the main GUI layouts
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        #call to super constructor
        super().__init__(*args, **kwargs)
        #setting the window title and size in the center
        self.setWindowTitle("Movie Tracker")
        self.setGeometry(int((QApplication.primaryScreen().geometry().width()/2 - 250)), int((QApplication.primaryScreen().geometry().height()/2 - 50)), 500, 100)
        # creates a login window and sets it as the main widget
        self.setCentralWidget(LoginWindow())
        # creates connections between the LoginWindow buttons and the functions in MainWindow class
        self.centralWidget().registerButton.clicked.connect(self.registerButton)
        self.centralWidget().loginButton.clicked.connect(self.loginButton)
        #enables the window to be sene
        self.show()
    # this function deals with what happens when the register button is clicked
    def registerButton(self):
        # disables the current login window
        self.centralWidget().close()
        # sets the register window as the central window
        self.setCentralWidget(RegisterWindow())
        # connects the return button functionality to the function in MainWindow class
        self.centralWidget().returnButton.clicked.connect(self.registerReturn)
    # this function deals with what happens when the return button in pressed in the register window
    def registerReturn(self):
         # closes the register window 
         self.centralWidget().close()
         # sets the central window to login window
         self.setCentralWidget(LoginWindow())
         # sets the login window button functionality with the functions in class MainWindow
         self.centralWidget().registerButton.clicked.connect(self.registerButton)
         self.centralWidget().loginButton.clicked.connect(self.loginButton)
    # this function deals with what happens when the login button is pressed from the login window class
    def loginButton(self):
        # checks to see if the user actually provided a username and password
        if not (self.centralWidget().userBox.text() and self.centralWidget().passwordBox.text()):
            # creates a pop up window that informs the user to add a username and password
            dialog = QMessageBox()
            dialog.setText("Please enter a valid username and password")
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.exec()
            return
        # creates a query string to check the SQL server and get the login info
        queryString = "SELECT * FROM Logins WHERE Username = '" + self.centralWidget().userBox.text() + "'"
        #print(queryString), debug statement to see if the query string is proper
        # actually processes the query string
        cursor.execute(queryString)
        # saves the login information row into a variable
        loginRow = cursor.fetchall()
        # Need to run SQL query "Select * FROM logins WHERE Username = self.centralWidget().userBox.text()"
        # above statement was a note while coding
        # if the login row was not found, then we inform the user that the username was not found
        if not loginRow:
            # creates popup that informs the user that their username was not found
            dialog = QMessageBox()
            dialog.setText("This username was not found")
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.exec()
            return
        # checks to see if the password matches
        if self.centralWidget().passwordBox.text() == loginRow[0].Password:
            # if it does, then we close the login window
            self.centralWidget().close()
            # create a new information window and provide the username to it
            self.setCentralWidget(InfoWindow(loginRow[0].Username))
            # sets the functionality of the logout button in the info window
            self.centralWidget().logoutButton.clicked.connect(self.logoutButton)
        else:
            # if the password does not match we will inform the user that it is wrong
            dialog = QMessageBox()
            dialog.setText("The username or password is wrong")
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.exec()
        #print(loginRow[0].Password) : debug statement to see if the password was being found correctly
    # this function sets the functionality for the logout button in info window
    def logoutButton(self):
        # closes the info window
        self.centralWidget().close()
        # sets the central window back to login window
        self.setCentralWidget(LoginWindow())
        # sets the functionality of the login window buttons
        self.centralWidget().registerButton.clicked.connect(self.registerButton)
        self.centralWidget().loginButton.clicked.connect(self.loginButton)
# this class deals with the widgets related to the login window
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
                dialog = QMessageBox()
                dialog.setText("Please enter a valid username or password")
                dialog.setIcon(QMessageBox.Icon.Warning)
                dialog.exec()
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
                dialog = QMessageBox()
                dialog.setText("User has been added, please return to login")
                dialog.setIcon(QMessageBox.Icon.Information)
                dialog.exec()
            else:
                dialog = QMessageBox()
                dialog.setText("This username already exists")
                dialog.setIcon(QMessageBox.Icon.Warning)
                dialog.exec()
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
        self.deleteShow.clicked.connect(self.deleteShowFunction)

        self.setLayout(layout)

    def addShowFunction(self):
        self.addShowWindow = addShowWindow(self.name, self.showsTable, self.shows)

    def deleteShowFunction(self):
        if(self.showsTable.currentRow() < 0):
            dialog = QMessageBox()
            dialog.setText("Please select a show to remove")
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.exec()
        else:
            queryString = "DELETE FROM shows WHERE Username = '" + self.name + "' AND Title = '" + self.showsTable.item(self.showsTable.currentRow(),0).text() + "'"
            cursor.execute(queryString)
            cursor.commit()
            self.shows.pop(self.showsTable.currentRow())
            self.showsTable.removeRow(self.showsTable.currentRow())
            #print(self.showsTable.item(self.showsTable.currentRow(),0).text())

    def editFunction(self):
        if(self.showsTable.currentRow() >= 0):
            self.temp = editShowWindow(self.shows[self.showsTable.currentRow()], self.name, self.showsTable)
        else:
            dialog = QMessageBox()
            dialog.setText("Please select a show")
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.exec()


class addShowWindow(QWidget):
    def __init__(self, name, table, shows, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Add")

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
        self.episodeBox.setValidator(QIntValidator())
        self.tepisodeBox = QLineEdit()
        self.tepisodeBox.setValidator(QIntValidator())
        

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
            dialog = QMessageBox()
            dialog.setText("Please Enter a title")
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.exec()
        elif(int(self.episodeBox.text()) > int(self.tepisodeBox.text())):
            dialog = QMessageBox()
            dialog.setText("Please enter valid episode numbers")
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.exec()
        else:
            for item in shows:
                if self.titleBox.text() == item.title:
                    dialog = QMessageBox()
                    dialog.setText("This Title already exists")
                    dialog.setIcon(QMessageBox.Icon.Warning)
                    dialog.exec()
                    return
            shows.append(Item(self.titleBox.text(), self.watchStatusDrop.currentText(), self.ratingDrop.currentText(), self.tepisodeBox.text(), self.episodeBox.text()))

            queryString = "INSERT INTO shows (Username, Title, WatchStatus, Rating, TotalEpisodes, CurrentEpisode) VALUES ('" + str(name) + "', '" + self.titleBox.text() + "', '" + self.watchStatusDrop.currentText() + "', " + self.ratingDrop.currentText() + ", " + self.tepisodeBox.text() + ", " + self.episodeBox.text() + ")"

            cursor.execute(queryString)
            cursor.commit()

            tableWidgets = [QTableWidgetItem(self.titleBox.text()),
                            QTableWidgetItem(self.watchStatusDrop.currentText()), 
                            QTableWidgetItem(str(self.ratingDrop.currentText())), 
                            QTableWidgetItem(str(self.episodeBox.text()) + "/" + str(self.tepisodeBox.text()))]
            for aspect in tableWidgets:
                aspect.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                aspect.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setRowCount(table.rowCount() + 1)
            table.setItem(table.rowCount()-1, 0, tableWidgets[0])
            table.setItem(table.rowCount()-1, 1, tableWidgets[1])
            table.setItem(table.rowCount()-1, 2, tableWidgets[2])
            table.setItem(table.rowCount()-1, 3, tableWidgets[3])
            self.close()


class editShowWindow(QWidget):
    def __init__(self, item, name, table, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Edit")

        self.exitButton = QPushButton("exit")

        self.statusLabel = QLabel("Edit")
        self.titleLabel = QLabel("Title:")
        self.watchStatusLabel = QLabel("Watch Status:")
        self.ratingLabel = QLabel("Rating:")
        self.episodesLabel = QLabel("Episode: ")

        self.titleBox = QLineEdit()
        self.titleBox.setText(item.title)
        self.titleBox.setEnabled(False)
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
        self.ratingDrop.setCurrentIndex(int(item.rating)-1)
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

        self.exitButton.clicked.connect(lambda: self.exitButtonFunction(item, name, table))

        self.setLayout(layout)
        self.show()
    def exitButtonFunction(self, item, name, table):
        if (int(self.episodeBox.text()) > int(item.totalEpisodes) or int(self.episodeBox.text()) < 0 ):
            dialog = QMessageBox()
            dialog.setText("Please enter a current amount of episodes")
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.exec()
        else:
            item.status = self.watchStatusDrop.currentText()
            item.rating = self.ratingDrop.currentText()
            item.currentEpisode = self.episodeBox.text()

            queryString = "UPDATE shows SET WatchStatus = '" + item.status + "', Rating = " + item.rating + ", CurrentEpisode = " + item.currentEpisode + " WHERE Username = '" + name + "' AND Title = '" + item.title + "'"
            cursor.execute(queryString)
            cursor.commit()
            table.item(table.currentRow(),1).setText(item.status)
            table.item(table.currentRow(),2).setText(item.rating)
            table.item(table.currentRow(),3).setText(str(item.currentEpisode) + "/" + str(item.totalEpisodes))
            self.close()

        


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
    
    app.setStyle(QStyleFactory.create("fusion"))

    window = MainWindow()

    sys.exit(app.exec())