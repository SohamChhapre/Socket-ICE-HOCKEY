import pygame , sys

import multiprocessing 
from pygame.locals import *
import math
from random import randint
from math import pi, cos, sin
from collections import deque
class Striker():
	def __init__(self,width,height,player_num):
		self.width = width
		self.height = height
		self.radius = 20
		self.color =  (255,255,0) # yellow

		self.x_pos = width//2
		self.y_max = 100


		self.x_speed = 2
		self.y_speed = 2

		self.speed_mag = 0
		if player_num == 1:
			self.y_pos = height-30
			self.y_mean = self.height-30
		else:
			self.y_pos = 30
			self.y_mean = 30



		self.stablizer = 10
		self.disappear_striker = False

		self.queue = deque()
		self.lim_length = 100
		self.speed_const = 1

	def update_pos_y(self ,  y , player):


		sign = +1 if player ==1 else -1

		self.queue.append(y)
		if len(self.queue) >self.lim_length:
			self.queue.popleft()
		if self.queue:
			self.speed_mag = (self.queue[-1] - self.queue[0])*self.speed_const
			self.speed_mag = abs(self.speed_mag)
		else:
			self.speed_mag = 0

		y_rat = y/10
		
		self.y_pos = self.y_mean - sign*((self.y_max*(y_rat))//self.stablizer)*self.stablizer

	def update_pos_x(self , x_rat ):
		w_mean = self.width//2 
		
		self.x_pos = w_mean + ((w_mean*x_rat)//self.stablizer)*self.stablizer

		

	def draw(self,pygame,DISPLAYSURF):
		pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x_pos),int(self.y_pos)), self.radius, 0)






class Computer_striker (Striker):

	def update_pos_y(self ,  y):
		pass

	def update_pos_x(self , puck):
		if puck.y_pos < self.height:
			if self.x_pos<=puck.x_pos:
				self.x_pos += self.x_speed
			else:
				self.x_pos -= self.x_speed
			
		if puck.y_pos < self.y_pos and abs(puck.x_pos - self.x_pos) < 10:
			self.x_pos = self.width//2



def init_striker1(width,height):
	global striker1
	striker1 = Striker(width,height,1)
	

def init_striker2(width,height,num_player):
	global striker2
	if num_player==1:
		striker2 = Computer_striker(width,height,2)
	else:
		striker2 = Striker(width,height,2)

# width = 300
# height = 600
# car = Car(width,height)

