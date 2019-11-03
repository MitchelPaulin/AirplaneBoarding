# File MainWindow.py
# Driver file for the application

import sys
import logging
import qdarkstyle
from PyQt5.QtGui import QBrush, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from PyQt5.QtCore import QFile, QSize
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

    simWindow = window.simulation_window
    width = simWindow.sceneRect().width()
    height = simWindow.sceneRect().height()
    planeImage = QPixmap('assets/planeLayout.png')
    print(width, height)
    planeImage = planeImage.scaled(1781, 431)

    if planeImage.isNull():
        print("Could not find plane layout image")

    newScene = QGraphicsScene(simWindow)
    newScene.setBackgroundBrush(QBrush(planeImage))
    simWindow.setScene(newScene)



    sys.exit(app.exec_())