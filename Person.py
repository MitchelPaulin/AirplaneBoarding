from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from Seat import SeatRow
from enum import Enum
import os

MoveType = Enum('MoveType', 'Up Down Left Right NoMove')

dirname = os.path.dirname(__file__)


class Person(QGraphicsPixmapItem):

    goalSeat = None
    moveable = None
    canBlock = None
    hasWaitedForPassengers = None
    hasStowed = None
    waitTime = 0  # how many cycles this person will wait
    isDefault = None

    pixMap = None
    waitingPixMap = None
    stowingPixMap = None

    def __init__(self, goalSeat):
        self.goalSeat = [goalSeat]
        self.moveable = False
        self.canBlock = True
        self.hasWaitedForPassengers = False
        self.waitTime = 0
        self.isDefault = True
        self.hasStowed = False

        if goalSeat.seatType == SeatRow.Center:
            self.pixMap = QPixmap(os.path.join(
                dirname, 'assets/tealPerson.png'))
            self.waitingPixMap = QPixmap(os.path.join(
                dirname, 'assets/tealPersonWaiting.png'))
            self.stowingPixMap = QPixmap(os.path.join(
                dirname, 'assets/tealPersonStowing.png'))
        elif goalSeat.seatType == SeatRow.Isle:
            self.pixMap = QPixmap(os.path.join(
                dirname, 'assets/violetPerson.png'))
            self.waitingPixMap = QPixmap(os.path.join(
                dirname, 'assets/violetPersonWaiting.png'))
            self.stowingPixMap = QPixmap(os.path.join(
                dirname, 'assets/violetPersonStowing.png'))
        elif goalSeat.seatType == SeatRow.Window:
            self.pixMap = QPixmap(os.path.join(
                dirname, 'assets/bluePerson.png'))
            self.waitingPixMap = QPixmap(os.path.join(
                dirname, 'assets/bluePersonWaiting.png'))
            self.stowingPixMap = QPixmap(os.path.join(
                dirname, 'assets/bluePersonStowing.png'))
        super().__init__(self.pixMap)

    def hasStowedBag(self):
        return self.hasStowed

    def setHasStowed(self, state):
        self.hasStowed = state

    def isDefaultPixMap(self):
        return self.isDefault

    def changeIsWaitingPixMap(self):
        self.setPixmap(self.waitingPixMap)
        self.isDefault = False

    def changeIsStowingPixMap(self):
        self.setPixmap(self.stowingPixMap)
        self.isDefault = False

    def changeDefaultPixMap(self):
        self.setPixmap(self.pixMap)
        self.isDefault = True

    def getHasWaitedForPassengers(self):
        return self.hasWaitedForPassengers

    def setHasWaitedWaitedForPassengers(self, state):
        self.hasWaitedForPassengers = state

    def setCanBlock(self, state):
        self.canBlock = state

    def isBlocking(self):
        return self.canBlock

    def setPosition(self, cell):
        self.setPos(cell.xPos, cell.yPos)

    def setCanMove(self, state):
        self.moveable = state

    def canMove(self):
        return self.moveable

    def getGoalSeat(self):
        return self.goalSeat[-1]

    def popGoalSeat(self):
        if len(self.goalSeat):
            self.goalSeat.pop()

    def addGoalSeat(self, seat):
        self.goalSeat.append(seat)

    def addWaitTime(self, time):
        self.waitTime += time

    def decWaitTime(self):
        self.waitTime -= 1

    def getWaitTime(self):
        return self.waitTime

    def getNextMove(self, curSeat):
        goal = self.getGoalSeat()

        if goal.xPos > curSeat.xPos:
            return MoveType.Right
        if goal.xPos < curSeat.xPos:
            return MoveType.Left
        if goal.yPos > curSeat.yPos:
            return MoveType.Down
        if goal.yPos < curSeat.yPos:
            return MoveType.Up
        return MoveType.NoMove

    def __str__(self):
        return str(self.goalSeat)
