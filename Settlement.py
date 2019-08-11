import Household
import random

##	TO DO
# 	Keep track of size of settlement

class Settlement:
	population = 0
	households = []
	terrain = []

	def __init__(self, terrain):
		self.terrain = terrain
		terrain.setSettlement()

	def getX(self, population):
		return self.terrain[0].x

	def getY(self, population):
		return self.terrain[0].y

	def tick(self):
		self.households.sort(key=lambda x: x.grain)
		for house in self.households:
			self.claimFields(house)
			#farm
			#rent_land
			house.grainTick() #consume_grain, storage loss
			#unclaim unused land
			#generational change
			#household fission

	def claimFields(self, house):
		claim_chance = random.random()
		### TODO: Ask Kiara if this is correct. Takes 2 workers to farm field, fields can grow up to worker number?
		### TODO: Implement known_patches and completing the claim
		known_patches = []
		if (claim_chance < house.ambition) and (house.workers > house.fields_owned) or (house.fields_owned <= 1):
			best_x = -1
			best_y = -1
			best_fertility = -1
			for patch in known_patches:
				if patch.fertility > best_fertility:
					best_x = patch.x
					best_y = patch.y
					best_fertility = patch.fertility

			self.terrain[best_x, best_y].claim(house)