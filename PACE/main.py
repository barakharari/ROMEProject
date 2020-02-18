import time
import sys
import os
import pygame
from pygame.locals import *
import pygame_textinput
import tests as t
import tkinter as tk
import threading
import option as opt
import UI
import graph as gp
import statistics
import pickle

pygame.init()

tests = ["Opto Test", "Random Test", "Saccades Test", "Smooth Test"]
options = []
optionSize = (1/len(tests)) * (UI.SCREENWIDTH / 2)

running = True
screen = pygame.display.set_mode((UI.SCREENWIDTH, UI.SCREENHEIGHT))
clock = pygame.time.Clock()

inputFile = 'stats.data'

def ageAndNameMenu():

	nameRect = pygame.Rect(UI.SCREENWIDTH / 2, 60, UI.SCREENWIDTH / 4 + 30, UI.SCREENHEIGHT / 2 - 60)
	ageRect = pygame.Rect(UI.SCREENWIDTH / 2, 60, UI.SCREENWIDTH / 4 + 30, UI.SCREENHEIGHT / 2 + 50)

	nameSurf = pygame.Surface((nameRect.left, nameRect.top))
	nameSurf.fill((UI.RED))
	ageSurf = pygame.Surface((ageRect.left, ageRect.top))
	ageSurf.fill((UI.RED))

	screen.blit(nameSurf, (ageRect.width, ageRect.height))
	screen.blit(ageSurf, (ageRect.width, ageRect.height))

	textinput = pygame_textinput.TextInput('', 'Times New Roman', 30, True, UI.WHITE, UI.RED)
	running = True
	nameEntered = False

	name = ""
	age = ""

	while running:

		events=pygame.event.get()

		UI.createText(screen, "Input Name and Age", UI.BLACK, (UI.SCREENWIDTH / 2, UI.SCREENHEIGHT / 6), int(UI.SCREENWIDTH / 15))
		UI.createText(screen, "Name:", UI.BLACK, (nameRect.width - 100, nameRect.height + nameRect.top / 2), int(UI.SCREENWIDTH / 20))
		UI.createText(screen, "Age:", UI.BLACK, (ageRect.width - 100, ageRect.height + ageRect.top / 2), int(UI.SCREENWIDTH / 20))
		# Feed it with events every frame

		if not nameEntered:
			nameSurf.fill(UI.RED)
			nameSurf.blit(textinput.get_surface(), (10, 10))
			screen.blit(nameSurf, (nameRect.width, nameRect.height))

			if textinput.update(events):
				name = textinput.get_text()
				textinput = pygame_textinput.TextInput('', 'Times New Roman', 30, True, UI.WHITE, UI.RED)
				nameEntered = True

		else:
			# Blit its surface onto the screen
			ageSurf.blit(textinput.get_surface(), (10, 10))
			screen.blit(ageSurf, (ageRect.width, ageRect.height))

			if textinput.update(events):
				age = textinput.get_text()
				return (name, age)

		pygame.display.update()
		clock.tick(30)

def gatherData(age, test):

	for i in range(0, len(options)):
		if (options[i].name == test):

			eyePos = options[i].test.eyePos
			blockPos = options[i].test.blockPos
			times = options[i].test.times

			#average distance from blockPos
			eyePosDistances = []
			for x in range(0,len(times)):
				eyePosDistances.append(abs(blockPos[i] - eyePos[i]))

			#mean of eyePos distances
			eyePosDistanceAverage = statistics.mean(eyePosDistances)

			info = None
			ageObject = None

			#with open('userData.data', 'rb') as handle:
    		#	info = pickle.load(handle)

			#if 18 <= age <= 30:
			#	testArray = info["18-30"][f"{test}"]
			#	testArray.append(eyePosDistanceAverage)
			#	info["18-30"][f"{test}Average"] = statistics.mean(testArray)
			#elif 31 <= age <= 60:
			#	testArray = info["31-60"][f"{test}"]
			#	testArray.append(eyePosDistanceAverage)
			#	info["31-60"][f"{test}Average"] = statistics.mean(testArray)
			#elif 61 <= age <= 80:
			#	testArray = info["61-80"][f"{test}"]
			#	testArray.append(eyePosDistanceAverage)
			#	info["61-80"][f"{test}Average"] = statistics.mean(testArray)

			#with open('userData.data', 'wb') as handle:
    		#	pickle.dump(info, handle, protocol=pickle.HIGHEST_PROTOCOL)

			#create graph

			#convdiv test
			if len(eyePos) == 0:
				graph = gp.convDivGraph()
			else:
				graph = gp.Graph(options[i].name, eyePos, blockPos, times)
			graph.initializeGraph()

			break

def initializeTests():

	yPosition = UI.SCREENHEIGHT / 2 - optionSize / 2

	for i in range(0,len(tests)):

		xPosition = (((i / len(tests)) * UI.SCREENWIDTH) + UI.SCREENWIDTH / (2 * (len(tests)))) - optionSize / 2
		test = None

		#screen, numRuns, numBlocks, speed, testName

		if tests[i] == "Opto Test":
			#Num blocks must be multiple of 4
			test = t.Test(screen, 300, 20, 7, "Opto Test")
		elif tests[i] == "Random Test":
			test = t.Test(screen, 11, None, 1, "Random Test")
		elif tests[i] == "Saccades Test":
			test = t.Test(screen, 11, None, 1, "Saccades Test")
		elif tests[i] == "Smooth Test":
			test = t.Test(screen, 200, None, None, "Smooth Test")
		else:
			print("Something went wrong with test names")

		options.append(opt.Option(tests[i], xPosition, yPosition, optionSize, test))

if __name__ == "__main__":

	screen.fill(UI.WHITE)
	name, age = ageAndNameMenu()

	screen.fill(UI.WHITE)
	initializeTests()

	#CREATE TITLE
	UI.createText(screen, "ROME Object Detection Project", UI.BLACK, (UI.SCREENWIDTH / 2, UI.SCREENHEIGHT / 6), int(UI.SCREENWIDTH / 15))

	#Event loop
	while running:

		#MAINMENU
		if UI.mainMenu:

			for i in range(0, len(options)):
				optionRect = pygame.Rect(options[i].xPosition, options[i].yPosition, options[i].size, options[i].size)
				if optionRect.collidepoint(pygame.mouse.get_pos()):

					#ON OPTION
					UI.createButton(screen, f'{tests[i]}', UI.BRIGHT_GREEN, UI.WHITE, optionRect, int(options[i].size / 6))

					#PRESSED WITHIN OPTION
					if pygame.mouse.get_pressed()[0]:

						#CLEAN UP
						screen.fill(UI.WHITE)
						UI.mainMenu = False

						#TEST THREAD
						testDone = False
						testThread = threading.Thread(target=options[i].runTest, args=(), daemon=True)
						testThread.start()

						break
				else:
					#NOT ON OPTION
					UI.createButton(screen, f'{tests[i]}', UI.GREEN, UI.BLACK, optionRect, int(options[i].size / 6))

			pygame.display.update()

		#NOT IN MAINMENU
		else:

			#SHOW GRAPHS
			if t.Test.testDone:
				t.Test.testDone = False

				gatherData(age, t.Test.currentTest)

			#PRESSED BACK BUTON
			if UI.BACKBUTTONRECT.collidepoint(pygame.mouse.get_pos()):
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
