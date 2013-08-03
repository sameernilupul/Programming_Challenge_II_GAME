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
NUM_PLAYERS = 4
ENEMY_TANK = pygame.image.load('./Resources/Tank1.png')
MY_TANK = pygame.image.load('./Resources/Tank2.png')
FALCON = pygame.image.load('./Resources/Falcon.png')
GRASS = pygame.image.load('./Resources/Grass.png')
WATER = pygame.transform.scale(pygame.image.load('./Resources/Water.png'), (38, 38))
STONE = pygame.transform.scale(pygame.image.load('./Resources/Rock.png'), (38, 38))
BRICK = pygame.transform.scale(pygame.image.load('./Resources/Brick.png'), (38, 38))
HEART = pygame.transform.scale(pygame.image.load('./Resources/Heart.png'), (38, 38))
COIN = pygame.image.load('./Resources/Coin.png')
BULLET = pygame.image.load('./Resources/Bullet.gif')
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
COINS = []
HEALTH = []
BULLETS = []

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
	print input_string
	if(case == 1):
		data = input_string.split(':')
		data[-1] = data[-1][:-1]
		for i in range(0,NUM_PLAYERS):
			details = data[i+1].split(';')
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
			
	if(case ==2):
		data = input_string.split(':')
		data[3] = data[3][:-1]
		coordinates = data[1].split(',')
		COINS.append(Coins(int(coordinates[0]),int(coordinates[1]),int(data[3]),int(data[2])))
	
	if(case ==3):
		data = input_string.split(':')
		data[2] = data[2][:-1]
		coordinates = data[1].split(',')
		HEALTH.append(Life(int(coordinates[0]),int(coordinates[1]),int(data[2])))
	
# Communication Thread	
def recieveData():
	global initialized
	global ARENA
	global PLAYER
	global updated
	global COINS
	
	s = socket.socket()         # Create a socket object
	host = '192.168.1.2' 		# Get local machine name
	port = 12345                # Reserve a port for your service.
	s.bind((host, port))        # Bind to the port
	print host
	s.listen(5)                 # Now wait for client connection.
	while True:
   		c, addr = s.accept()     # Establish connection with client.
   		data = c.recv(1024)
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
   		elif(data[0] == 'L' and data[1] == ':'):
   			update(data,3)
   			updated = 3
   		c.close()                # Close the connection
   		#Reduce life time of coins and health
   		for i in range(0,len(COINS)):
   			COINS[i].lifetime -=1000
   		for i in range(0,len(HEALTH)):
   			HEALTH[i].lifetime -=1000
   		
   		for i in range(0,NUM_PLAYERS):
   			if(TANKS[i].shooting ==1):
   				coordinates = calculateTopLeftCoordinates(TANKS[i].pos_x,TANKS[i].pos_y,760,760)
   				if(TANKS[i].direction ==0):
   					bullet_image = BULLET
   				elif(TANKS[i].direction ==1):
   					bullet_image = pygame.transform.rotate(BULLET, -90)
   				elif(TANKS[i].direction ==2):
   					bullet_image = pygame.transform.rotate(BULLET, 180)
   				elif(TANKS[i].direction ==3):
   					bullet_image = pygame.transform.rotate(BULLET, 90)
   				BULLETS.append(Bullet(coordinates[0],coordinates[1],TANKS[i].direction,bullet_image))  
   		
   		

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
			
			#display coins
			remove =[]
			for i in range(0,len(COINS)):
				if(COINS[i].lifetime <= 1000):
					remove.append(i)
				coin = COINS[i]
				coordinates = calculateTopLeftCoordinates(coin.pos_x,coin.pos_y,760,760)
				DISPLAYSURF.blit(COIN,(coordinates[0]-5,coordinates[1]-5))
				
			#remove coins
			for i in range(0,NUM_PLAYERS):
				for j in range(0,len(COINS)):
					if(TANKS[i].pos_x == COINS[j].pos_x and TANKS[i].pos_y == COINS[j].pos_y):
						remove.append(j)
			remove = set(remove)
			remove = list(remove)
			for i in range(0,len(remove)):
				coin = COINS.pop(remove[i])
			
			# display health
			remove =[]
			for i in range(0,len(HEALTH)):
				if(HEALTH[i].lifetime <= 1000):
					remove.append(i)
				life = HEALTH[i]
				coordinates = calculateTopLeftCoordinates(life.pos_x,life.pos_y,760,760)
				DISPLAYSURF.blit(HEART,(coordinates[0],coordinates[1]))
				
			#remove health
			for i in range(0,NUM_PLAYERS):
				for j in range(0,len(HEALTH)):
					if(TANKS[i].pos_x == HEALTH[j].pos_x and TANKS[i].pos_y == HEALTH[j].pos_y):
						remove.append(j)
			remove = set(remove)
			remove = list(remove)
			for i in range(0,len(remove)):
				coin = HEALTH.pop(remove[i])
				
			#display bullets
			for i in range(0,len(BULLETS)):
				DISPLAYSURF.blit(BULLETS[i].image,(BULLETS[i].pos_x,BULLETS[i].pos_y))
			#beep.play()
			#display tanks
			for i in range(0,NUM_PLAYERS):
				if(TANKS[i].life > 0):
					coordinates = calculateTopLeftCoordinates(TANKS[i].pos_x,TANKS[i].pos_y,760,760)
					DISPLAYSURF.blit(TANKS[i].image,(coordinates[0]-10,coordinates[1]-10))
					
			#update Bullets
			for i in range(0,len(BULLETS)):
				if(BULLETS[i].direction ==0):
					BULLETS[i].pos_y -= 12
				elif(BULLETS[i].direction ==1):
					BULLETS[i].pos_x += 12
				elif(BULLETS[i].direction ==2):
					BULLETS[i].pos_y += 12
				elif(BULLETS[i].direction ==3):
					BULLETS[i].pos_x -= 12
	
	
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
   		

