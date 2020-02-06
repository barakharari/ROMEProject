import time
import sys
import os
import pygame
from pygame.locals import *
import tests as t
import tkinter as tk
import threading
import option as opt
import UI
import graph as gp

pygame.init()

tests = ["optoTest", "randTest"]
options = []
optionSize = (1/len(tests)) * (UI.SCREENWIDTH / 4)

mainMenu = True
running = True
screen = pygame.display.set_mode((UI.SCREENWIDTH, UI.SCREENHEIGHT))

def initializeWindow(name):
#center the window
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	screen.fill(UI.WHITE)
	pygame.display.set_caption(f'{name}')
	pygame.display.flip()

def createOptions():

	#CREATE TITLE
	UI.createText(screen, "ROME Object Detection Project", UI.BLACK, (UI.SCREENWIDTH / 2, UI.SCREENHEIGHT / 6), int(UI.SCREENWIDTH / 15))

	yPosition = UI.SCREENHEIGHT / 2 - optionSize / 2

	for i in range(0,len(tests)):
		xPosition = (((i / len(tests)) * UI.SCREENWIDTH) + UI.SCREENWIDTH / (2 * (len(tests)))) - optionSize / 2
		test = None

		if tests[i] == "optoTest":
			test = t.OptoTest(screen, 32, 1000, 5, UI.SCREENWIDTH, UI.SCREENHEIGHT)
		elif tests[i] == "randTest":
			test = t.RandTest(screen, 10, UI.SCREENWIDTH, UI.SCREENHEIGHT)

		options.append(opt.Option(tests[0], xPosition, yPosition, optionSize, test))


if __name__ == "__main__":

	initializeWindow("Main Menu")

	optionsThread = threading.Thread(target=createOptions, args=(), daemon=True)
	optionsThread.start()

	#Event loop
	while running:

		#pygame.time.delay(10)
		mouse = pygame.mouse.get_pos()

		#MAINMENU
		if mainMenu:
			for i in range(0, len(options)):
				xPos = options[i].get_xPosition()
				yPos = options[i].get_yPosition()
				size = options[i].get_size()
				if (xPos <= mouse[0] <= xPos + size) and (yPos <= mouse[1] <= yPos + size):

					#ON OPTION
					UI.createButton(screen, f'{tests[i]}', UI.BRIGHT_GREEN, UI.WHITE, (xPos, yPos, size, size), int(size / 5))

					#PRESSED WITHIN OPTION
					if pygame.mouse.get_pressed()[0]:
						mainMenu = False
						screen.fill(UI.WHITE)

						#BACK BUTTON
						UI.createButton(screen, "BACK", UI.BRIGHT_GREEN, UI.BLACK, (50,50,75,75), 20)

						#TEST THREAD
						testThread = threading.Thread(target=options[i].runTest, args=(), daemon=True)
						testThread.start()
				else:

					#NOT ON OPTION
					UI.createButton(screen, f'{tests[i]}', UI.GREEN, UI.BLACK, (xPos, yPos, size, size), int(size / 5))

			pygame.display.update()

		#NOT IN MAINMENU
		else:
			if (50 <= mouse[0] <= 125) and (50 <= mouse[1] <= 125):
				if pygame.mouse.get_pressed()[0]:
					mainMenu = True
					screen.fill(UI.WHITE)
					options = []
					optionsThread.start()

		#QUIT EVENT LOOP
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
					running = False
	#pygame.exit()
