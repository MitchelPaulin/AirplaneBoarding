from Person import Person
from Seat import *


class Plane:

    FIRST_SEAT_X = 755
    FIRST_SEAT_Y = 54
    SEAT_GAP_X = 3.6
    SEAT_GAP_Y = 2.4
    COLS = 24
    ROWS = 6
    TOTOAL_SEATS = COLS * ROWS

    # holds an array of seats that patrons can occupy
    positions = []

    def __init__(self):
        for i in range(self.ROWS):
            self.positions.append([])

            y = self.FIRST_SEAT_Y + Seat.SEAT_HEIGHT * i
            y += self.SEAT_GAP_Y * (i - 1)
            
            if i >= 3:
                y += Seat.SEAT_HEIGHT
                y -= self.SEAT_GAP_Y

            seatType = SeatRow.Window

            if i == 1 or i == 4:
                seatType = SeatRow.Center 
            elif i == 2 or i == 3:
                seatType = SeatRow.Isle

            for j in range(self.COLS):

                x = self.FIRST_SEAT_X + Seat.SEAT_WIDTH * j

                if x >= 1:
                    x += self.SEAT_GAP_X * (j - 1)

                newSeat = Seat(x, y, seatType)
                self.positions[i].append(newSeat)
