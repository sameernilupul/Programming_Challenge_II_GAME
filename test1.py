import pygame,sys
from pygame.locals import *
from GameObjects import Tank 
from numpy import *
from Arena import *
from Calculations import *
#Parameters

FPS = 30
WIDTH = 760
HEIGHT = 760
fpsClock = pygame.time.Clock()
NUM_PLAYERS = 5
MY_TANK = pygame.image.load('./Resources/Tank1.png')
ENEMY_TANK = pygame.image.load('./Resources/Tank2.png')
GRASS = pygame.image.load('./Resources/Grass.png')
WATER = pygame.image.load('./Resources/Water.png')
STONE = pygame.image.load('./Resources/Rock.png')
BRICK = pygame.image.load('./Resources/Brick.png')
ARENA = getInitialArena()[0]
PLAYER = getInitialArena()[1]

# initialization

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT),0,32)
pygame.display.set_caption('Tank Game')

WHITE = (255,255,255)
catx =100
caty =100

Player1 = Tank("Name", 100,0,0,ENEMY_TANK)

beep = pygame.mixer.Sound('beeps.wav')
#pygame.mixer.music.load('/Users/sameernilupul/Music/paradise.mp3')
#pygame.mixer.music.play(-1,0.0)

print ARENA
#main loop
init =0;
while True:
	
	for x in range(0,20):
		for y in range(0,20):
			if ARENA[x*20+y] == 0: 							# Grass Land
				coordinates = calculateTopLeftCoordinates(x,y, 760,760)
				DISPLAYSURF.blit(GRASS,(coordinates[0],coordinates[1]))
			if ARENA[x*20+y] == 1: 							# Brick Wall
				coordinates = calculateTopLeftCoordinates(x,y, 760,760)
				DISPLAYSURF.blit(BRICK,(coordinates[0],coordinates[1]))
			if ARENA[x*20+y] == 2: 							# Stone Wall
				coordinates = calculateTopLeftCoordinates(x,y, 760,760)
				DISPLAYSURF.blit(STONE,(coordinates[0],coordinates[1]))
			if ARENA[x*20+y] == 3: 							# Water
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