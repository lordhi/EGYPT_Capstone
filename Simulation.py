from Settlement import Settlement
from Terrain import Terrain
from Household import Household
import random
import numpy as np

class Simulation:
	years_passed = 0

	elevation_dataset = []
	flood_level = 0
	total_grain = 0
	total_households = 0
	total_population = 0
	projected_historical_population = 0
	lorenz_points = 0
	gini_index_reserve = 0
	house_colours = 0,0,0
	average_ambition = 0
	average_competency = 0
	min_ambition = 0
	min_competency = 0
	time_span = 0
	generational_variation = 0
	knowledge_radius = 0
	distance_cost = 0
	fallow_limit = 0
	pop_growth_rate = 0
	min_fission_chance = 0
	land_rental_rate = 0

	starting_population = 0

	fission_enabled = False
	rent_enabled = False
	manual_seed_enabled = False
	
	x_size = 30
	y_size = 30

	settlements = []
	all_households = []
	terrain = []

	def __init__(self, model_time_span, starting_settlements, starting_households, starting_household_size, starting_grain, min_ambition, min_competency, 
						generational_variation, knowledge_radius, distance_cost, fallow_limit, pop_growth_rate, min_fission_chance, land_rental_rate, 
						fission_enabled, rent_enabled, manual_seed_enabled):
		self.years_passed = 0
		
		self.elevation_dataset = []
		self.flood_level = 0
		self.total_households = 0
		self.total_population = 0
		self.projected_historical_population = 0
		self.lorenz_points = 0
		self.gini_index_reserve = 0
		self.house_colours, self.claim_x, self.claim_y = 0,0,0
		self.time_span = model_time_span
		self.done = False

		#values reset
		self.total_grain = starting_settlements*starting_households*starting_grain
		self.average_ambition = 0
		self.average_competency = 0
		
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
		self.setupHouseholds(starting_households, starting_household_size, starting_grain, min_ambition, min_competency, min_fission_chance, int(knowledge_radius), distance_cost, land_rental_rate)

	def setupSettlements(self, starting_settlements):
		count = 0
		Settlement.parent = self
		while count < starting_settlements:
			x_coord = random.randint(0, self.x_size-1)
			y_coord = random.randint(0, self.y_size-1)
			terrain_patch = self.terrain[x_coord][y_coord] 
			if not terrain_patch.settlement and not terrain_patch.river:
				settlement = Settlement(terrain_patch, x_coord, y_coord)
				terrain_patch.owner = settlement
				self.settlements.append(settlement)

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
		pass

	def setupHouseholds(self, starting_households, starting_household_size, starting_grain, min_ambition, min_competency, min_fission_chance, knowledge_radius, distance_cost, land_rental_rate):
		for settlement in self.settlements:
			for i in range(int(starting_households)):
				new_household = Household(settlement, starting_grain, starting_household_size, min_ambition, min_competency, min_fission_chance, knowledge_radius, distance_cost, land_rental_rate, settlement.x, settlement.y, self.terrain, self.x_size, self.y_size)

				settlement.households.append(new_household)
				self.all_households.append(new_household)

			settlement.population += starting_households*starting_household_size

	def run(self):
		while self.years_passed < self.time_span:
			self.tick()
			self.years_passed += 1 

	def tick(self):
		self.years_passed += 1
		random.shuffle(self.settlements)

		self.total_grain = 0
		self.flood()
		self.tickSettlements()
		self.populationShift()

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

		if self.years_passed > self.time_span:
			self.done = True

	def flood(self):
		mu= random.randint(0,10) + 5
		sigma= random.randint(0, 5) + 5
		alpha= (2 * sigma**2)
		beta= 1 / (sigma * np.sqrt(2 * np.pi)) 

		for x in range(self.x_size):		## TO DO: Test speed increase of numpy vs only doing needed calculations
			for y in range(self.y_size):
				self.terrain[x][y].setFertility(beta, alpha, mu)

	def tickSettlements(self):
		for settlement in self.settlements:
			settlement.tick()
		#for settlement in settlements:
			#recolor
			#get plot values

	def populationShift(self):
		pass


	def rentLand(self):
		for household in self.all_households.sort(key=lambda x: x.ambition, reverse=True):
			household.rentLand() # Move land_rental_rate inside household or not? (Thinking about extensibility)
	

					