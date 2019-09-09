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
		self.households = []
		terrain.settlement = True
		terrain.owner = self

		self.x = x
		self.y = y

	def tick(self):
		if self.parent.legacy_mode:
			self.households.sort(key=lambda x: -x.grain)
			for house in self.households:
				house.claimLand()
			random.shuffle(self.households)
		else:
			random.shuffle(self.households)
			for house in self.households:
				house.claimLand()

		for house in self.households:
			house.farm()
			house.grainTick() #consume_grain, storage loss
			house.generationalChange()
			house.populationIncrease()
		
		i = 0
		while (i < len(self.households)):
			if self.households[i].workers == 0:
				self.households[i].clearUp()
				self.parent.all_households.remove(self.households[i])

				del self.households[i]

			else:
				i += 1
		
		if self.parent.fission_enabled:
			self.fission()

	def fission(self):
		for i in range(len(self.households)):
			self.households[i].fission()
