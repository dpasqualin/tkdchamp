#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from datetime import datetime

class Person:
    def __init__(self,firstName=None,
                      lastName=None,
                      birthday=None,
                      email=None):

        self.__firstName = firstName or ""
        self.__lastName = lastName or ""
        self.__birthday = birthday
        self.__email = email

    def getName(self):
        return str(self.__firstName + " " + self.__lastName).strip()

    def getFirstName(self):
        return self.__firstName

    def getLastname(self):
        return self.__lastName

    def getBirthday(self):
        return self.__birthday

    def getAge(self):
        #FIXME: Nao eh assim que se faz
        return datetime.today().year - self.getBirthday().year


class Fighter(Person):

    def __init__(self,firstName=None,
                      lastName=None,
                      birthday=None,
                      email=None,
                      belt=0):

        Person.__init__(self,firstName,lastName,birthday,email)
        self.__belt = belt

    def getBelt(self):
        return self.__belt


class Judge(Person):

    def __init__(self,ident,
                      firstName=None,
                      lastName=None,
                      birthday=None,
                      email=None):

        Person.__init__(self,firstName,lastName,birthday,email)
        self.__ident = ident

    def getID(self):
        return self.__ident

