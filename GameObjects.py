class Tank(object):
	def __init__(self, name = None, life = 0,pos_x = 0,pos_y = 0, image = None, direction = None):
		self.name = name
		self.life = life
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image
		self.speed = 1
		self.direction = direction
		self.coins = 0
		self.points = 0
		self.shooting = 0
		
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
		
class Bullet:
	def __init__(self, pos_x = 0,pos_y = 0, image = None):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image
		self.speed = 3
		
class Coins:
	def __init__(self, pos_x = 0,pos_y = 0, amount = 0, life_time = 0):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.amount = amount
		self.lifetime = life_time