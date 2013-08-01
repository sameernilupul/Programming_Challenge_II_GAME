from numpy import *

def getInitialArena(initial_string):
	data = initial_string.split(':')
	data[4] = data[4][:-1]
	arena = zeros(400,dtype('i'))
	arena.reshape(20,20)
	object_type = 0
	for i in range(2,5):
		coordinates = data[i].split(';')
		if(i == 2):
			object_type = 1 # 1 -> Brick
		if(i == 3):
			object_type = 2 # 2 -> Stone
		if(i == 4):
			object_type = 3	# 3 -> Water
		for index in range(0,len(coordinates)):
			coordinate = coordinates[index].split(',')
			arena[int(coordinate[0])*20 +int(coordinate[1])] = object_type
	
	return [arena,data[1]]