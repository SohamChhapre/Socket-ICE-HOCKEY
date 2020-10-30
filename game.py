import pygame , sys, os
import pygame_menu
import threading

import server
from pygame.locals import *
import math
from random import randint
import striker 
import time
# import subprocess

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
		self.disappear = False
		self.disappear_time = 0
		self.def_speed = 5
		self.collision_const = 10
		self.disappear_striker_no = 0


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
		self.disappear = False

		striker.striker1.reset()
		striker.striker2.reset()
		
		

	def dist(self,a,b):
		return ((a.y_pos - b.y_pos)**2 + (a.x_pos-b.x_pos)**2)**0.5

	def atan(self,a,b):
		if abs(a.x_pos - b.x_pos)==0:
			if (a.y_pos - b.y_pos)>0:
				return math.pi/2
			else:
				return -math.pi/2
		return math.atan((a.y_pos - b.y_pos) / (a.x_pos - b.x_pos))
	
	def update(self , dt , striker1 , striker2):

		if (not(dt)):return

		if striker1.disappear_striker == True:
			self.disappear = True
			self.disappear_time = time.time()
			striker1.disappear_striker = False
			self.disappear_striker_no = 1
		
		if striker2.disappear_striker == True:
			self.disappear = True
			self.disappear_time = time.time()
			striker2.disappear_striker = False
			self.disappear_striker_no = 2


		# show ball after 10 secs
		if self.disappear and  time.time() - self.disappear_time>=10: # 10 secs
			self.disappear=False
			self.disappear_striker_no = 0

		# collsion with striker 1
		if (self.dist(striker1 , self) <= striker1.radius + self.radius + self.collision_const):
			self.max_speed = self.def_speed + striker1.speed_mag


			ang = self.atan(striker1 , self)

			if self.x_pos <= striker1.x_pos:	
				self.x_speed = -math.cos(ang) * self.max_speed
				self.y_speed = -math.sin(ang) * self.max_speed

			else:
				self.x_speed = math.cos(ang) * self.max_speed
				self.y_speed = math.sin(ang) * self.max_speed

		# collsion with striker 2
		if (self.dist(striker2 , self) <= striker2.radius + self.radius + self.collision_const):
			self.max_speed = self.def_speed + striker2.speed_mag

			ang = self.atan(striker2 , self)

			if self.x_pos <= striker2.x_pos:	
				self.x_speed = -math.cos(ang) * self.max_speed
				self.y_speed = -math.sin(ang) * self.max_speed

			else:
				self.x_speed = math.cos(ang) * self.max_speed
				self.y_speed = math.sin(ang) * self.max_speed


		# collision with left wall

		if self.x_pos - self.radius -  self.collision_const < 0 :
			self.x_speed = -self.x_speed
			self.x_pos = self.radius +  self.collision_const
		
		# collision with right wall

		if self.x_pos + self.radius + self.collision_const > self.width:
			self.x_speed = -self.x_speed
			self.x_pos = self.width - self.radius - self.collision_const

		# collision with top wall

		if self.y_pos < self.radius :
			self.y_pos = self.radius 
			self.y_speed = -self.y_speed

		# collision with bottom wall

		if self.y_pos > self.height - self.radius :
			self.y_pos = self.height - self.radius 
			self.y_speed = -self.y_speed

		# goal condition point of 2
		if (self.y_pos > self.height - self.radius - self.collision_const) and \
		(self.x_pos > self.width//2 - 100 ) and \
		(self.x_pos < self.width//2 +100):
			score.update(s2=1)
			self.restart("striker2")
			score.draw(pygame,DISPLAYSURF)
			pygame.display.update()
			time.sleep(1)

		# goal condition point of 1
		if (self.y_pos < self.radius + self.collision_const) and \
		(self.x_pos > self.width//2 - 100 ) and \
		(self.x_pos < self.width//2 +100 ):
			score.update(s1=1)
			self.restart("striker1")
			score.draw(pygame,DISPLAYSURF)
			pygame.display.update()
			time.sleep(1)

		# update position from speed


		self.x_pos += self.x_speed * dt * self.c_time
		self.y_pos += self.y_speed * dt * self.c_time



	def draw(self,pygame,DISPLAYSURF):
		if self.disappear == False:
			pygame.draw.circle(DISPLAYSURF, self.red, (int(self.x_pos),int(self.y_pos)), self.radius, 0)
		else:
			if self.disappear_striker_no == 1 and self.y_pos > self.height//2:
				pygame.draw.circle(DISPLAYSURF, self.red, (int(self.x_pos),int(self.y_pos)), self.radius, 0)
			if self.disappear_striker_no == 2 and self.y_pos < self.height//2:
				pygame.draw.circle(DISPLAYSURF, self.red, (int(self.x_pos),int(self.y_pos)), self.radius, 0)




class Score:
	def __init__(self,pygame,width,height):
		self.width = width
		self.height = height
		self.score1 = 0
		self.score2 = 0
		self.color = (0,0,200)
		self.back = (255,255,255)
		self.fontObj = pygame.font.Font('freesansbold.ttf', 20)
		output = "1: " + str(self.score1) + " || 2: "+str(self.score2)
		self.textSurfaceObj = self.fontObj.render(output , True, self.color, self.back)
		self.textRectObj = self.textSurfaceObj.get_rect()
		self.textRectObj.center = (self.width//2, self.height//2)
		
	def update(self,s1 = 0,s2 = 0):

		self.score1 += s1
		self.score2 += s2
		output = "1: " + str(self.score1) + " || 2: "+str(self.score2)
		self.textSurfaceObj = self.fontObj.render(output, True, self.color, self.back)
		self.textRectObj = self.textSurfaceObj.get_rect()
		self.textRectObj.center = (self.width//2, self.height//2)
		
		

	def text(self,t):
		self.textSurfaceObj = self.fontObj.render(t, True, self.color, self.back)
		self.textRectObj = self.textSurfaceObj.get_rect()
		self.textRectObj.center = (self.width//2, self.height//2)

	def draw(self,pygame,DISPLAYSURF):
		# DISPLAYSURF.fill(self.back)
		DISPLAYSURF.blit(self.textSurfaceObj, self.textRectObj)

def draw_rect(hieght , width , DISPLAYSURF , pygame):
	color = (200,200,200)
	r = ((width//2)-100 , 0 , 200 , 10)
	pygame.draw.rect(DISPLAYSURF , color , r )
	r = ((width//2)-100 , height-10 , 200 , 10)
	pygame.draw.rect(DISPLAYSURF , color , r )


def game():

	global total_points

	DISPLAYSURF.fill(WHITE)
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



	# score.update(s1 = 0 , s2=0)

	score.draw(pygame,DISPLAYSURF)
	
	pygame.display.update()
	dt = fpsClock.tick(FPS)
	quit = 0
	while True:

		dt = fpsClock.tick(FPS)
		ev = pygame.event.get()
		for event in ev:
		# handle MOUSEBUTTONUP
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					pause()
				if event.key == pygame.K_q:
					quit = 1
					break
		if quit ==1:
			break

		
		DISPLAYSURF.fill(WHITE)
		DISPLAYSURF.blit(bg, (2, -2))
		striker.striker1.draw(pygame,DISPLAYSURF)
		if num_player==1:
			striker.striker2.update_pos_x(puck)
		striker.striker2.draw(pygame,DISPLAYSURF)
		score.draw(pygame,DISPLAYSURF)
		puck.update(dt , striker.striker1 , striker.striker2)
		puck.draw(pygame,DISPLAYSURF)

		if score.score2 >= total_points or score.score1 >= total_points:
			if score.score2 >= total_points:
				score.text("Player2 win")
			else:
				score.text("Player1 win")
			score.draw(pygame,DISPLAYSURF)
			pygame.display.update()
			time.sleep(1)

			score.score2 = 0
			score.score1 = 0
			break
		
		
		draw_rect(height , width , DISPLAYSURF , pygame)
		pygame.display.update()
		fpsClock.tick(FPS)
# global num_player

def set_player(value , number):
	global num_player
	num_player = number
	striker.init_striker2(width,height,num_player)

def set_points(value , number):
	global total_points
	total_points = number

def set_y_control(value , number):

	striker.y_control = number
	# 1- slider , 2 - sensor

def pause():

	DISPLAYSURF.fill(WHITE)
	score.text("PAUSE")
	score.draw(pygame,DISPLAYSURF)
	pygame.display.update()
	flag = 0
	while(True):

		dt = fpsClock.tick(10)
		ev = pygame.event.get()
		for event in ev:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				flag = 1
				break
		if flag == 1:
			break
	score.update(s1 = 0 , s2=0)
	return 


def quit():
	# print("in quit")

	os._exit(0)

if __name__ == "__main__": 


	global num_player
	global total_points
	num_player=1
	global y_control
	y_control = 1
	pygame.init()
	FPS = 60
	fpsClock = pygame.time.Clock()

	width = 400
	height = 600
	DISPLAYSURF = pygame.display.set_mode((width,height))
	pygame.display.set_caption('ICE HOCKEY')
	bg = pygame.image.load("bg.png") #INSIDE OF THE GAME LOOP gameDisplay.blit(bg, (0, 0)) 

	GREEN = (  0, 255,   0)
	RED = (255,0,0)
	WHITE = (0,0,0)



	menu = pygame_menu.Menu(400, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)



	TEXT2 =	"Tilt the mobile move the striker vertically " 
	TEXT3 = "Slider to control horizontal motion "

	menu.add_label(TEXT2 , max_char=-1, font_size=15)
	menu.add_label(TEXT3 , max_char=-1, font_size=15)

	menu.add_selector('Opponent :', [('Select', 0) , ('Computer', 1), ('Player', 2)], onchange=set_player)
	menu.add_selector('Total Points :', [('Select', 0) ,('5', 5) , ('11', 11), ('21', 21)], onchange= set_points)
	menu.add_selector('Y_COntrol :', [('Select', 0) ,('Slider', 1) , ('sensor', 2)], onchange= set_y_control)
	menu.add_button('Play', game)
	menu.add_button('Quit', quit)

	# menu.add_button('Quit', pygame_menu.events.EXIT)

	
	
	striker.init_striker1(width,height)
	# striker.init_striker2(width,height,1)
	
	score = Score(pygame,width,height)
	puck = Puck(width,height)

	t1 = threading.Thread(target=menu.mainloop, args=(DISPLAYSURF,)) 
	# t1 = threading.Thread(target=game, args=()) 
	t2 = threading.Thread(target=server.start, args=(pygame,DISPLAYSURF,))
	# server.start(pygame,DISPLAYSURF)

	# t1.start()
	t2.start() 
	menu.mainloop(DISPLAYSURF)
	t1.start()
	

	t1.join()
	t2.join()
	
