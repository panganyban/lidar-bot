#!/usr/bin/env python

from __future__ import absolute_import
from abc import ABCMeta, abstractmethod


class Observable(object):
    def __init__(self):
        self.observers = []
        self.changed = 0

    def addObserver(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def deleteObserver(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def deleteAllObservers(self):
        self.observers = []

    def notifyObservers(self, arg=None):
        # lock observers list
        for obs in self.observers:
            obs.update(arg)
        # unlock


class Observer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, arg):
        pass
