import time
import sys
import os
import pygame
from pygame.locals import *
import random
import graph as gp
import UI
from serial import Serial as ser


class rectObj:
	xCoord = 0
	color = ()

class Test:

	testDone = None
	currentTest = ""

	def updateScreen(self):
		self.screen.fill(pygame.Color("white"))
		#BACK BUTTON
		UI.createButton(self.screen, "BACK", UI.BRIGHT_GREEN, UI.BLACK, UI.BACKBUTTONRECT, 20)

	def __init__(self, screen, numRuns, numBlocks, speed, testName):
		self.screen = screen
		self.numRuns = numRuns
		self.numBlocks = numBlocks
		self.speed = speed
		self.testName = testName
		self.blockPos = []
		self.eyePos = []
		self.times = []
		self.width = UI.SCREENWIDTH
		self.height = UI.SCREENHEIGHT

	def countdown(self):
		for i in range(0, 3):
			UI.createText(self.screen, "Starting test in:", UI.BLACK, (UI.SCREENWIDTH / 2, UI.SCREENHEIGHT / 6), int(UI.SCREENWIDTH / 14))
			UI.createText(self.screen, f"{3-i}", UI.BLACK, (UI.SCREENWIDTH / 2, UI.SCREENHEIGHT / 2), int(UI.SCREENWIDTH / 16))
			pygame.display.update()
			time.sleep(1)
			self.screen.fill(pygame.Color("white"))

	def runTest(self):
		self.countdown()
		if self.testName == "Opto Test":
			self.optoTest()
		elif self.testName == "Random Test":
			self.randTest()
		elif self.testName == "Saccades Test":
			self.saccadesTest()
		elif self.testName == "Smooth Test":
			self.smoothTest()

	def saccadesTest(self):

		self.blockPos = []
		self.eyePos = []
		self.times = []

		left = (self.width / 4) - 50
		right = (3 * self.width / 4) - 50
		y = (self.height / 2) - 50

		Test.testDone = False
		Test.currentTest = self.testName

		currentTime = 0

		for i in range(0, self.numRuns):

			if UI.mainMenu:
				return

			self.updateScreen()

			if i % 2 == 0:
				pygame.draw.rect(self.screen, pygame.Color("red"), (left, y, 100, 100))
				self.blockPos.append(left + 50)
			else:
				pygame.draw.rect(self.screen, pygame.Color("red"), (right, y, 100, 100))
				self.blockPos.append(right + 50)


			pygame.display.update()
			time.sleep(self.speed)

			mouseX, mouseY = pygame.mouse.get_pos()
			self.eyePos.append(mouseX)
			self.times.append(currentTime)

			currentTime += 1

		Test.testDone = True

	def randTest(self):

		self.blockPos = []
		self.eyePos = []
		self.times = []

		Test.testDone = False
		Test.currentTest = self.testName

		currentTime = 0

		for i in range(0, self.numRuns):

			if UI.mainMenu:
				return

			x = random.randint(100, self.width - 100)
			y = random.randint(100, self.height - 100)

			self.updateScreen()

			pygame.draw.rect(self.screen, pygame.Color("red"), (x, y, 100, 100))

			pygame.display.update()
			time.sleep(self.speed)

			mouseX, mouseY = pygame.mouse.get_pos()
			self.blockPos.append(x + 50)
			self.eyePos.append(mouseX)
			self.times.append(currentTime)

			currentTime += 1

		Test.testDone = True

	def smoothTest(self):


		self.blockPos = []
		self.eyePos = []
		self.times = []

		#Starting position of rectangle
		rect_x = UI.SCREENWIDTH / 2
		rect_y = UI.SCREENHEIGHT / 2

		#Speed/direction of rectangle
		rect_change_x = -3
		rect_change_y = 3

		Test.testDone = False
		Test.currentTest = self.testName

		currentTime = 0

		for i in range(0, self.numRuns):

			if UI.mainMenu:
				return

			rect_x += rect_change_x #Changes rectangle x to move in x direction
			rect_y += rect_change_y #Changes rectangle y to move in y direction

			self.updateScreen()
			pygame.draw.rect(self.screen, UI.RED, [rect_x, rect_y, 100,100])


			#Bounce ball if needed
			if rect_y > UI.SCREENHEIGHT - 100 or rect_y < 0: #If y position reaches the border
				rect_change_y = rect_change_y * -1 #Makes rectangle move in opposite y direction
			if rect_x > UI.SCREENWIDTH - 100 or rect_x < 0: #If x position reaches the border
				rect_change_x = rect_change_x * -1 #Makes rectangle move in opposite x direction
			self.blockPos.append(rect_x + 50)
			mouseX, mouseY = pygame.mouse.get_pos()
			self.eyePos.append(mouseX)
			self.times.append(currentTime)

			currentTime += 1

			pygame.display.update()

		Test.testDone = True

	def convdiv(self):
		port = "/dev/ttyACMO"
		ser = serial.Serial(port, 115200, timeout = 1)

		while True:
			if UI.mainMenu:
				return
			data = ser.read(4)
			self.times.append(data)
			break;

	def optoTest(self):

		self.blockPos = []
		self.eyePos = []
		self.times = []

		blockList = []

		self.updateScreen()
		pygame.display.update()

		#Create all the blocks being iterated through
		for x in range(self.numBlocks):
			tempBlock = rectObj()
			tempBlock.xCoord = (x / self.numBlocks) * self.width
			if x % 4 == 0:
				tempBlock.color = UI.RED
			else:
				tempBlock.color = UI.BLACK
			blockList.append(tempBlock)

		BLOCKHEIGHT = (self.width / self.numBlocks)
		CENTERY = (self.height/2) - (BLOCKHEIGHT / 2)

		#Create surface to create green rectangle
		surf = pygame.Surface((BLOCKHEIGHT * 4 - 20, BLOCKHEIGHT * 3))
		surf.fill(UI.WHITE)
		greenRect = pygame.draw.rect(surf, UI.GREEN, (0, 0, BLOCKHEIGHT * 4 - 20, BLOCKHEIGHT * 3), 7)
		greenRectLeft =  greenRect.left
		greenRectRight = greenRect.left + greenRect.width
		#place at this pixel location
		self.screen.blit(surf, (3 * self.width / 8, 3 * self.height / 8))
		pygame.display.update()

		Test.testDone = False
		Test.currentTest = self.testName

		currentTime = 0
		right = True

		for x in range(self.numRuns):

			if UI.mainMenu:
				return

			if x == self.numRuns / 2:
				right = False

			for block in blockList:
				pygame.draw.rect(self.screen, block.color, (block.xCoord, CENTERY, BLOCKHEIGHT, BLOCKHEIGHT))

				if right:
					block.xCoord += self.speed
				else:
					block.xCoord -= self.speed

				if block.xCoord > self.width - (BLOCKHEIGHT / 2):
					block.xCoord = -(BLOCKHEIGHT / 2)
				if block.xCoord < -(BLOCKHEIGHT / 2):
					block.xCoord = self.width - (BLOCKHEIGHT / 2)

				if block.xCoord > greenRectLeft and block.xCoord < greenRectRight and block.color == UI.RED:
					self.blockPos.append(block.xCoord + BLOCKHEIGHT / 2)
					mouseX, mouseY = pygame.mouse.get_pos()
					self.eyePos.append(mouseX)
					self.times.append(currentTime)

			pygame.display.update()
			time.sleep(.005)

			currentTime += 1

		Test.testDone = True
