from Terrain import Terrain
import random
import numpy as np
import math

class Household:
	grain = 0
	workers = 0
	ambition = 0
	competency = 0
	workers_worked = 0
	generation_countdown = 1
	generational_variation = 0.2
	minimum_ambition = 0
	minimum_competency = 0
	fallow_limit = 5
	fields_owned = []		#list of terrain
	fields_harvested = 0	
	
	known_patches = []
	knowledge_radius = 0

	distance_cost = 0

	all_terrain = None
	x_size = 0
	y_size = 0

	x = 0
	y = 0

	settled_in = None

	def __init__(self,settled_in, grain, workers, min_ambition, min_competency, generation_countdown, knowledge_radius, distance_cost, x, y, all_terrain, x_size, y_size):
		self.grain = grain
		self.workers = workers
		self.ambition = min_ambition + (random.random()*(1 - min_ambition))
		self.competency = min_competency + (random.random()*(1 - min_competency))
		self.minimum_ambition = min_ambition
		self.minimum_competency = min_competency
		# self.ambition = ambition
		# self.competency	= competency
		self.workers_worked = 0
		self.generation_countdown = generation_countdown
		self.knowledge_radius = knowledge_radius
		self.distance_cost = distance_cost
		self.x = x
		self.y = y
		self.x_size = x_size
		self.y_size = y_size
		self.all_terrain = all_terrain
		self.settled_in = settled_in
		self.fields_owned = []
		self.fields_harvested = 0
		self.known_patches = []

		self.settled_in.population += workers

		min_y = y-knowledge_radius
		min_y = 0 if min_y < 0 else min_y
		max_y = y+knowledge_radius
		max_y = y_size if max_y > y_size else max_y

		min_x = x-knowledge_radius
		min_x = 0 if min_x < 0 else min_x
		max_x = x+knowledge_radius
		max_x = x_size if max_x > x_size else max_x

		for x in range(min_x, max_x):
			for y in range(min_y, max_y):
				distance = ((x-self.x)**2 + (y-self.y)**2)**0.5
				if distance < knowledge_radius and not all_terrain[x][y].river:
					self.known_patches.append(all_terrain[x][y])

	def grainTick(self):
		#ethnographic data suggests an adult needs an average of 160kg of grain per year to sustain.
		self.grain -= self.workers*160
		if self.grain < 0:
			num_not_supported = math.ceil(self.grain/160)
			self.grain = 0
			if num_not_supported < self.workers:
				self.workers -= num_not_supported
				self.settled_in.population -= num_not_supported
				self.settled_in.parent.total_population -= num_not_supported
			else:
				self.settled_in.population -= self.workers
				self.settled_in.parent.total_population -= self.workers
				self.workers = 0
		self.grain = self.grain * 0.9	#accounts for loss due to storage
		self.settled_in.parent.total_grain += self.grain

	def populationIncrease(self):
		pass

	def farm(self):
		self.fields_owned.sort(key = lambda x: x.harvest)
		max_fields_to_work = int(self.workers//2)

		total_harvest = 0
		self.workers_worked = 0
		self.fields_harvested = 0
		best_harvest = 0
		best_field = None
		for i in range(max_fields_to_work):
			#Stop harvesting if all owned fields have been harvested
			if self.fields_harvested >= len(self.fields_owned):
				break
			
			field = self.fields_owned[self.fields_harvested]

			farm_chance = random.random()
			## TODO:
			## Consider better way of performing ambition calculation,
			## original method was rapid way of getting the code working
			if self.grain < self.workers*160 or farm_chance < self.ambition*self.competency:
				field.harvested = True
				field.years_not_harvested = 0
				self.fields_harvested += 1
				self.workers_worked += 2
				field_harvest = field.fertility*field.max_yield*self.competency - field.house_distance*field.owner.distance_cost - 300
				
				total_harvest += field_harvest
		self.grain += total_harvest

		i = self.fields_harvested
		if self.fallow_limit > 0:
			while i < len(self.fields_owned):
				if self.fields_owned[i].years_not_harvested > self.fallow_limit:
					self.fields_owned[i].unclaim()
					del self.fields_owned[i]
				i += 1

	def claimLand(self):
		claim_chance = random.random()
		### TODO: Ask Kiara if this is correct. Takes 2 workers to farm field, fields can grow up to worker number?
		### TODO: Implement known_patches
		if (claim_chance < self.ambition and self.workers > len(self.fields_owned)) or (len(self.fields_owned) <= 1 and self.workers > 0):
			best_x = -1
			best_y = -1
			best_fertility = -1
			for patch in self.known_patches:
				if patch.fertility > best_fertility and not patch.owned and not patch.settlement and not patch.settlement_territory:
					best_x = patch.x
					best_y = patch.y
					best_fertility = patch.fertility

			if self.all_terrain[best_x][best_y].claim(self):
				self.fields_owned.append(self.all_terrain[best_x][best_y])

	def rentLand(self, land_rental_rate):
		total_harvest = 0
		max_fields_to_work = (self.workers - self.workers_worked)//2

		for i in range(max_fields_to_work):
			best_harvest = 0
			best_field = self.all_terrain[self.x][self.y]

			for field in self.known_patches:
				this_harvest = field.fertility*field.max_yield*self.competency - (((self.x - field.x)**2 + (self.y - field.y)**2)**0.5)*self.distance_cost
				if not field.harvested and this_harvest >= best_harvest: # this_harvest > best_harvest ?
					best_field = field
					best_harvest = this_harvest

			harvest_chance = random.random()

			if best_field.field and field not in self.fields_owned and harvest_chance < (self.ambition * self.competency):
				field.harvested = True
				# shape
				# color

				total_harvest += best_harvest * (1 - (land_rental_rate/100)) - 300

				best_field.owner.grain += best_harvest * (land_rental_rate/100)
		
			self.fields_harvested += 1

		self.grain += total_harvest

	def generationalChange(self):
		self.generation_countdown -= 1
		if self.generation_countdown <= 0:
			self.generation_countdown = random.randrange(0,5) + 10

			ambition_change = 2*self.generational_variation*(random.random() - 0.5)
			while self.ambition + ambition_change > 1 or self.ambition + ambition_change < self.minimum_ambition:
				ambition_change = 2*self.generational_variation*(random.random() - 0.5)
			
			self.ambition += ambition_change

			competency_change = 2*self.generational_variation*(random.random() - 0.5)
			while self.competency + competency_change > 1 or self.competency + competency_change < self.minimum_competency:
				competency_change = 2*self.generational_variation*(random.random() - 0.5)
			
			self.competency += competency_change

	
