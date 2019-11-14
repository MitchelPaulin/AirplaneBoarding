from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from Seat import SeatRow


class Person(QGraphicsPixmapItem):

    goalSeat = None

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
    
    def getGoalSeat(self):
        return self.goalSeat[-1]
    
    def popGoalSeat(self):
        if len(self.goalSeat):
            self.goalSeat.pop()
    
    def __str__(self):
        return str(self.goalSeat)