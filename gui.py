from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
import sys

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs,):
        super().__init__(*args, **kwargs)
        
        # set the window title
        self.setWindowTitle('Hello World')
        
        # show the window
        self.show()

class SecondWindow(QWidget):
        def __init__(self, *args, **kwargs):
             super().__init__(*args,**kwargs)

             self.setWindowTitle("testing window")
             self.setGeometry(100,200,300,400)

             label = QLabel("this is a label!")
             button = QPushButton("Hide and Show!")

             layout = QVBoxLayout()

             layout.addWidget(label)
             layout.addWidget(button)

             self.setLayout(layout)

             self.show()
        def hideWindow(self):
             self.hide()

        def showWindow(self):
             self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = SecondWindow()
    window2 = SecondWindow()
    window.hideWindow()

    # start the event loop
    sys.exit(app.exec())