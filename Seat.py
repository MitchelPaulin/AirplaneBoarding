from enum import Enum

SeatRow = Enum('SeatRow', 'Window Center Isle NoSeat')


class Seat:

    SEAT_WIDTH = 30
    SEAT_HEIGHT = 30

    xPos = None
    yPos = None
    seatType = None
    person = None

    def setPerson(self, person):
        """
        Place person in their spot as well as change the position 
        """
        self.person = person
        person.setPosition(self)
    
    def hasPerson(self):
        return self.person != None 

    def getPerson(self):
        return self.person
    
    def removePerson(self):
        temp = self.person
        self.person = None
        return temp 

    def __init__(self, xPos, yPos, seatType):
        self.xPos = xPos
        self.yPos = yPos
        self.seatType = seatType

    def __str__(self):
        return str(self.xPos) + " " + str(self.yPos) + " " + str(self.seatType)
