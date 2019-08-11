import Household
import random

##	TO DO
# 	Keep track of size of settlement

class Settlement:
	population = 0
	households = []
	terrain = None
	x = -1
	y = -1

	def __init__(self, terrain):
		self.terrain = terrain
		terrain.settlement = True
		terrain.owner = self

	def tick(self):
		self.households.sort(key=lambda x: x.grain)
		for house in self.households:
			# self.claimFields(house)
			#farm
			#rent_land
			house.grainTick() #consume_grain, storage loss
			#unclaim unused land
			#generational change
			#household fission