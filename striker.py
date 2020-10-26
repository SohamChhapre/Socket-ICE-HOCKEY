import pygame , sys

import multiprocessing 
from pygame.locals import *
import math
from random import randint
from math import pi, cos, sin

class Striker1():
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.radius = 20
		self.color =  (255,255,0) # yellow

		self.x_pos = width//2
		self.y_max = 100

		self.y_pos = height-20


		self.stablizer = 5

	def update_pos(self , x_rat  ,y_rat):
		w_mean = self.width//2 -10
		y_mean = self.height-20
		self.x_pos = w_mean + ((w_mean*x_rat)//self.stablizer)*self.stablizer

		self.y_pos = y_mean - ((self.y_max*(y_rat))//self.stablizer)*self.stablizer

	def draw(self,pygame,DISPLAYSURF):
		pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x_pos),int(self.y_pos)), self.radius, 0)



class Striker2():
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.radius = 20
		self.color =  (255,255,0) # yellow

		self.x_pos = width//2
		self.y_max = 100

		self.y_pos = 20


		self.stablizer = 5

	def update_pos(self , x_rat  ,y_rat):
		w_mean = self.width//2
		y_mean = self.height-20
		self.x_pos = w_mean + ((w_mean*x_rat)//self.stablizer)*self.stablizer

		self.y_pos = y_mean - ((self.y_max*(y_rat))//self.stablizer)*self.stablizer

	def draw(self,pygame,DISPLAYSURF):
		pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x_pos),int(self.y_pos)), self.radius, 0)


def init_striker(width,height):
	print(101)
	global striker1
	global striker2
	striker1 = Striker1(width,height)
	striker2 = Striker2(width,height)

# width = 300
# height = 600
# car = Car(width,height)

