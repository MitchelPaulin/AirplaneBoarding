# File MainWindow.py
# Driver file for the application

import sys
import logging
import qdarkstyle
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QFile
from PyQt5.uic import loadUi


class MainWindow(QMainWindow):
    """
    The Main panel of the application 
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("assets/mainwindow.ui", self)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    logging.basicConfig(filename='debug.log', filemode='w', level=logging.INFO)

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = MainWindow()

    sys.exit(app.exec_())