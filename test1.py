import pygame,sys
from pygame.locals import *
from GameObjects import Tank 
from numpy import *
from Arena import *
from Calculations import *
import thread
import socket
from copy import copy, deepcopy
#Parameters

FPS = 30
WIDTH = 1260
HEIGHT = 760
fpsClock = pygame.time.Clock()
NUM_PLAYERS = 5
ENEMY_TANK = pygame.image.load('./Resources/Tank1.png')
MY_TANK = pygame.image.load('./Resources/Tank2.png')
FALCON = pygame.image.load('./Resources/Falcon.png')
GRASS = pygame.image.load('./Resources/Grass.png')
WATER = pygame.transform.scale(pygame.image.load('./Resources/Water.png'), (38, 38))
STONE = pygame.transform.scale(pygame.image.load('./Resources/Rock.png'), (38, 38))
BRICK = pygame.transform.scale(pygame.image.load('./Resources/Brick.png'), (38, 38))
COIN = pygame.image.load('./Resources/Coin.png')
BACKGROUND = pygame.image.load('./Resources/Background.png')
MENU = pygame.image.load('./Resources/Menu.png')
SCORE_CARD = pygame.Surface((400,400))  # the size of your rect

ARENA = None
PLAYER = None

data = None
initialized = 0
updated = 0
# initialization

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT),0,32)
pygame.display.set_caption('Tank Game')
SCORE_CARD.set_alpha(150)                # alpha level

TANKS = [Tank("My_Tank", 100,0,0,MY_TANK,0),Tank("Enemy 1", 100,0,0,ENEMY_TANK,0),Tank("Enemy 2", 100,0,0,ENEMY_TANK,0),Tank("Enemy 3", 100,0,0,ENEMY_TANK,0),Tank("Enemy 4", 100,0,0,ENEMY_TANK,0)]
TANKS_PREVIOUS = None

beep = pygame.mixer.Sound('beeps.wav')
#pygame.mixer.music.load('/Users/sameernilupul/Music/paradise.mp3')
#pygame.mixer.music.play(-1,0.0)

def updateScorecard():
	SCORE_CARD.fill((0,0,0))
	pygame.draw.rect(SCORE_CARD, (0,0,0), [4,4 , 393, 493], 10)
	myfont = pygame.font.SysFont("PTSans", 25, True)
	label = myfont.render("ID    Points    Coins    Health", 20, (255,255,255))
	SCORE_CARD.blit(label, (15, 20))
	
	for i in range(0,NUM_PLAYERS):
		label = myfont.render("  "+str(i), 20, (255,255,255))
		SCORE_CARD.blit(label, (5, 50*(i+1)+20))
		label = myfont.render(str(TANKS[i].points), 20, (255,255,255))	
		SCORE_CARD.blit(label, (80, 50*(i+1)+20))
		label = myfont.render(str(TANKS[i].coins), 20, (255,255,255))
		SCORE_CARD.blit(label, (190, 50*(i+1)+20))
		label = myfont.render(str(TANKS[i].life), 20, (255,255,255))
		SCORE_CARD.blit(label, (310, 50*(i+1)+20))
		
def update(input_string, case):
	global TANKS
	global TANKS_PREV
	TANKS_PREV = deepcopy(TANKS)
	print updated
	if(case == 1):
		data = input_string.split(':')
		data[-1] = data[-1][:-1]
		for i in range(0,NUM_PLAYERS):
			details = data[i+1].split(';')
			print details
			coordinates = details[1].split(',')
			TANKS[i].pos_x = int(coordinates[0])
			TANKS[i].pos_y = int(coordinates[1])
			TANKS[i].direction = int(details[2])
			TANKS[i].shooting = int(details[3])
			TANKS[i].life = int(details[4])
			TANKS[i].coins = int(details[5])
			TANKS[i].points = int(details[6])
		
			angle = TANKS[i].direction - TANKS_PREV[i].direction
			if(angle == 3 or angle == -3):
				angle = angle/(-3)
			TANKS[i].image = pygame.transform.rotate(TANKS[i].image, -90*angle)
	
	elif(case == 2):
		data = input_string.split(':')
	
# Communication Thread	
def recieveData():
	global initialized
	global ARENA
	global PLAYER
	global updated
	s = socket.socket()         # Create a socket object
	host = '192.168.1.2' 		# Get local machine name
	port = 12345                # Reserve a port for your service.
	s.bind((host, port))        # Bind to the port
	print host
	s.listen(5)                 # Now wait for client connection.
	while True:
   		c, addr = s.accept()     # Establish connection with client.
   		data = c.recv(1024)
   		print data
   		if(data[0] == 'I'):
   			ARENA = getInitialArena(data)[0]
   			PLAYER = getInitialArena(data)[1]
   			initialized = 1
   		elif(data[0] == 'G' and data[1] == ':'):
   			update(data,1)
   			updated = 1
   		elif(data[0] == 'C' and data[1] == ':'):
   			update(data,2)
   			updated = 2
   		c.close()                # Close the connection

#main Loop
def mainLoop():
	global initialized
	init =0;	
	while True:
		#display menu and background
		DISPLAYSURF.blit(BACKGROUND,(0,0))
		DISPLAYSURF.blit(MENU,(760,0))
		pygame.draw.rect(DISPLAYSURF, (0,0,0), [760, 0, 500, 760], 7)
		
		myfont = pygame.font.SysFont("PTSans", 47, True)
		label = myfont.render("The Battle of Kursk", 10, (255,255,240))
		DISPLAYSURF.blit(label, (780, 40))
		
		updateScorecard()
		DISPLAYSURF.blit(SCORE_CARD,(810,200))
		
		#end of displaying menu and background
		
		if(initialized ==1):
			for x in range(0,20):
				for y in range(0,20):
					#if ARENA[x*20+y] == 0:							## Grass Land
						#coordinates = calculateTopLeftCoordinates(x,y, 760,760)
						#DISPLAYSURF.blit(GRASS,(coordinates[0],coordinates[1]))
					if ARENA[x*20+y] == 1: 							## Brick Wall
						coordinates = calculateTopLeftCoordinates(x,y, 760,760)
						DISPLAYSURF.blit(BRICK,(coordinates[0],coordinates[1]))
					if ARENA[x*20+y] == 2: 							## Stone Wall
						coordinates = calculateTopLeftCoordinates(x,y, 760,760)
						DISPLAYSURF.blit(STONE,(coordinates[0],coordinates[1]))
					if ARENA[x*20+y] == 3: 							## Water
						coordinates = calculateTopLeftCoordinates(x,y, 760,760)
						DISPLAYSURF.blit(WATER,(coordinates[0],coordinates[1]))
			
			for i in range(0,NUM_PLAYERS):
				if(TANKS[i].life > 0):
					coordinates = calculateTopLeftCoordinates(TANKS[i].pos_x,TANKS[i].pos_y,760,760)
					DISPLAYSURF.blit(TANKS[i].image,(coordinates[0]-10,coordinates[1]-10))
			
			beep.play()
	
	
	
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		pygame.display.update()
		fpsClock.tick(FPS)
	
	
# Starting threads

try:
   thread.start_new_thread(recieveData,())
   thread.start_new_thread(mainLoop,())
except:
   print "Error: unable to start thread"
while 1:
   pass
   		

