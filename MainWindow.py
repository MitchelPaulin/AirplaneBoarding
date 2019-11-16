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

    plane = None
    simulation = None
    scene = None
    isPaused = None

    # handle UI stuff here

    def startSim(self):
        if self.simulation:
            self.simulation.clearPatrons()

        simType = None

        if self.back_to_front_radio.isChecked():
            simType = ShuffleType.BackToFront
        elif self.random_radio.isChecked():
            simType = ShuffleType.Random
        elif self.steffen_perfect_radio.isChecked():
            simType = ShuffleType.Steffen
        elif self.boarding_groups_radio.isChecked():
            simType = ShuffleType.BoardingGroups
        else:
            return

        self.isPaused = False
        self.plane = Plane()
        self.simulation = Simulation(self.plane, self.scene, simType, self.actions_per_second_slider.value(),
                                     self.stow_time_slider.value(), self.passenger_shuffle_time_slider.value())
        self.simulation.start()

    def pauseSim(self):
        if self.isPaused:
            self.simulation.start()
            self.isPaused = False
        elif self.simulation:
            self.simulation.pause()
            self.isPaused = True

    def cancelSim(self):
        if self.simulation:
            self.simulation.clearPatrons()
            self.simulation.pause()
            self.simulation = None

    def __init__(self):
        super(MainWindow, self).__init__()
        path = os.path.join(dirname, 'assets/mainwindow.ui')
        loadUi(path, self)
        simWindow = self.simulation_window
        path = os.path.join(dirname, 'assets/planeLayout.png')
        planeImage = QPixmap(path)

        if planeImage.isNull():
            print("Could not find plane layout image")
            exit()

        self.scene = QGraphicsScene(simWindow)
        self.scene.addPixmap(planeImage)
        simWindow.setScene(self.scene)
        self.begin_simulation_button.clicked.connect(self.startSim)
        self.pause_simulation_button.clicked.connect(self.pauseSim)
        self.cancel_simulation_button.clicked.connect(self.cancelSim)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    logging.basicConfig(filename='debug.log', filemode='w', level=logging.INFO)

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = MainWindow()

    sys.exit(app.exec_())
