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

tests = ["Opto Test", "Random Test", "Saccades Test", "Smooth Test"]
options = []
optionSize = (1/len(tests)) * (UI.SCREENWIDTH / 2)

running = True
screen = pygame.display.set_mode((UI.SCREENWIDTH, UI.SCREENHEIGHT))

def initializeWindow(name):
#center the window
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	screen.fill(UI.WHITE)
	pygame.display.set_caption(f'{name}')
	pygame.display.flip()

def initializeMainMenu():

	yPosition = UI.SCREENHEIGHT / 2 - optionSize / 2

	for i in range(0,len(tests)):

		xPosition = (((i / len(tests)) * UI.SCREENWIDTH) + UI.SCREENWIDTH / (2 * (len(tests)))) - optionSize / 2
		test = None

		#screen, numRuns, numBlocks, speed, testName

		if tests[i] == "Opto Test":
			test = t.Test(screen, 1000, 20, 5, "Opto Test")
		elif tests[i] == "Random Test":
			test = t.Test(screen, 10, None, 0.5, "Random Test")
		elif tests[i] == "Saccades Test":
			test = t.Test(screen, 5, None, 1, "Saccades Test")
		elif tests[i] == "Smooth Test":
			test = t.Test(screen, 50, None, None, "Smooth Test")
		else:
			print("Something went wrong with test names")

		options.append(opt.Option(tests[i], xPosition, yPosition, optionSize, test))

if __name__ == "__main__":

	initializeWindow("Main Menu")

	optionsThread = threading.Thread(target=initializeMainMenu, args=(), daemon=True)
	testThread = None
	optionsThread.start()

	#CREATE TITLE
	UI.createText(screen, "ROME Object Detection Project", UI.BLACK, (UI.SCREENWIDTH / 2, UI.SCREENHEIGHT / 6), int(UI.SCREENWIDTH / 15))

	#Event loop
	while running:

		#pygame.time.delay(10)
		mouse = pygame.mouse.get_pos()

		#MAINMENU
		if UI.mainMenu:

			for i in range(0, len(options)):
				xPos = options[i].xPosition
				yPos = options[i].yPosition
				size = options[i].size
				if (xPos <= mouse[0] <= xPos + size) and (yPos <= mouse[1] <= yPos + size):

					#ON OPTION
					UI.createButton(screen, f'{tests[i]}', UI.BRIGHT_GREEN, UI.WHITE, (xPos, yPos, size, size), int(size / 6))

					#PRESSED WITHIN OPTION
					if pygame.mouse.get_pressed()[0]:

						screen.fill(UI.WHITE)
						UI.mainMenu = False

						#TEST THREAD
						testDone = False
						testThread = threading.Thread(target=options[i].runTest, args=(), daemon=True)
						testThread.start()

						break
				else:

					#NOT ON OPTION
					UI.createButton(screen, f'{tests[i]}', UI.GREEN, UI.BLACK, (xPos, yPos, size, size), int(size / 6))

			pygame.display.update()

		#NOT IN MAINMENU
		else:

			#SHOW GRAPHS
			if t.Test.testDone:
				t.Test.testDone = False

				#How do i determined the chosen test?
				for i in range(0, len(options)):
					if (options[i].name == t.Test.currentTest):

						#name, eyePos, blockPos, time

						graph = gp.Graph(options[i].name, options[i].test.eyePos, options[i].test.blockPos, options[i].test.times)
						graph.initializeGraph()
						break

			#PRESSED BACK BUTON
			if (50 <= mouse[0] <= 125) and (50 <= mouse[1] <= 125):
				if pygame.mouse.get_pressed()[0]:
					UI.mainMenu = True

					screen.fill(UI.WHITE)
					#CREATE TITLE
					UI.createText(screen, "ROME Object Detection Project", UI.BLACK, (UI.SCREENWIDTH / 2, UI.SCREENHEIGHT / 6), int(UI.SCREENWIDTH / 15))
					pygame.display.update()

		#QUIT EVENT LOOP
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
					running = False
	#pygame.exit()
