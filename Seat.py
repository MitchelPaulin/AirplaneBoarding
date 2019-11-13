from enum import Enum

SeatRow = Enum('SeatRow', 'Window Center Isle')


class Seat:

    SEAT_WIDTH = 30
    SEAT_HEIGHT = 30

    x_pos = None
    y_pos = None
    row = None
    person = None

    # place a person in this seat
    def setPerson(self, person):
        self.person = person

    def __init__(self, x_pos, y_pos, seatRow):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.row = seatRow

    def __str__(self):
        print(self.x_pos, self.y_pos, self.row)
