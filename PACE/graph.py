import time
import sys
import os
from matplotlib import pyplot as plt

class Graph:
    
    def __init__(self, eyePos, blockPos, time):
        self.eyePos = eyePos
        self.blockPos = blockPos
        self.time = time

    def initializeGraph(self):
        for x in range(0,len(self.eyePos)):
            plt.plot(self.blockPos[x][0], self.time[x])
            plt.plot(self.eyePos[x][0], self.time[x])
        plt.show()
