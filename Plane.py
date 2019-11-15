from Person import Person
from Seat import *


class Plane:

    """
    A class to act as a wrapper around a matrix of seats 
    """

    FIRST_SEAT_X = 755
    FIRST_SEAT_Y = 54
    SEAT_GAP_X = 3.6
    SEAT_GAP_Y = 2
    COLS = 24
    ROWS = 7

    # holds an array of seats that patrons can occupy
    cells = []
    startSeat = None

    def __init__(self):
        for i in range(self.ROWS):
            self.cells.append([])

            y = self.FIRST_SEAT_Y + Seat.SEAT_HEIGHT * i
            y += self.SEAT_GAP_Y * (i - 1)

            # determine seat type based on row
            seatType = SeatRow.NoSeat
            if i == 1 or i == 5:  # Center row index
                seatType = SeatRow.Center
            elif i == 2 or i == 4:  # Isle row index
                seatType = SeatRow.Isle
            elif i == 0 or i == 6:  # Window row index
                seatType = SeatRow.Window

            x = None
            for j in range(self.COLS):

                x = self.FIRST_SEAT_X + Seat.SEAT_WIDTH * j

                if x >= 1:
                    x += self.SEAT_GAP_X * (j - 1)

                newSeat = Seat(x, y, seatType, i, j)
                self.cells[i].append(newSeat)

        # first seat in isle is where everyone starts
        self.startSeat = self.cells[3][0]

    def startSeatEmpty(self):
        return self.startSeat.getPerson() is None

    def addToStartSeat(self, person):
        if self.startSeatEmpty():
            self.startSeat.setPerson(person)
