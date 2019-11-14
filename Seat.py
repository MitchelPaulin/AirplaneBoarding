from enum import Enum

SeatRow = Enum('SeatRow', 'Window Center Isle NoSeat')


class Seat:

    SEAT_WIDTH = 30
    SEAT_HEIGHT = 30

    x_pos = None
    y_pos = None
    seatType = None
    person = None

    # place a person in this seat
    def setPerson(self, person):
        self.person = person

    def __init__(self, x_pos, y_pos, seatType):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.seatType = seatType

    def __str__(self):
        return str(self.x_pos) + " " + str(self.y_pos) + " " + str(self.seatType)
