class Tank(object):
	def __init__(self, name = None, life = 0,pos_x = 0,pos_y = 0, image = None):
		self.name = name
		self.life = life
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image
		
		
class BrickWall:
	def __init__(self, life = 0,pos_x = 0,pos_y = 0, image = None):
		self.life = life
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image
		
class StoneWall:
	def __init__(self, pos_x = 0,pos_y = 0, image = None):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image
		
class Water:
	def __init__(self, pos_x = 0,pos_y = 0, image = None):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image