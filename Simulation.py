from Settlement import Settlement
from Terrain import Terrain
from Household import Household
import random
import numpy as np

class Simulation:
	x_size = 30
	y_size = 30

	def __init__(self, model_time_span, starting_settlements, starting_households, starting_household_size, starting_grain, min_ambition, min_competency, 
						generational_variation, knowledge_radius, distance_cost, fallow_limit, pop_growth_rate, min_fission_chance, land_rental_rate, 
						 manual_seed_enabled,fission_enabled, rent_enabled, legacy_mode, seed = ''):
		self.years_passed = 0
		self.legacy_mode = legacy_mode
		self.flood_level = 0
		self.total_population = 0
		self.projected_historical_population = 0
		self.time_span = model_time_span
		self.done = False
		self.seed = seed
		if manual_seed_enabled:
			random.seed(seed)
		self.all_settlements = []

		#values reset
		self.total_grain = starting_settlements*starting_households*starting_grain		
		self.min_ambition = min_ambition
		self.min_competency = min_competency

		self.generational_variation = generational_variation
		self.knowledge_radius = knowledge_radius
		self.distance_cost = distance_cost
		self.fallow_limit = fallow_limit
		self.pop_growth_rate = pop_growth_rate
		self.min_fission_chance = min_fission_chance
		self.land_rental_rate = land_rental_rate
		self.settlements = []
		self.all_households = []
		self.terrain = []

		self.fission_enabled = fission_enabled
		self.rent_enabled = rent_enabled
		self.manual_seed_enabled = manual_seed_enabled

		self.starting_population = starting_settlements * starting_households * starting_household_size
		self.total_population = self.starting_population

		#initalise terrain
		for x in range(self.x_size):
			column = []
			for y in range(self.y_size):
				column.append(Terrain(x,y))
			self.terrain.append(column)

		for y in range(self.y_size):
			self.terrain[0][y].river = True

		self.setupSettlements(starting_settlements)
		self.setupHouseholds(starting_households, starting_household_size, starting_grain, min_ambition, min_competency, min_fission_chance, int(knowledge_radius), distance_cost, land_rental_rate, fallow_limit, legacy_mode)

	def setupSettlements(self, starting_settlements):
		count = 0
		Settlement.parent = self
		while count < starting_settlements:
			x_coord = random.randint(0, self.x_size-1)
			y_coord = random.randint(0, self.y_size-1)
			terrain_patch = self.terrain[x_coord][y_coord] 
			if not terrain_patch.settlement and not terrain_patch.river:
				settlement = Settlement(terrain_patch, x_coord, y_coord)
				self.settlements.append(settlement)
				self.all_settlements.append(settlement)

				for x in range(x_coord-1, x_coord+2):
					for y in range(y_coord-1, y_coord+2):
						is_valid = True

						if x < 0 or x >= self.x_size:
							is_valid = False

						if y < 0 or y >= self.y_size:
							is_valid = False

						if is_valid:
							self.terrain[x][y].settlement_territory = True 

				count += 1
		

	def setupHouseholds(self, starting_households, starting_household_size, starting_grain, min_ambition, min_competency, min_fission_chance, knowledge_radius, distance_cost, land_rental_rate, fallow_limit, legacy_mode):
		for settlement in self.settlements:
			for i in range(int(starting_households)):
				new_household = Household(settlement, starting_grain, starting_household_size, min_ambition, min_competency, min_fission_chance, knowledge_radius, distance_cost, land_rental_rate, fallow_limit, settlement.x, settlement.y, self.terrain, self.x_size, self.y_size, self.generational_variation, legacy_mode)

				settlement.households.append(new_household)
				self.all_households.append(new_household)


	def run(self):
		while self.years_passed < self.time_span:
			self.tick()
			self.years_passed += 1 

	def tick(self):
		'''Performs the simulation for a single year'''
		self.years_passed += 1
		random.shuffle(self.settlements)

		self.total_grain = 0
		self.flood()
		for settlement in self.settlements:
			settlement.tick()
		
		self.projected_historical_population = self.starting_population * (1.001) ** self.years_passed

		i = 0
		while(i < len(self.settlements)):
			if len(self.settlements[i].households) == 0:
				self.settlements[i].terrain.settlement = False
				self.settlements[i].terrain.was_settlement = True
				self.settlements[i].terrain.settlement_territory = True
				del self.settlements[i]
			else:
				i += 1

		if self.rent_enabled:
			self.rentLand()

		for settlement in self.settlements:
			settlement.tock()

		if self.years_passed > self.time_span or len(self.settlements) == 0:
			self.done = True

	def flood(self):
		'''Sets the fertility and harvest levels for all terrain, based off of the flood levels for the year and the distance of the fields from the nile'''
		mu= random.randint(0,10) + 5
		sigma= random.randint(0, 5) + 5
		alpha= (2 * sigma**2)
		beta= 1 / (sigma * np.sqrt(2 * np.pi)) 

		for x in range(self.x_size):		## TO DO: Test speed increase of numpy vs only doing needed calculations
			for y in range(self.y_size):
				self.terrain[x][y].setFertility(beta, alpha, mu)


	def rentLand(self):
		self.all_households.sort(key=lambda x: x.ambition, reverse=True)
		for household in self.all_households:
			household.rentLand()
	

					