import pygame , sys

import threading

import server
from pygame.locals import *
import math
from random import randint
import striker 
import time


class Puck():
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.radius = 10
		self.max_speed = 5
		self.x_speed = 3.5
		self.y_speed = 3.5
		self.red = (255,0,0)

		self.x_pos = self.width//2
		self.y_pos = self.height//2
		self.c_time = 0.1


	def restart(self , sign):
		if sign == "striker2":
			sign = -1
		else:
			sign = 1
		self.x_speed = 0
		self.y_speed = 5 *sign
		self.x_pos = self.width//2
		self.y_pos = self.height//2
		self.max_speed = 5

	def dist(self,a,b):
		return ((a.y_pos - b.y_pos)**2 + (a.x_pos-b.x_pos)**2)**0.5

	def atan(self,a,b):
		return math.atan((a.y_pos - b.y_pos) / (a.x_pos - b.y_pos))
	
	def update(self , dt , striker1 , striker2):
		print("1000001")
		# if (not(dt)):return



		# collsion with striker 1
		if (self.dist(striker1 , self) <= striker1.radius + self.radius + 5):
			# self.max_speed = (striker1.x_speed**2 + striker1.y_speed**2)**0.5
			if self.max_speed<5:
				self.max_speed = 5

			ang = self.atan(striker1 , self)

			if self.x_pos <= striker1.x_pos:
				# self.x_speed = -math.cos(ang) * self.max_speed
				# self.y_speed = -math.sin(ang) * self.max_speed
				
				self.x_speed = -math.sin(ang) * self.max_speed
				self.y_speed = -math.cos(ang) * self.max_speed

			else:
				# self.x_speed = math.cos(ang) * self.max_speed
				# self.y_speed = math.sin(ang) * self.max_speed
	
				self.x_speed = math.sin(ang) * self.max_speed
				self.y_speed = math.cos(ang) * self.max_speed

		# collsion with striker 2
		if (self.dist(striker2 , self) <= striker2.radius + self.radius + 5):
			# self.max_speed = (striker2.x_speed**2 + striker2.y_speed**2)**0.5
			if self.max_speed<5:
				self.max_speed = 5

			ang = self.atan(striker2 , self)

			if self.x_pos <= striker2.x_pos:
				# self.x_speed = -math.cos(ang) * self.max_speed
				# self.y_speed = -math.sin(ang) * self.max_speed

				self.x_speed = -math.sin(ang) * self.max_speed
				self.y_speed = -math.cos(ang) * self.max_speed


			else:
				# self.x_speed = math.cos(ang) * self.max_speed
				# self.y_speed = math.sin(ang) * self.max_speed

				self.x_speed = math.sin(ang) * self.max_speed
				self.y_speed = math.cos(ang) * self.max_speed


		# collision with left wall

		if self.x_pos - self.radius < 0:
			self.x_speed = -self.x_speed
			self.x_pos = self.radius
		
		# collision with right wall

		if self.x_pos+self.radius > self.width:
			self.x_speed = -self.x_speed
			self.x_pos = self.width - self.radius

		# collision with top wall

		if self.y_pos<self.radius+5:
			self.y_pos = self.radius +5
			self.y_speed = -self.y_speed

		# collision with bottom wall

		if self.y_pos > self.height - self.radius:
			self.y_pos = self.height - self.radius
			self.y_speed = -self.y_speed

		# goal condition point of 2
		if (self.y_pos > self.height - self.radius - 10) and \
		(self.x_pos > self.width//2 - 100 ) and \
		(self.x_pos < self.width//2 +100):
			score.update(s2=1)
			self.restart("striker2")

		# goal condition point of 1
		if (self.y_pos < self.radius + 10) and \
		(self.x_pos > self.width//2 - 100 ) and \
		(self.x_pos < self.width//2 +100 ):
			score.update(s1=1)
			self.restart("striker1")

		# update position from speed
		
		self.x_pos += self.x_speed * dt * self.c_time
		self.y_pos += self.y_speed * dt * self.c_time

		print(10000000000000000001,self.x_pos , self.y_pos)
		

	def draw(self,pygame,DISPLAYSURF):
		print("1001")
		pygame.draw.circle(DISPLAYSURF, self.red, (int(self.x_pos),int(self.y_pos)), self.radius, 0)




class Score:
	def __init__(self,pygame,width,height):
		self.width = width
		self.height = height
		self.score1 = 0
		self.score2 = 0
		self.color = (0,0,0)
		self.back = (255,255,255)
		self.fontObj = pygame.font.Font('freesansbold.ttf', 20)
		output = "1: " + str(self.score1) + " || 2: "+str(self.score2)
		self.textSurfaceObj = self.fontObj.render(output , True, self.color, self.back)
		self.textRectObj = self.textSurfaceObj.get_rect()
		self.textRectObj.center = (self.width//2, 20)
		
	def update(self,s1 = 0,s2 = 0):

		self.score1 += s1
		self.score2 += s2
		output = "1: " + str(self.score1) + " || 2: "+str(self.score2)
		self.textSurfaceObj = self.fontObj.render(output, True, self.color, self.back)
		self.textRectObj = self.textSurfaceObj.get_rect()
		self.textRectObj.center = (self.width//2, 20)

	def text(self,t):
		self.textSurfaceObj = self.fontObj.render(t, True, self.color, self.back)
		self.textRectObj = self.textSurfaceObj.get_rect()
		self.textRectObj.center = (self.width//2, 20)

	def draw(self,pygame,DISPLAYSURF):
		# DISPLAYSURF.fill(self.back)
		DISPLAYSURF.blit(self.textSurfaceObj, self.textRectObj)



def game():


	time.sleep(2)
	score.text("3")
	score.draw(pygame,DISPLAYSURF)
	pygame.display.update()
	time.sleep(1)
	score.text("2")
	score.draw(pygame,DISPLAYSURF)
	pygame.display.update()
	time.sleep(1)
	score.text("1")
	score.draw(pygame,DISPLAYSURF)
	pygame.display.update()
	score.text("GAME STARTS")
	score.draw(pygame,DISPLAYSURF)
	pygame.display.update()





	while True:
		dt = fpsClock.tick(FPS)
		DISPLAYSURF.fill(WHITE)
		DISPLAYSURF.blit(bg, (0, 0))
		striker.striker1.draw(pygame,DISPLAYSURF)
		striker.striker2.draw(pygame,DISPLAYSURF)
		puck.update(dt , striker.striker1 , striker.striker2)
		puck.draw(pygame,DISPLAYSURF)
		
		score.draw(pygame,DISPLAYSURF)
		endgame=False
		

		if endgame==True:
			break
		pygame.display.update()
		fpsClock.tick(FPS)

if __name__ == "__main__": 



	print(1)
	pygame.init()
	FPS = 100
	fpsClock = pygame.time.Clock()

	width = 400
	height = 600
	DISPLAYSURF = pygame.display.set_mode((width,height))
	pygame.display.set_caption('helloworls')
	bg = pygame.image.load("bg.png") #INSIDE OF THE GAME LOOP gameDisplay.blit(bg, (0, 0)) 

	GREEN = (  0, 255,   0)
	RED = (255,0,0)
	WHITE = (0,0,0)

	striker.init_striker(width,height)
	score = Score(pygame,width,height)
	puck = Puck(width,height)


	t1 = threading.Thread(target=game, args=()) 
	t2 = threading.Thread(target=server.start, args=(pygame,DISPLAYSURF,))

	t1.start()
	t2.start() 


	t1.join()
	t2.join()