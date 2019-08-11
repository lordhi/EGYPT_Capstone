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

	def setRiver(self):
		self.river = True

	def setSettlement(self):
		self.settlement = True
		self.settlement_territory = True

	def setSettlementTerritory(self):
		self.settlement_territory = True

	def setFertility(self, beta, alpha, mu):
		self.harvested = False
		self.years_not_harvested += 1
		self.fertility = 17*(beta*(np.exp(-(mu - self.nile_distance)**2 / alpha)))
		if self.owner != None:
			self.harvest = self.fertility*self.max_yield*self.owner.competency - self.house_distance*self.owner.distance_cost

	def claim(self, claimant):
		if (not self.settlement) and (not self.river) and (not self.owned) and (not self.settlement_territory):
			self.owned = True
			self.field = True
			self.harvested = False

			self.owner = claimant
			self.years_not_harvested = 0

			self.house_distance = 0

			return True
		else:
			return False

