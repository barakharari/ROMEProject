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

    def runTest(self):
        self.test.runTest()
