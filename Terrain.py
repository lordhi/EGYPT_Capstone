
import numpy as np

class Terrain:
	__slots__ = "settlement", "was_settlement", "settlement_territory", "field", "river", "harvested", "owned", "owner", "fertility", "harvest", "max_yield", "nile_distance", "house_distance", "years_not_harvested", "x", "y"

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.nile_distance = x

		self.settlement = False
		self.was_settlement = False
		self.settlement_territory = False
		self.field = False
		self.river = False
		self.harvested = False
		self.owned = False
		self.owner = None
		self.fertility = 0
		self.harvest = 0
		self.max_yield = 2475
		self.house_distance = 0
		self.years_not_harvested = 0

	def setFertility(self, beta, alpha, mu):
		self.harvested = False
		self.years_not_harvested += 1
		self.fertility = 17*(beta*(np.exp(-(mu - self.nile_distance)**2 / alpha)))
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