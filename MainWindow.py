# File MainWindow.py
# Driver file for the application

import sys
import logging
import qdarkstyle
import os 
from PyQt5.QtGui import QBrush, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from PyQt5.QtCore import QFile, QSize
from PyQt5.uic import loadUi
from Plane import Plane 
from Person import Person 
from Seat import SeatRow
from Simulation import Simulation, ShuffleType

dirname = os.path.dirname(__file__)
class MainWindow(QMainWindow):
    """
    The Main panel of the application 
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        path = os.path.join(dirname, 'assets/mainwindow.ui')
        loadUi(path, self)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    logging.basicConfig(filename='debug.log', filemode='w', level=logging.INFO)

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = MainWindow()

    simWindow = window.simulation_window
    path = os.path.join(dirname, 'assets/planeLayout.png')
    planeImage = QPixmap(path)

    if planeImage.isNull():
        print("Could not find plane layout image")
        exit()

    newScene = QGraphicsScene(simWindow)
    newScene.addPixmap(planeImage)
    simWindow.setScene(newScene)

    plane = Plane()
    simulation = Simulation(plane, newScene, ShuffleType.Random)

    #handle UI stuff here 

    simulation.start()

    sys.exit(app.exec_())
