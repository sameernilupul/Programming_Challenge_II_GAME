import pygame,sys
from pygame.locals import *
from GameObjects import Tank 
from numpy import *
from Arena import *
from Calculations import *
import thread
import socket
#Parameters

FPS = 30
WIDTH = 760
HEIGHT = 760
fpsClock = pygame.time.Clock()
NUM_PLAYERS = 5
MY_TANK = pygame.image.load('./Resources/Tank1.png')
ENEMY_TANK = pygame.image.load('./Resources/Tank2.png')
FALCON = pygame.image.load('./Resources/Falcon.png')
GRASS = pygame.image.load('./Resources/Grass.png')
WATER = pygame.image.load('./Resources/Water.png')
STONE = pygame.image.load('./Resources/Rock.png')
BRICK = pygame.image.load('./Resources/Brick.png')
COIN = pygame.image.load('./Resources/Coin.png')
ARENA = None
PLAYER = None

data = None
initialized = 0

# initialization

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT),0,32)
pygame.display.set_caption('Tank Game')

WHITE = (255,255,255)
catx =100
caty =100

Player1 = Tank("Name", 100,0,0,MY_TANK)

beep = pygame.mixer.Sound('beeps.wav')
#pygame.mixer.music.load('/Users/sameernilupul/Music/paradise.mp3')
#pygame.mixer.music.play(-1,0.0)



# Communication Thread	
def recieveData():
	global initialized
	global ARENA
	global PLAYER
	
	s = socket.socket()         # Create a socket object
	host = '192.168.1.1' 		# Get local machine name
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
   		c.close()                # Close the connection

#main Loop
def mainLoop():
	global initialized
	global catx
	init =0;	
	while True:
		if(initialized ==1):
			for x in range(0,20):
				for y in range(0,20):
					if ARENA[x*20+y] == 0:							## Grass Land
						coordinates = calculateTopLeftCoordinates(x,y, 760,760)
						DISPLAYSURF.blit(GRASS,(coordinates[0],coordinates[1]))
					if ARENA[x*20+y] == 1: 							## Brick Wall
						coordinates = calculateTopLeftCoordinates(x,y, 760,760)
						DISPLAYSURF.blit(BRICK,(coordinates[0],coordinates[1]))
					if ARENA[x*20+y] == 2: 							## Stone Wall
						coordinates = calculateTopLeftCoordinates(x,y, 760,760)
						DISPLAYSURF.blit(STONE,(coordinates[0],coordinates[1]))
					if ARENA[x*20+y] == 3: 							## Water
						coordinates = calculateTopLeftCoordinates(x,y, 760,760)
						DISPLAYSURF.blit(WATER,(coordinates[0],coordinates[1]))
	
			DISPLAYSURF.blit(Player1.image,(catx,caty))
			catx += 1
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
   		

