#!/usr/bin/env python
from time import time
from math import log
from threading import Semaphore

class PointCounter(object):
    """ Point Counter for a TaeKwonDo Fight.
            fight: a fight to control """
    def __init__(self, fight):
        self.__numberOfJudge = 0
        self.__fight = fight
        self.__sem = Semaphore(1)
        self.__judgeList = []

        # Necessary number of judge to validate a point
        self.__nJudge = 0

        # Acceptable time interval between commands of different judges
        # If this time is exceeded the point is not counted.
        self.timeout = 1.3 # X seconds

        # Control list of fight, fighter:{list_of_judges,first entry time}
        fBlue = self.__fight.getBlueFighter()
        fRed = self.__fight.getRedFighter()
        self.flist = {fBlue: {'j':[], 't':0},
                      fRed : {'j':[], 't':0}}

    def __updateNecessaryJudge(self):
        """ Recalculate the min number of judges necessary to make a
        point """
        self.__nJudge = int(log(len(self.__nJudge,2)))+1

    def getNJudge(self):
        """ Return the number of judges connected """
        return self.__nJudge

    def addJudge(self, judge):
        """ Add a new judge to judge list """

        self.__judgeList.append(judge)
        self.__updateNecessaryJudge()

    def judgeSignal(self, fighter, judge, n=1):

        now = time()
        self.__sem.acquire()

        if judge not in self.flist[fighter]['j']:

            if self.flist[fighter]['t'] == 0:
                self.flist[fighter]['t'] = now

            self.flist[fighter]['j'].append(judge)

            # If time limit was not exceeded
            if now - self.flist[fighter]['t'] <= self.timeout:
                # If necessary number of judges was reached
                if len(self.flist[fighter]['j']) >= self.getNJudge():
                    self.__fight.addPoint(fighter,n)
                    self.flist[fighter]['j'] = []
                    self.flist[fighter]['t'] = 0
                else:
                    self.flist[fighter]['j'].append(judge)
            # Se o tempo limite estourou considera esse como outro ponto
            else:
                self.flist[fighter]['j'] = [judge]
                self.flist[fighter]['t'] = now

        self.__sem.release()
