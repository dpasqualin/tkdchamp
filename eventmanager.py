#!/usr/bin/env python

class EventManager:

    def __init__(self):
        self.__eventDict = {}

    def runEvent(self, event, **args=None):
        """ Execute all functions associated to the event """
        if self.__eventDict.has_key(event):
            for f in self.__eventDict[event]:
                f(event,args)

    def associateEvent(self, event, function):
        """ Create an association between the function and event.
        When the event occur, the function will be called. """
        if self.eventExist(event):
            self.__eventDict[event].append(function)
        else:
            self.__eventDict[event] = [function]

    def eventExist(self, event):
        """ Return True if event exist and False otherwise """
        return self.__eventDict.has_key(event)

    def getAssociations(self):
        return self.__eventDict
