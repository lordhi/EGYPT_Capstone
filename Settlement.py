import Household
import random

##	TO DO
# 	Keep track of size of settlement

class Settlement:
	population = 0
	households = []
	terrain = None
	rent_enabled = False
	x = -1
	y = -1

	def __init__(self, terrain, x, y):
		self.terrain = terrain
		terrain.settlement = True
		terrain.owner = self

		self.x = x
		self.y = y

	def tick(self):
		self.households.sort(key=lambda x: x.grain)
		for house in self.households:
			house.claimLand()
			house.farm()
			if self.rent_enabled:
				house.rentLand()
			house.grainTick() #consume_grain, storage loss
			house.generationalChange()
			#household fission