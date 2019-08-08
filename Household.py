import Terrain
import random

class Household:
	grain = 0
	workers = 0
	ambition = 0
	competency = 0
	workers_worked = 0
	generation_countdown = 0
	fields_owned = []		#list of terrain
	fields_harvested = []	#list of terrain
	all_terrain = None

	distance_cost = 0

	x = 0
	y = 0

	settled_in = None

	def __init__(self, grain, workers, ambition, competency, distance_cost, x, y, all_terrain):
		self.grain = grain
		self.workers = workers
		self.ambition = ambition
		self.competency	= competency
		self.distance_cost = distance_cost
		self.x = x
		self.y = y
		self.all_terrain = all_terrain


	def grainTick(self):
		#ethnographic data suggests an adult needs an average of 160kg of grain per year to sustain.
		grain = grain - workers*160
		if grain < 0:
			num_not_supported = -grain/160
			grain = 0
			if num_not_supported < workers:
				workers = workers -  num_not_supported
			else:
				pass
		grain = grain * 0.9	#accounts for loss due to storage

	def populationIncrease(self):
		pass

	def farm(self):
		#set terrain harvested years not harvested to 0
		fields_owned.sort(key = lambda x: x.harvest)
		max_fields_to_work = workers//2
		
		total_harvest = 0
		workers_worked = 0
		fields_harvested = 0
		best_harvest = 0
		best_field = None

		for i in range(max_fields_to_work):
			#Stop harvesting if all owned fields have been harvested
			if fields_harvested >= len(fields_owned):
				break
			
			field = fields_owned[fields_harvested]

			farm_chance = random.random()
			## TODO: Ask Kiara if this is correct, in original code ambition was only 
			## taken into account if household had enough grain at start of year
			if grain < workers*160 or farm_chance < ambition*competency:
				field.harvested = True
				field.years_not_harvested = 0
				fields_harvested += 1
				workers_worked += 2

				# Cost of 300 to reseed field
				total_harvest += field.harvest - 300
				grain += field.harvest - 300

	def claimLand(self):
		claim_chance = random.random()
		### TODO: Ask Kiara if this is correct. Takes 2 workers to farm field, fields can grow up to worker number?
		### TODO: Implement known_patches
		if (claim_chance < ambition and workers > fields_owned) or fields_owned <= 1:
			best_x = -1
			best_y = -1
			best_fertility = -1
			for patch in known_patches:
				if patch.fertility > best_fertility:
					best_x = patch.x
					best_y = patch.y
					best_fertility = patch.fertility

			if all_terrain[best_x][best_y].claim(self):
				fields_owned += 1
				fields_owned.append(all_terrain[best_x][best_y])


	def unclaimLand():
		pass

	def rentLand():
		pass