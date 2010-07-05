#!/usr/bin/env python

class EventManager:

    def __init__(self):
        self.__eventDict = {}

    def addEvent(self, event):
        self.__eventDict[event] = []

    def runEvent(self, event, **args=None):
        if self.__eventDict.has_key(event):
            for f in self.__eventDict[event]:
                f(event,args)

    def associateEvent(self, event, function):
        if self.eventExist(event):
            self.__eventDict[event].append(function)

    def eventExist(self, event):
        return self.__eventDict.has_key(event)

    def getAssociations(self):
        return self.__eventDict
