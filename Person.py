from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from Seat import SeatRow


class Person(QGraphicsPixmapItem):

    goalSeat = None

    def __init__(self, goalSeat):
        self.goalSeat = goalSeat
        if goalSeat.row == SeatRow.Center:
            super().__init__(QPixmap('assets/tealPerson.png'))
        elif goalSeat.row == SeatRow.Isle:
            super().__init__(QPixmap('assets/violetPerson.png'))
        elif goalSeat.row == SeatRow.Window:
            super().__init__(QPixmap('assets/bluePerson.png'))
        else:
            super().__init__(QPixmap('assets/tealPerson.png'))