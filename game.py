import pygame , sys, os
import pygame_menu
import threading

import server
from pygame.locals import *
import math
from random import randint
import striker 
import time
import subprocess

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
		
		if striker2.disappear_striker == True:
			self.disappear = True
			self.disappear_time = time.time()
			striker2.disappear_striker = False


		# show ball after 10 secs
		if self.disappear and  time.time() - self.disappear_time>=10: # 10 secs
			self.disappear=False

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

		# goal condition point of 1
		if (self.y_pos < self.radius + self.collision_const) and \
		(self.x_pos > self.width//2 - 100 ) and \
		(self.x_pos < self.width//2 +100 ):
			score.update(s1=1)
			self.restart("striker1")

		# update position from speed


		self.x_pos += self.x_speed * dt * self.c_time
		self.y_pos += self.y_speed * dt * self.c_time



	def draw(self,pygame,DISPLAYSURF):
		if self.disappear == False:
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



	score.update(s1 = 0 , s2=0)

	score.draw(pygame,DISPLAYSURF)
	
	pygame.display.update()




	dt = fpsClock.tick(FPS)
	while True:
		dt = fpsClock.tick(FPS)
		DISPLAYSURF.fill(WHITE)
		DISPLAYSURF.blit(bg, (0, 0))
		striker.striker1.draw(pygame,DISPLAYSURF)
		if num_player==1:
			striker.striker2.update_pos_x(puck)
		striker.striker2.draw(pygame,DISPLAYSURF)

		puck.update(dt , striker.striker1 , striker.striker2)
		puck.draw(pygame,DISPLAYSURF)
		
		score.draw(pygame,DISPLAYSURF)
		draw_rect(height , width , DISPLAYSURF , pygame)
		pygame.display.update()
		fpsClock.tick(FPS)
# global num_player

def set_player(value , number):
	global num_player
	num_player = number
	striker.init_striker2(width,height,num_player)

def quit():
	# print("in quit")

	os._exit(0)

if __name__ == "__main__": 


	global num_player
	# num_player=1
	pygame.init()
	FPS = 20
	fpsClock = pygame.time.Clock()

	width = 400
	height = 600
	DISPLAYSURF = pygame.display.set_mode((width,height))
	pygame.display.set_caption('ICE HOCKEY')
	bg = pygame.image.load("bg.png") #INSIDE OF THE GAME LOOP gameDisplay.blit(bg, (0, 0)) 

	GREEN = (  0, 255,   0)
	RED = (255,0,0)
	WHITE = (0,0,0)



	menu = pygame_menu.Menu(300, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)
	process = subprocess.Popen(['ipconfig'], 
                           stdout=subprocess.PIPE)
	data_list=process.stdout.readlines()
	if len(data_list)<26:
		TEXT1="Connect Mobile Hotspot and Start Again"
	else:
		ip_data=data_list[25].decode("utf-8")
		ip=ip_data.split(":")[1].split("\r")[0]
		# menu.add_text_input('Name :', default='John Doe')

		TEXT1 = "Enter"+ip+":5001"+ "on your mobile " 
	TEXT2 =	"Tilt the mobile move the striker vertically " 
	TEXT3 = "Slider to control horizontal motion "
	menu.add_label(TEXT1 , max_char=-1, font_size=15)
	menu.add_label(TEXT2 , max_char=-1, font_size=15)
	menu.add_label(TEXT3 , max_char=-1, font_size=15)
	menu.add_selector('Opponent :', [('Select', 0) , ('Computer', 1), ('Player', 2)], onchange=set_player)
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
	
