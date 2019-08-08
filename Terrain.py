import Household
import numpy as np

class Terrain:
	settlement = False
	settlement_territory = False
	field = False
	river = False
	harvested = False
	owned = False
	owner = None
	color_stack = 0,0,0
	fertility = 0
	harvest = 0
	max_yield = 2475
	nile_distance = 0
	house_distance = 0
	years_not_harvested = 0
	x = -1
	y = -1

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def isRiver(self):
		river = True

	def setFertility(self, beta, alpha, mu):
		harvested = False
		years_not_harvested += 1
		fertility = 17*(beta*(np.exp((mu - distance)**2 / alpha)))
		if owner != None:
			harvest = fertility*max_yield*owner.competency - house_distance*owner.distance_cost

	def claim(self, claimant):
		if (not settlement) and (not river) and (not owned) and (not settlement_territory):
			owned = True
			field = True
			harvested = False

			owner = claimant
			years_not_harvested = 0

			house_distance = 

			return True
		else:
			return False

