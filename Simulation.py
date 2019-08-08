import Settlement
import Terrain
import random

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

	x_size = 300
	y_size = 300

	settlements = []
	terrain = []

	def __init__():
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
		for x in range(x_size):
			column = []
			for y in range(y_size):
				column.append(Terrain(x,y))
			terrain.append(column)

		for y in range(y_size):
			terrain[0][y].isRiver()

		setupSettlements()

	def setupSettlements():
		pass

	def run():
		c = 0
		while c < time_span:
			tick()
			c += 1 

	def tick():
		flood()
		tickSettlements()
		populationShift()
		
		tick()

	def flood():
		mu= random.randint(0,10) + 5
		sigma= random.randint(0, 5) + 5
		alpha= (2 * sigma**2)
		beta= 1 / (sigma * sqrt(2 * pi)) 

		for x in range(x_size):		## TO DO: Test speed increase of numpy vs only doing needed calculations
			for y in range(y_size):
				terrain[x][y].setFertility(beta, alpha, mu)

	def tickSettlements():
		for settlement in settlements:
			settlement.tick()
				#household fission
		#for settlement in settlements:
			#recolor
			#get plot values

	def populationShift():
		pass