from flask import Flask 
from flask_sockets import Sockets

import pygame , sys

from pygame.locals import *
import math
from random import randint
import time
import striker


app = Flask(__name__) 
sockets = Sockets(app)

@sockets.route('/accelerometer') 
def echo_socket(ws):
	f=open("accelerometer.txt","a")
	while True:
		message = ws.receive()
		print(message) 
		ws.send(message)
		print(message, file=f)
	f.close()


@sockets.route('/gyroscope')
def echo_socket(ws):
	f=open("gyroscope.txt","a")
	while True:
		message = ws.receive()
		print(message)
		ws.send(message)
		print(message, file=f)
	f.close()
	
@sockets.route('/magnetometer')
def echo_socket(ws):
	f=open("magnetometer.txt","a")
	while True:
		message = ws.receive()
		print(message)
		ws.send(message)
		print(message, file=f)
	f.close()

@sockets.route('/orientation')
def echo_socket(ws):
	global now
	while True:
		message = ws.receive()
		# print(message)
		x_data = float(message.split(",")[1])
		y_data = float(message.split(",")[2])
		z_data = float(message.split(",")[0])

		# print(x_data , y_data , z_data)
		if y_data>=0 and y_data<180:
			y_data = 360

		if y_data<270 and y_data>180:
			y_data = 270

		y_rat = (y_data-270)/90

		if x_data<180 and x_data>0:
			if x_data>45:
				x_data = 45
			x_rat = x_data/45
			striker.striker1.update_pos(-1* x_rat,y_rat)

		if x_data>180 and x_data<360:
			if x_data<315:
				x_data=315
			x_rat = (360-x_data)/45
			striker.striker1.update_pos(x_rat , y_rat)





@sockets.route('/stepcounter')
def echo_socket(ws):
	f=open("stepcounter.txt","a")
	while True:
		message = ws.receive()
		print(message)
		ws.send(message)
		print(message, file=f)
	f.close()

@sockets.route('/thermometer')
def echo_socket(ws):
	f=open("thermometer.txt","a")
	while True:
		message = ws.receive()
		print(message)
		ws.send(message)
		print(message, file=f)
	f.close()

@sockets.route('/lightsensor')
def echo_socket(ws):
	f=open("lightsensor.txt","a")
	while True:
		message = ws.receive()
		print(message)
		ws.send(message)
		print(message, file=f)
	f.close()

@sockets.route('/proximity')
def echo_socket(ws):
	f=open("proximity.txt","a")
	while True:
		message = ws.receive()
		print(message)
		ws.send(message)
		print(message, file=f)
	f.close()

@sockets.route('/geolocation')
def echo_socket(ws):
	f=open("geolocation.txt","a")
	while True:
		message = ws.receive()
		print(message)
		ws.send(message)
		print(message, file=f)
	f.close()

	

@app.route('/') 
def hello(): 
	return 'Hello World!'

def start(pygame1,DISPLAYSURF1):
	global pygame
	global DISPLAYSURF
	pygame,DISPLAYSURF = pygame1,DISPLAYSURF1


	# print(id(car))

	print("server started")
	global now
	now = time.time()
	from gevent import pywsgi
	from geventwebsocket.handler import WebSocketHandler
	server = pywsgi.WSGIServer(('0.0.0.0', 5001), app, handler_class=WebSocketHandler)

	server.serve_forever()
