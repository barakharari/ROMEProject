import time
import sys
import os
import pygame
from pygame.locals import *
import tkinter as tk

#CONSTANTS
BLACK = (0,0,0)
RED = (200,0,0)
GREEN = (0,180,0)
BRIGHT_GREEN = (0,225,0)
BRIGHT_RED = (255,0,0)
WHITE = (255, 255, 255)
SCREENWIDTH = int(tk.Tk().winfo_screenwidth() / 2)
SCREENHEIGHT = int(tk.Tk().winfo_screenheight() / 2)

def createButton(screen, text, buttonColor, fontColor, positionRect, fontSize):
    font = pygame.font.SysFont("Times New Roman, Arial", fontSize)
    pygame.draw.rect(screen, buttonColor, positionRect)
    textSurface = font.render(text, True, fontColor)
    textRect = textSurface.get_rect()
    textRect.center = (positionRect[0] + positionRect[2]/2), (positionRect[1] + positionRect[3]/2)
    screen.blit(textSurface, textRect)

def createText(screen, text, fontColor, position, fontSize):
    font = pygame.font.SysFont("Times New Roman, Arial", fontSize)
    textSurface = font.render(text, True, fontColor)
    textRect = textSurface.get_rect()
    textRect.center = position[0], position[1]
    screen.blit(textSurface, textRect)
