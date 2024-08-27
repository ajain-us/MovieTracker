from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
import sys

class MainWindow(QWidget):
     def __init__(self, *args, **kwargs,):
        super().__init__(*args, **kwargs)
        
        # set the window title
        self.setWindowTitle('Hello World')
        button = QPushButton("Hide and Show")

        button.clicked.connect(self.hideWindow)

        layout = QVBoxLayout()

        layout.addWidget(button)

        self.setLayout(layout)
        
        # show the window
     def hideWindow(self):
          self.hide()
          SecondWindow(parent).show()

     def showWindow(self):
          self.show()
     def addParent(self, window):
          self.parent = window

     
     



class SecondWindow(QWidget):
        def __init__(self, loginWindow, *args, **kwargs):
             super().__init__(*args,**kwargs)

             self.setWindowTitle("testing window")
             self.setGeometry(100,200,300,400)

             window = loginWindow

             loginWindow.parent = self

             window.otherWindow = self
             label = QLabel("this is a label!")
             button = QPushButton("Hide and Show!")

             button.clicked.connect(self.hideWindow)

             layout = QVBoxLayout()

             layout.addWidget(label)
             layout.addWidget(button)

             self.setLayout(layout)

             self.show()
        def hideWindow(self, window):
             self.hide()
             print("This is doing something")
             loginWindow.show()

        def showWindow(self):
             self.show()
     


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    loginWindow = MainWindow()
    window = SecondWindow(loginWindow)
    loginWindow.addParent(window = window)



    # start the event loop
    sys.exit(app.exec())