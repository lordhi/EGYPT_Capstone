from Terrain import Terrain
import random
import numpy as np
import math

class Household:
	__slots__ = "color", "grain", "workers", "ambition", "competency","minimum_ambition", "minimum_competency", "workers_worked", "generation_countdown", "min_fission_chance", "knowledge_radius", "distance_cost", "land_rental_rate", "fallow_limit", "x", "y", "x_size", "y_size", "all_terrain", "settled_in", "fields_owned", "fields_harvested", "known_patches", "legacy_mode", "generational_variation"
	
	def __init__(self, settled_in, grain, workers, min_ambition, min_competency, min_fission_chance, knowledge_radius, distance_cost, land_rental_rate, fallow_limit, x, y, all_terrain, x_size, y_size, generational_variance, legacy_mode):
		self.color = None
		self.grain = grain
		self.workers = workers
		self.ambition = self.randomRange(min_ambition, 1) # min_ambition + (random.random()*(1 - min_ambition))
		self.competency = self.randomRange(min_competency, 1) # min_competency + (random.random()*(1 - min_competency))
		self.minimum_ambition = min_ambition
		self.minimum_competency = min_competency
		self.workers_worked = 0
		self.generation_countdown = random.randint(0, 5) + 10
		self.min_fission_chance = min_fission_chance
		self.knowledge_radius = knowledge_radius
		self.distance_cost = distance_cost
		self.land_rental_rate = land_rental_rate
		self.fallow_limit = fallow_limit
		self.x = x
		self.y = y
		self.x_size = x_size
		self.y_size = y_size
		self.all_terrain = all_terrain
		self.settled_in = settled_in
		self.fields_owned = []
		self.fields_harvested = 0
		self.known_patches = []
		self.legacy_mode = legacy_mode
		self.generational_variation = generational_variance

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
				if not all_terrain[x][y].river and distance < knowledge_radius:
					self.known_patches.append(all_terrain[x][y])

	def clearUp(self):
		'''Deletes the household'''
		self.grain = 0
		while len(self.fields_owned) > 0:
			self.fields_owned[0].unclaim()
			del self.fields_owned[0]

	def grainTick(self):
		'''Performs all calculations to do with reduction in grain for the year,
		based off of ethnographic data which suggests that an adult needs 160kg
		of grain per year to survive'''
		self.grain -= self.workers*160
		if self.grain < 0:
			if self.legacy_mode:
				num_not_supported = 1
			else:
				# Note that grain is negative, and thus the negative here
				# serves to ensure that workers are reduced
				num_not_supported = math.ceil(-self.grain/160)
				if num_not_supported > self.workers:
					num_not_supported = self.workers

			self.grain = 0
			self.workers -= num_not_supported
			self.settled_in.population -= num_not_supported
			self.settled_in.parent.total_population -= num_not_supported

		self.grain = self.grain * 0.9	#accounts for loss due to storage
		self.settled_in.parent.total_grain += self.grain

	def populationIncrease(self):
		'''Serves to increase the population if conditions are correct'''
		populate_chance = random.random()
		if self.settled_in.parent.total_population <= (self.settled_in.parent.projected_historical_population) and populate_chance > 0.5:
			self.workers += 1
			self.settled_in.population += 1
			self.settled_in.parent.total_population += 1

	def farm(self):
		'''Performs all farming for the household for a year, excluding any land rental which may occur'''
		self.fields_owned.sort(key = lambda x: x.harvest*self.competency - x.house_distance*x.owner.distance_cost)
		max_fields_to_work = int(self.workers//2)

		total_harvest = 0
		self.workers_worked = 0
		self.fields_harvested = 0

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
				field_harvest = field.harvest*self.competency - field.house_distance*field.owner.distance_cost - 300
				
				total_harvest += field_harvest
		self.grain += total_harvest

		'''Unclaims fields which have not been harvested'''
		i = self.fields_harvested
		if self.fallow_limit > 0:
			while i < len(self.fields_owned):
				if self.fields_owned[i].years_not_harvested > self.fallow_limit:
					self.fields_owned[i].unclaim()
					del self.fields_owned[i]
				i += 1

	def claimLand(self):
		claim_chance = random.random()
		if (claim_chance < self.ambition and self.workers > len(self.fields_owned)) or (len(self.fields_owned) <= 1 and self.workers > 0):
			best_x = None
			best_y = None
			best_fertility = -1
			for patch in self.known_patches:
				if patch.fertility > best_fertility and not patch.owned and not patch.settlement and not patch.settlement_territory:
					best_x = patch.x
					best_y = patch.y
					best_fertility = patch.fertility
			if best_fertility != -1 and self.all_terrain[best_x][best_y].claim(self):
				self.fields_owned.append(self.all_terrain[best_x][best_y])

	def rentLand(self):
		if self.legacy_mode or (not self.legacy_mode and self.fields_harvested == len(self.fields_owned)):
			self.known_patches.sort(key = lambda x: x.harvest*self.competency - (((self.x - x.x)**2 + (self.y - x.y)**2)**0.5)*self.distance_cost if not x.harvested else 0)

			total_harvest = 0
			max_fields_to_work = int((self.workers - self.workers_worked)//2)
			num_fields_rented = 0

			for i in range(max_fields_to_work):

				best_field = self.known_patches[num_fields_rented]

				harvest_chance = random.random()

				if best_field.field and best_field not in self.fields_owned and harvest_chance < (self.ambition * self.competency):
					best_field.harvested = True
					# shape
					# color
					field_harvest = best_field.harvest*self.competency - (((self.x - best_field.x)**2 + (self.y - best_field.y)**2)**0.5)*self.distance_cost

					total_harvest += field_harvest * (1 - (self.land_rental_rate/100)) - 300

					best_field.owner.grain += field_harvest * (self.land_rental_rate/100)

					num_fields_rented += 1
					self.fields_harvested += 1

			self.grain += total_harvest

	def randomRange(self, minimum, maximum):
		if maximum == minimum:
			return minimum
		return random.random()*(maximum-minimum) + minimum

	def generationalChange(self):
		'''Changes ambition and competency every 10-15 years,
		finding the possible range in which the household can change to,
		and then generating a value within this range'''
		self.generation_countdown -= 1
		if self.generation_countdown <= 0:
			self.generation_countdown = random.randrange(0,6) + 10

			self.ambition = self.randomRange(
				max(self.ambition-self.generational_variation, self.minimum_ambition),
				min(self.ambition+self.generational_variation, 1))

			self.competency = self.randomRange(
				max(self.competency-self.generational_variation, self.minimum_competency),
				min(self.competency+self.generational_variation, 1))

	def fission(self):
		if self.workers > 15 and self.grain > 3 * self.workers * 164:
			fission_chance = random.random()
			if fission_chance > self.min_fission_chance:
				grain = 1100
				workers = 5

				new_household = Household(self.settled_in, grain, workers, self.minimum_ambition, self.minimum_competency, self.min_fission_chance, self.knowledge_radius, self.distance_cost, self.land_rental_rate, self.fallow_limit, self.x, self.y, self.all_terrain, self.x_size, self.y_size, self.generational_variation, self.legacy_mode)

				self.settled_in.households.append(new_household)
				self.settled_in.parent.all_households.append(new_household)

				self.workers -= 5
				self.grain -= 1100

