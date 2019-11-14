from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from Seat import SeatRow
from enum import Enum

MoveType = Enum('MoveType', 'Up Down Left Right NoMove')

class Person(QGraphicsPixmapItem):

    goalSeat = None
    moveable = True

    def __init__(self, goalSeat):
        self.goalSeat = [goalSeat]
        if goalSeat.seatType == SeatRow.Center:
            super().__init__(QPixmap('assets/tealPerson.png'))
        elif goalSeat.seatType == SeatRow.Isle:
            super().__init__(QPixmap('assets/violetPerson.png'))
        elif goalSeat.seatType == SeatRow.Window:
            super().__init__(QPixmap('assets/bluePerson.png'))
        else:
            super().__init__(QPixmap('assets/tealPerson.png'))
    
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