from enum import Enum

SeatRow = Enum('SeatRow', 'Window Center Isle NoSeat')


class Seat:

    SEAT_WIDTH = 30
    SEAT_HEIGHT = 30

    xPos = None
    yPos = None
    seatType = None
    person = None
    row = None 
    col = None 
    goalReached = None 

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

    def __init__(self, xPos, yPos, seatType, row, col):
        self.xPos = xPos
        self.yPos = yPos
        self.seatType = seatType
        self.row = row 
        self.col = col
        self.goalReached = False 
    
    def goalIsReachd(self):
        self.goalReached = True 
    
    #required since we need to keep track of if this seat is someones goal whether that person is blocking or not 
    def isGoal(self):
        return self.goalReached

    def getRow(self):
        return self.row 
    
    def getCol(self):
        return self.col

    def __str__(self):
        return str(self.xPos) + " " + str(self.yPos) + " " + str(self.seatType)
