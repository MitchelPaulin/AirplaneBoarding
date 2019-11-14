from PyQt5.QtCore import QTimer
from Person import Person
import logging
from enum import Enum
import random
from Seat import SeatRow

ShuffleType = Enum('ShuffleType', 'Random Steffen')


class Simulation:

    ACTIONS_PER_SECOND = 1

    timer = None 
    plane = None
    patrons = None
    scene = None

    def __init__(self, plane, scene, shuffleType):
        self.plane = plane 
        self.scene = scene
        self.timer = QTimer()
        self.timer.timeout.connect(self.next)
        self.timer.setInterval(1000 / self.ACTIONS_PER_SECOND)

        self.patrons = self.makePatrons()
        self.sufflePatrons(shuffleType)

        self.timer.start()
    

    def makePatrons(self):
        """
        Make a person object for each seat to be occupied and assign it as the goal seat, return a list 
        """
        patrons = []

        for row in self.plane.cells:
            for seat in row:
                if seat.seatType != SeatRow.NoSeat:
                    patrons.append(Person(seat))
        
        return patrons
    
    def sufflePatrons(self, shuffleType):
        """
        suffle the patrons based on what boarding technique we want
        """
        if shuffleType == ShuffleType.Random:
            random.shuffle(self.patrons)


    def next(self):
        """
        move to the next time step 
        """
        top = self.patrons.pop()
        top.setPos(top.getGoalSeat().x_pos, top.getGoalSeat().y_pos)
        self.scene.addItem(top)
