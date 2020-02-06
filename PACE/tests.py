import time
import sys
import os
import pygame
from pygame.locals import *
import random
import graph as gp
import UI

class rectObj:
	xCoord = 0
	color = ()

class RandTest:

	blockPos = []
	eyePos = []
	time = []

	def updateScreen(self):
		self.screen.fill(pygame.Color("white"))
		#BACK BUTTON
		UI.createButton(self.screen, "BACK", UI.BRIGHT_GREEN, UI.BLACK, (50,50,75,75), 20)

	def __init__(self, screen, numRuns, width, height):
		self.screen = screen
		self.numRuns = numRuns
		self.width = width
		self.height = height

	def runTest(self):

		blockPos = []
		eyePos = []
		times = []

		for i in range(0, self.numRuns):
			x = random.randint(100, self.width - 100)
			y = random.randint(100, self.height - 100)
			self.updateScreen()
			pygame.draw.rect(self.screen, pygame.Color("red"), (x, y, 100, 100))
			time.sleep(0.5)
			pygame.display.update()
			mouseX, mouseY = pygame.mouse.get_pos()
			blockPos.append([x,y])
			eyePos.append([mouseX,mouseY])
			times.append(time.perf_counter_ns())

		graph = gp.Graph(blockPos, eyePos, times)
		graph.initializeGraph()
		#pygame.quit()

class OptoTest:

	blockPos = []
	eyePos = []
	time = []

	def __init__(self, screen, numBlocks, numRuns, speed, width, height):
		self.screen = screen
		self.numBlocks = numBlocks
		self.numRuns = numRuns
		self.speed = speed
		self.width = width
		self.height = height

	def runTest(self):

		blockPos = []
		eyePos = []
		time = []

		blockList = []

		for x in range(self.numBlocks):
			tempBlock = rectObj()
			tempBlock.xCoord = (x / self.numBlocks) * self.width
			if x % 4 == 0:
				tempBlock.color = RED
			else:
				tempBlock.color = BLACK
			blockList.append(tempBlock)
		#create surface to create green rectangle
		surf = pygame.Surface((400,150))
		surf.fill(WHITE)
		greenRect = pygame.draw.rect(surf, GREEN, (0, 0, 400, 150), 7)
		greenRectLeft =  (self.width / 2) - (greenRect.width / 2)
		greenRectRight = self.width - greenRectLeft
		#place at this pixel location
		screen.blit(surf, (self.width / 2 - (greenRect.width / 2), self.height / 2 - (greenRect.height / 2)))

		BLOCKHEIGHT = self.width / self.numBlocks
		CENTERY = (self.height/2) - (BLOCKHEIGHT / 2)

		for x in range(self.numRuns):
			for block in blockList:
				pygame.draw.rect(screen, block.color, (block.xCoord, CENTERY, BLOCKHEIGHT, BLOCKHEIGHT))
				block.xCoord += self.speed
				if block.xCoord >= self.width - BLOCKHEIGHT:
					block.xCoord = -BLOCKHEIGHT
				if block.xCoord > greenRectLeft and block.xCoord < greenRectRight and block.color == RED:
					blockPos.append(block.xCoord)
					mouseX, mouseY = pygame.mouse.get_pos()
					eyePos.append([mouseX,mouseY])

			pygame.display.update()
			time.sleep(.002)

		for pos in eyePos:
			print("Eye pos: %d", pos[0])
		for pos in blockPos:
			print("Block pos: %d", pos[0])
