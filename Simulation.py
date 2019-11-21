from PyQt5.QtCore import QTimer, QElapsedTimer
from Person import Person
import logging
from enum import Enum
import random
from Seat import SeatRow
from Plane import Plane
from Person import MoveType
import heapq 
import sys

ShuffleType = Enum('ShuffleType', 'Random Steffen BackToFront BoardingGroups')


class Simulation:

    actionsPerSecond = None
    stowTime = None 
    timer = None
    plane = None
    patrons = None
    scene = None
    peopleInSim = None
    generations = None 
    popSize = None 
    elapsedTime = None 
    simulationQueues = []
    times = []
    window = None 
    curGeneration = 0
    curSimList = None 
    timeHeap = []
    iteration = None 
    variance = 0
    bestTime = None 

    def __init__(self, plane, scene, window, actions=10, stowTime=1, shuffleTime=2, generations=10, popSize=10):
        self.plane = plane
        self.scene = scene
        self.timer = QTimer()
        self.timer.timeout.connect(self.next)
        self.actionsPerSecond = actions
        self.stowTime = stowTime
        self.generations = generations
        self.popSize = popSize
        self.shuffleTime = shuffleTime
        self.timer.setInterval(1000 / self.actionsPerSecond)
        self.peopleInSim = []
        self.elapsedTime = QElapsedTimer()
        self.window = window
        self.window.time_lcd.setDigitCount(3)
        self.iteration = 0
        self.variance = 30
        self.bestTime = sys.maxsize

        #create an initial population 
        patrons = self.makePatrons()
        patrons = sorted(patrons, key=lambda patron: patron.getGoalSeat().xPos, reverse=True)
        # now we will shuffle groups of 36 (6 * 6) to simulate a boarding party
        i = 0
        BOARDING_GROUP_SIZE = 36
        while i < len(patrons):
            group = patrons[i:i+BOARDING_GROUP_SIZE]
            random.shuffle(group)
            patrons[i:i+BOARDING_GROUP_SIZE] = group
            i += BOARDING_GROUP_SIZE
        self.simulationQueues.append(patrons)

        self.timeHeap = [(100, patrons[:]), (100, patrons[:])]
        heapq.heapify(self.timeHeap)


    def start(self):
        self.patrons = self.simulationQueues.pop()
        self.curSimList = self.patrons[:]
        self.timer.start()
        self.elapsedTime.start()

    def makePatrons(self):
        """
        Make a person object for each seat to be occupied and assign it as the goal seat, return a list 
        """
        patrons = []

        for row in self.plane.cells:
            for seat in row:
                if seat.seatType != SeatRow.NoSeat:
                    patrons.append(Person(seat))

        return patrons

    def next(self):
        """
        Move to the next time step 
        """

        self.window.time_lcd.display(self.elapsedTime.elapsed() / 1000)

        # allow all patrons to move again
        for person in self.peopleInSim:
            person.setCanMove(True)

        # ask the plane to try and move everyone twoards the goal seat
        finished = self.movePatrons()

        # try to see if we can get someone on the plane
        if self.plane.startSeatEmpty() and len(self.patrons) > 0:
            nextPerson = self.patrons.pop(0)
            self.plane.addToStartSeat(nextPerson)
            self.scene.addItem(nextPerson)
            self.peopleInSim.append(nextPerson)
            finished = False 
        
        if finished:
            if len(self.simulationQueues) > 0:
                time = self.elapsedTime.restart() / 1000
                print(time)
                if time < self.bestTime:
                    self.bestTime = time
                    self.window.best_time_lcd.display(time)
                    text = ""
                    for person in self.curSimList:
                        text += str(person.getGoalSeat().row * Plane.COLS + person.getGoalSeat().col) + " "
                    self.window.best_sequence_label.setText(text)
                self.iteration += 1
                self.window.iteration_lcd.display(self.iteration % self.popSize)
                heapq.heappush(self.timeHeap, (time, self.curSimList[:]))
                self.clearPatrons()
                self.patrons = self.simulationQueues.pop()
                self.peopleInSim = []
            else:
                self.curGeneration += 1
                self.window.generation_lcd.display(self.curGeneration)

                if self.curGeneration > self.generations:
                    self.timer.stop()
                    return 

                #take the best two lists and mutate them 
                firstBest = heapq.heappop(self.timeHeap)
                sndBest = heapq.heappop(self.timeHeap)
                print(firstBest[0], sndBest[0])
                firstBest = [Person(p.getGoalSeat()) for p in firstBest[1]]
                sndBest = [Person(p.getGoalSeat()) for p in sndBest[1]]
                self.simulationQueues = [firstBest[:], sndBest[:]]
                for _ in range(self.popSize // 2 - 1):
                    cp1 = [Person(p.getGoalSeat()) for p in firstBest]
                    cp2 = [Person(p.getGoalSeat()) for p in sndBest]
                    self.mutate(cp1, self.variance)
                    self.mutate(cp2, self.variance)
                    self.simulationQueues.append(cp1)
                    self.simulationQueues.append(cp2)
                self.variance -= 3
                self.resetSim()

    
    def mutate(self, patronList, variance):
        for _ in range(variance):
            idx = range(len(patronList))
            i1, i2 = random.sample(idx, 2)
            patronList[i1], patronList[i2] = patronList[i2], patronList[i1]
                

    def movePatrons(self):
        """
        For every patron on the plane attemp to move them twoards the goal
        """

        state = self.plane.cells
        simFinished = True 

        # propigate change from front to back
        for col in range(Plane.COLS - 1, -1, -1):
            for row in range(Plane.ROWS):
                cell = state[row][col]
                if cell.hasPerson():
                    person = cell.getPerson()

                    if person.getWaitTime() > 0:
                        person.decWaitTime()
                        simFinished = False
                        continue

                    # this person is not waiting, so set to default pixmap
                    if not person.isDefaultPixMap():
                        person.changeDefaultPixMap()
                    
                    if cell != person.getGoalSeat():
                        simFinished = False

                    # if the person is not where they should be
                    if cell != person.getGoalSeat() and person.canMove(): 
                        move = person.getNextMove(cell)
                        newSeat = None
                        if move == MoveType.Right:
                            newSeat = state[row][col + 1]
                        elif move == MoveType.Left:
                            newSeat = state[row][col - 1]
                        elif move == MoveType.Up:
                            newSeat = state[row - 1][col]
                        elif move == MoveType.Down:
                            newSeat = state[row + 1][col]
                        else:
                            continue

                        # they are now in the same column as their seat, stow bag
                        if move == MoveType.Up or move == MoveType.Down:
                            if not person.hasStowedBag():
                                person.addWaitTime(self.stowTime)
                                person.setHasStowed(True)
                                person.changeIsStowingPixMap()
                                continue
                            elif not person.getHasWaitedForPassengers():
                                # the amount of time this person waits is proportional to the people they need to get by

                                # note refactor this into new function and fix it so people only count people as waiting they need to pass over
                                peopleToWaitFor = 0
                                if move == MoveType.Up:
                                    for i in range(1, 3 - person.getGoalSeat().row):
                                        if state[row - i][col].isGoal():
                                            peopleToWaitFor += 1
                                else:
                                    for i in range(1, person.getGoalSeat().row - 3):
                                        if state[row + i][col].isGoal():
                                            peopleToWaitFor += 1

                                if peopleToWaitFor > 0:
                                    person.addWaitTime(peopleToWaitFor * self.shuffleTime)
                                    person.changeIsWaitingPixMap()

                                person.setHasWaitedWaitedForPassengers(True)
                                continue

                        # move person to new seat
                        if not newSeat.hasPerson() or not newSeat.getPerson().isBlocking():
                            # cant move twice in one sim loop
                            person.setCanMove(False)
                            newSeat.setPerson(person)

                            # person made it
                            if newSeat == person.getGoalSeat():
                                newSeat.goalIsReached()

                            # remove person from previous cell
                            cell.removePerson()

                    else:
                        person.setCanBlock(False)
        
        return simFinished
    
    def clearPatrons(self):
        for person in self.peopleInSim:
            self.scene.removeItem(person)
    
    def resetSim(self):
        self.timer.stop()
        self.timeHeap = []
        self.clearPatrons()
        self.peopleInSim = []
        self.times = []
        self.start()