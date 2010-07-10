#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from pointcounter import PointCounter

class Fight:
    """ This class intends to control a TaeKwonDo fight. """

    def __init__(self, fBlue, fRed, eventManager=None):
        self.__fBlue = fBlue
        self.__fRed = fRed

        # Stores score of fighters in this fight
        self.__score = {self.__fBlue:0, self.__fRed:0}

        # Stores committed faults in this fight
        self.__fault = {self.__fBlue:0, self.__fRed:0}
        self.__halfFault = {self.__fBlue:0, self.__fRed:0}

        # Stores fight status (true -> paused)
        self.__paused = False

        # Initialize point counter program
        self.__pc = PointCounter(self)

        # Current round
        self.__round = 1

    def getPointCounter(self):
        return self.__pc

    def addJudge(self, judge):
        """ Add a new judge to the fight """
        self.__pc.addJudge(judge)

    def getNJudge(self):
        """ Return the number of judges judging the fight """
        self.__pc.getNJudge()

    def judgeSignal(self, fighter, judge, n=1):
        """ A judge has been sinalized a possible point to a fighter """
        self.__pc.judgeSignal(fighter, judge, n)

    def getEventManager(self):
        return self.__eventManager

    def addPoint(self, fighter, n=1):
        """ Score 1 or 2 points to fighter. """
        self.__score[fighter] += n
        end = self.__checkEnd()
        if end:
            self.finish(end)

        self.__runEvent(self.addPoint)

    def __checkEnd(self):
        """ Check if a fight is over. """

        blue = self.__score[self.getBlueFighter()]
        red = self.__score[self.getRedFighter()]
        if blue - red > 7 or blue > 12:
            return self.getBlueFighter()
        elif red - blue > 7 or red > 12:
            return self.getRedFighter()
        else:
            return False

    def addFault(self, fighter):
        """ Add a fault to a fighter. """
        self.fault[fighter] += 1
        self.__runEvent(self.Fault)

    def addHalfFault(self, fighter):
        """ Add a half fault to a fighter. """
        self.halfFault[fighter] += 1
        self.__runEvent(self.haldFault)

    def pause(self):
        """ Pause this fight. """
        self.__paused = True
        self.__runEvent(self.pause)

    def unpause(self):
        """ Continue this fight, if it is paused. """
        self.__paused = False
        self.__runEvent(self.unpause)

    def finish(self, fighter):
        """ Finish this fight. """
        self.__runEvent(self.finish)

    def start(self):
        """ Start this fight. Must be called once. """
        self.__runEvent(self.start)

    def nextRound(self):
        """ Start next round, if the current round is done. """
        self.__round += 1
        self.__runEvent(self.nextRound)

    def getCurrentRound(self):
        """ Return current round. """
        return self.__round

    def getBlueFighter(self):
        """ Return Blue fighter. """
        return self.__fBlue

    def getRedFighter(self):
        """ Return Red fighter. """
        return self.__fRed

    def __runEvent(self,event):
        if self.__eventManager:
            self.__eventManager.runEvent(event)
