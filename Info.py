from PIL import Image, ImageTk
from Animations import Animations
from Constants import *

class Info:
	def __init__(self,plt,canvas,graph1,graph2):
		#Initialise all values to their defaults
		self.clicked_once = False
		self.paused = True
		self.ending = False
		self.graphs_data = []
		self.pointers = [6,7] #what does each graph point to 
		self.changed = [False,False]
		self.pause_play_text = "Play   "
		self.stepping = False
		self.graphs_data = [
							[ [], [[]] ],				[ [], [[]] ],				[ [], [[],[]] ],	
							[[], [[]] ],				[ [], [[]] ],
							[ [], [[],[],[]] ],
							[[],[]],					[[], [[],[],[]] ],
							[[], [[],[],[]] ],			[[],[[],[],[],[],[]]],
							[[],[[],[],[],[],[]]]
							]
		self.seed = ""
		self.tw = None
		
		self.animationEvery = 1
		self.count_since_last_graph_draw = 0
		self.force_draw_every = 10

		#Load all of the images of barley into a permananent storage position so that they may later be resized
		self.barley_images_permanent = [None,None,None]
		self.barley_images_permanent[PINK] = Image.open("images/pink_background_barley.png")
		self.barley_images_permanent[BLUE] = Image.open("images/blue_background_barley.png")
		self.barley_images_permanent[YELLOW] = Image.open("images/yellow_background_barley.png")

		#Load all of the images of houses into a permananent storage position so that they may later be resized
		self.house_images_permanent = [None,None,None]
		self.house_images_permanent[PINK] = Image.open("images/pink_background_house.png")
		self.house_images_permanent[BLUE] = Image.open("images/blue_background_house.png")
		self.house_images_permanent[YELLOW] = Image.open("images/yellow_background_house.png")	

		#Create the animations object to do handle the animations of the graphs and the grid
		self.animate = Animations(plt,canvas,self,graph1,graph2)

	def resizeImage(self,img,basewidth):
		#Takes an image and returns an image with the width resized to the parameter basewidth while maintaining the aspect ratio
		wpercent = (basewidth/float(img.size[0]))
		hsize = int((float(img.size[1])*float(wpercent)))
		img = img.resize((basewidth,hsize), Image.ANTIALIAS)
		return ImageTk.PhotoImage(img)

	def greeness(self,value):
		#Returns a shade of green based on the given value
		de=("%02x"%0)
		re=("%02x"%value)
		we=("%02x"%0)
		ge="#"
		return ge+de+re+we

	def drawGridSimulation(self):
		#Acts as an interface to the drawGridSimulation() method of the animation object
		self.animate.drawGridSimulation()

	def plotData(self):
		#Acts as an interface to the plotData() method of the animation object
		self.animate.plotData()

	def showGraphs(self):
		#Acts as an interface to the showGraphs() method of the animation object
		self.animate.showGraphs()

	def updateGraphs(self):
		#Acts as an interface to the updateGraphs() method of the animation object
		self.animate.updateGraphs()

	def clearCanvas(self):
		#Acts as an interface to the clearCanvas() method of the animation object
		self.animate.clearCanvas()

	def get_x_and_y_step(self):
		return (self.animate.xstep,self.animate.ystep)