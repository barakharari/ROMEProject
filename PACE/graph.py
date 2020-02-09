import time
import sys
import os
from matplotlib import pyplot as plt

class Graph:

    def __init__(self, name, eyePos, blockPos, times):
        self.eyePos = eyePos
        self.blockPos = blockPos
        self.times = times
        self.name = name

    def initializeGraph(self):
        plt.xlabel("Time")
        plt.ylabel("Distance")
        plt.title(f"{self.name}")
        plt.plot(self.times, self.blockPos, color="b", label="Block Position")
        plt.plot(self.times, self.eyePos, color="k", linestyle="--", label="Eye Position")
        plt.legend()
        plt.show()
