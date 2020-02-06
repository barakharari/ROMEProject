import time
import sys
import os
import tkinter as tk

class Option:
    def __init__(self, name, xPosition, yPosition, size, test):
        self.name = name
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.size = size
        self.test = test

    def get_xPosition(self):
        return self.xPosition

    def get_yPosition(self):
        return self.yPosition

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size

    def runTest(self):
        self.test.runTest()
