from Household import Household
import random

##	TO DO
# 	Keep track of size of settlement

class Settlement:
	__slots__ = "population", "terrain", "households", "x", "y"
	parent = None

	def __init__(self, terrain, x, y):
		self.population = 0
		self.terrain = terrain
		self.households = []
		terrain.settlement = True
		terrain.owner = self

		self.x = x
		self.y = y

	def tick(self):
		'''Performs actions in each household which should take place before renting would occur if enabled'''
		if self.parent.legacy_mode:
			self.households.sort(key=lambda x: x.grain, reverse=True)
			for house in self.households:
				house.claimLand()
			random.shuffle(self.households)
		else:
			random.shuffle(self.households)
			for house in self.households:
				house.claimLand()

		for house in self.households:
			house.farm()

	def tock(self):
		'''Performs actions in each household which should take place after renting would occur if enabled'''
		for house in self.households:
			house.grainTick() #consumes grain, kills people who aren't fed, performs storage loss
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
