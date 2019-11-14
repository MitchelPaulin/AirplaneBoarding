from PyQt5.QtCore import QTimer
from Person import Person
import logging
from enum import Enum
import random
from Seat import SeatRow
from Plane import Plane 
from Person import MoveType

ShuffleType = Enum('ShuffleType', 'Random Steffen')

class Simulation:

    ACTIONS_PER_SECOND = 2

    timer = None 
    plane = None
    patrons = None
    scene = None
    peopleInSim = None

    def __init__(self, plane, scene, shuffleType):
        self.plane = plane 
        self.scene = scene
        self.timer = QTimer()
        self.timer.timeout.connect(self.next)
        self.timer.setInterval(1000 / self.ACTIONS_PER_SECOND)

        self.patrons = self.makePatrons()
        self.sufflePatrons(shuffleType)

        self.peopleInSim = []

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

        #allow all patrons to move again 
        for person in self.peopleInSim:
            person.setCanMove(True)

        #ask the plane to try and move everyone twoards the goal seat 
        self.movePatrons()

        #try to see if we can get someone on the plane 
        if self.plane.startSeatEmpty() and len(self.patrons) > 0:
            nextPerson = self.patrons.pop()
            self.plane.addToStartSeat(nextPerson)            
            self.scene.addItem(nextPerson) 
            self.peopleInSim.append(nextPerson)
    
    def movePatrons(self):
        """
        For every patron on the plane attemp to move them twoards the goal
        """

        state = self.plane.cells 

        #propigate change from front to back 
        for col in range(Plane.COLS -1, -1, -1):
            for row in range(Plane.ROWS):
                cell = state[row][col]
                if cell.hasPerson():
                    person = cell.getPerson()

                    if person.getWaitTime() > 0:
                        person.decWaitTime()
                        continue 

                    #if the person is not where they should be 
                    if cell != person.getGoalSeat() and person.canMove():
                        move = person.getNextMove(cell)
                        newSeat = None 
                        if move == MoveType.Right:
                            newSeat = state[row][col + 1]
                        elif move == MoveType.Left:
                            newSeat = state[row][col - 1]
                        elif move == MoveType.Up:
                            newSeat = state[row - 1][col]
                        elif move == MoveType.Down:
                            newSeat = state[row + 1][col]
                        else:
                            continue
                        #move person to new seat 
                        if not newSeat.hasPerson():
                            person.setCanMove(False) #cant move twice in one sim loop
                            newSeat.setPerson(person)
                            cell.removePerson()
                        elif not newSeat.getPerson().isBlocking():
                            #person needs to wait people number of cycles to enter seat 
                            if not person.getHasWaitedForPassengers():
                                person.addWaitTime(2)
                                person.setHasWaitedWaitedForPassengers(True)
                            else:
                                person.setCanMove(False) #cant move twice in one sim loop
                                newSeat.setPerson(person)
                                cell.removePerson()

                    else:
                        person.setCanBlock(False)