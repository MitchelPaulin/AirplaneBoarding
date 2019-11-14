# File MainWindow.py
# Driver file for the application

import sys
import logging
import qdarkstyle
from PyQt5.QtGui import QBrush, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from PyQt5.QtCore import QFile, QSize
from PyQt5.uic import loadUi
from Plane import Plane 
from Person import Person 
from Seat import SeatRow
from Simulation import Simulation, ShuffleType


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
    planeImage = QPixmap('assets/planeLayout.png')

    if planeImage.isNull():
        print("Could not find plane layout image")
        exit()

    newScene = QGraphicsScene(simWindow)
    newScene.addPixmap(planeImage)
    simWindow.setScene(newScene)

    plane = Plane()
    simulation = Simulation(plane, newScene, ShuffleType.Random)

    #handle UI stuff here 

    #test
    # for row in plane.positions:
    #     for seat in row:
    #         if seat.seatType != SeatRow.NoSeat:
    #             p = Person(seat)
    #             p.setPos(seat.x_pos, seat.y_pos)
    #             newScene.addItem(p)

    sys.exit(app.exec_())
