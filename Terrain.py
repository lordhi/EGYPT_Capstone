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
		self.nile_distance = x

		self.settlement = False
		self.settlement_territory = False
		self.field = False
		self.river = False
		self.harvested = False
		self.owned = False
		self.owner = None
		self.color_stack = 0,0,0
		self.fertility = 0
		self.harvest = 0
		self.max_yield = 2475
		self.house_distance = 0
		self.years_not_harvested = 0

	def setFertility(self, beta, alpha, mu):
		self.harvested = False
		self.years_not_harvested += 1
		self.fertility = 17*(beta*(np.exp(-(mu - self.nile_distance)**2 / alpha)))
		if self.owned:
			self.harvest = self.fertility*self.max_yield

	def claim(self, claimant):
		if (not self.settlement) and (not self.river) and (not self.owned) and (not self.settlement_territory):
			self.owned = True
			self.field = True
			self.harvested = False

			self.owner = claimant
			self.years_not_harvested = 0

			self.house_distance = ((self.x - claimant.x)**2 + (self.y - claimant.y)**2)**0.5

			return True
		else:
			return False

	def unclaim(self):
		self.owned = False
		self.owner = None
		self.field = False
		self.house_distance = 0