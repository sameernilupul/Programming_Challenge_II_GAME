import pygame,sys
from pygame.locals import *

FPS = 30
WIDTH = 1000
HEIGHT = 700
fpsClock = pygame.time.Clock()
NUM_PLAYERS = 5
MY_TANK = pygame.image.load('./Resources/Tank1.png')
ENEMY_TANK = pygame.image.load('./Resources/Tank2.png')
GRASS = pygame.image.load('./Resources/Grass.png')
WATER = pygame.image.load('./Resources/Water.png')
ROCK = pygame.image.load('./Resources/Rock.png')
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT),0,32)
pygame.display.set_caption('Tank Game')

WHITE = (255,255,255)
cat = pygame.image.load('./Resources/Tank1.png')
catx =100
caty =100

beep = pygame.mixer.Sound('beeps.wav')
#pygame.mixer.music.load('/Users/sameernilupul/Music/paradise.mp3')
#pygame.mixer.music.play(-1,0.0)

while True:
	DISPLAYSURF.fill(WHITE)
	DISPLAYSURF.blit(cat,(catx,caty))
	catx += 1
	beep.play()
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
	fpsClock.tick(FPS)