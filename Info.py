from PIL import Image, ImageTk
from Animations import Animations
from Constants import *

class Info:
	# sim = None
	# paused = None
	# animationcount = None
	# xpos = None
	# graphcount = None
	# clicked_once = None
	# ending = None
	# house_images = None
	# barley_images = None
	# seed = None
	# graphs_data = None
	# changed = None
	# pointers = None
	# chosen_households_one = None
	# chosen_households_two = None
	# pause_play_text = None
	# stepping = None
	# animationEvery = None
	# graphEvery = None
	# colors = None
	# count_since_last_graph_draw = None
	# force_draw_every = None

	def __init__(self,plt,canvas,graph1,graph2):
		self.clicked_once = False
		self.paused = True
		self.ending = False
		self.graphs_data = []
		self.pointers = [6,7] #what does each graph point to 
		self.changed = [False,False]
		self.pause_play_text = "Play   "
		self.stepping = False
		self.graphs_data = [
							[ [], [[]] ],		[ [], [[]] ],		[ [], [[]] ],
							[[], [[]] ],		[ [], [[]] ],
							[ [], [[],[],[]] ],
							[[],[]],			[[], [[],[],[]] ],
							[[], [[],[],[]] ],			[[],[[],[],[],[],[]]],
							[[],[[],[],[],[],[]]]
							]
		self.seed = ""
		
		self.animationEvery = 1
		self.count_since_last_graph_draw = 0
		self.force_draw_every = 10

		#Barley images
		self.barley_images = [None,None,None]
		self.barley_images[PINK] = Image.open("images/pink_background_barley.png")
		self.barley_images[BLUE] = Image.open("images/blue_background_barley.png")
		self.barley_images[YELLOW] = Image.open("images/yellow_background_barley.png")

		#House images
		self.house_images = [None,None,None]
		self.house_images[PINK] = Image.open("images/pink_background_house.png")
		self.house_images[BLUE] = Image.open("images/blue_background_house.png")
		self.house_images[YELLOW] = Image.open("images/yellow_background_house.png")

		self.animate = Animations(plt,canvas,self,graph1,graph2)

	def resizeImage(self,img,basewidth):
		wpercent = (basewidth/float(img.size[0]))
		hsize = int((float(img.size[1])*float(wpercent)))
		img = img.resize((basewidth,hsize), Image.ANTIALIAS)
		return ImageTk.PhotoImage(img)

	def greeness(self,value):
		de=("%02x"%0)
		re=("%02x"%value)
		we=("%02x"%0)
		ge="#"
		return ge+de+re+we

	# def padListWithZeros(self,l,length):
	# 	d = length-len(l)
	# 	if d > 0:
	# 		l += [0]*d
	# 	return l