from numpy import *


def calculateCoordinates( pos_x, pos_y, width, height):
	assert pos_x<20 and pos_y <20
	assert width == height and width % 40 == 0
	
	X = (width/20)*(pos_x+1) - width/40
	Y = (height/20)*(pos_y+1) - height/40
	#return the actual coordinates of the relavent object
	return array([X,Y]) 
