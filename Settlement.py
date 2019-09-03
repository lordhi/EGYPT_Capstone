from Household import Household
import random

##	TO DO
# 	Keep track of size of settlement

class Settlement:
	population = 0
	households = []
	terrain = None
	rent_enabled = False
	parent = None
	x = -1
	y = -1

	def __init__(self, terrain, x, y):
		self.population = 0
		self.terrain = terrain
		terrain.settlement = True
		terrain.owner = self

		self.x = x
		self.y = y

	def tick(self):
		random.shuffle(self.households)
		self.households.sort(key=lambda x: x.grain)
		for house in self.households:
			house.claimLand()
			house.farm()
			house.grainTick() #consume_grain, storage loss
			house.generationalChange()
		
		i = 0
		while (i < len(self.households)):
			if self.households[i].workers == 0:
				self.households[i].clearUp()
				del self.households[i]
			else:
				i += 1
		self.fission()

	def fission(self):
		for i in range(len(self.households)):
			self.households[i].fission()
