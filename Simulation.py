from Settlement import Settlement
from Terrain import Terrain
from Household import Household
import random
import numpy as np

class Simulation:
	elevation_dataset = []
	flood_level = 0
	total_grain = 0
	total_households = 0
	total_population = 0
	projected_historical_population = 0
	lorenz_points = 0
	gini_index_reserve = 0
	house_colours, claim_x, claim_y = 0,0,0
	average_ambition = 0
	average_competency = 0
	time_span = 0

	x_size = 30
	y_size = 30

	settlements = []
	terrain = []

	def __init__(self, starting_settlements, starting_households, starting_household_size, starting_grain, min_ambition, min_competency, distance_cost):
		elevation_dataset = []
		flood_level = 0
		total_households = 0
		total_population = 0
		projected_historical_population = 0
		lorenz_points = 0
		gini_index_reserve = 0
		house_colours, claim_x, claim_y = 0,0,0

		#values reset
		total_grain = 0
		average_ambition = 0
		average_competency = 0

		#initalise terrain
		for x in range(self.x_size):
			column = []
			for y in range(self.y_size):
				column.append(Terrain(x,y))
			self.terrain.append(column)

		for y in range(self.y_size):
			self.terrain[0][y].setRiver()

		self.setupSettlements(starting_settlements)
		self.setupHouseholds(starting_households, starting_household_size, starting_grain, min_ambition, min_competency, distance_cost)
		self.establish_population(starting_settlements, starting_households, starting_household_size)

	def setupSettlements(self, starting_settlements):
		count = 0
		while count < starting_settlements:
			x_coord = random.randint(0, self.x_size-1)
			y_coord = random.randint(0, self.y_size-1)
			terrain_patch = self.terrain[x_coord][y_coord] 
			if not terrain_patch.settlement and not terrain_patch.river:
				self.settlements.append(Settlement(terrain_patch))
				
				for x in range(x_coord-1, x_coord+2):
					for y in range(y_coord-1, y_coord+2):
						is_valid = True

						if x < 0 or x >= 300:
							is_valid = False

						if y < 0 or y >= 300:
							is_valid = False

						if is_valid:
							self.terrain[neighbour_x][neighbour_y].setSettlementTerritory() 

				count += 1
		pass

	def setupHouseholds(self, starting_households, starting_household_size, starting_grain, min_ambition, min_competency, distance_cost):
		for settlement in self.settlements:
			for i in range(starting_households):
				grain = starting_grain
				workers = starting_household_size
				ambition = min_ambition + (random.random()*(1 - min_ambition))
				competency = min_competency + (random.random()*(1 - min_competency))
				generation_countdown = random.randint(0, 5) + 10
				new_household = Household(grain, workers, ambition, competency, generation_countdown, distance_cost, settlement.getX(), settlement.getY(), self.terrain)
				settlement.households.append(new_household)
				new_household.settled_in = settlement

			settlement.population += starting_households*starting_household_size

	def establish_population(self, starting_settlements, starting_households, starting_household_size):
		self.total_population = starting_settlements * starting_households * starting_household_size

	def run(self):
		c = 0
		while c < self.time_span:
			self.tick()
			c += 1 

	def tick(self):
		self.flood()
		self.tickSettlements()
		self.populationShift()

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
				#household fission
		#for settlement in settlements:
			#recolor
			#get plot values

	def populationShift(self):
		pass