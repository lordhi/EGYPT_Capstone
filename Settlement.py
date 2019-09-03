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
			household = self.households[i]
			if household.workers > 15 and household.grain > 3 * household.workers * 164:
				fission_chance = random.random()
				if fission_chance > self.parent.min_fission_chance:
					grain = 1100
					workers = 5
					generation_countdown = random.randint(0, 5) + 10

					# Think which variables should be inherited from the previous household for extensibility purposes
					new_household = Household(self, grain, workers, household.minimum_ambition, household.minimum_competency, generation_countdown, household.knowledge_radius, household.distance_cost, self.x, self.y, household.all_terrain, household.x_size, household.y_size)

					self.households.append(new_household)
					self.parent.all_households.append(new_household)

					household.workers -= 5
					household.grain -= 1100
