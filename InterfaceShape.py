from tkinter import *
import time
import matplotlib.pyplot as plt
import numpy
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg as NavigationToolbar2Tk
from Simulation import Simulation

############################################################################
#Colors
bg_slider_color = '#82bcb7'
trough_color = '#415e5b'
slider_knob_color = '#c86767'
top_panel_color = '#f0f0f0'
button_color = '#bcbce6'
general_background = '#ffffff'

#Parameters:
############################################################################
runRate = 30 			#frames per second it computes at
#animationEvery = 1 	#number of frames between animation updates
#graphEvery = 30 		#number of frames between graph updates

w1 = 2 	#slider frame width
w2 = 6 	#animation frame + graphs frame width
w3 = 8	#graphs2 frame width
h1 = 1 	#top frame height
h2 = 6	#animation frame height
h3 = 2  #graphs 1 frame height
		#graphs 2 frame height is h2 + h3
s = 90  #how many pixels is the side of one cell worth

padx = 10
pady = 5
sfHeight = 70 #the heights of the side slider blocks
sliHeight = sfHeight - 2*pady #slider heights
sliWidth = w1*s-2*padx
graphW = 75

#Calculations
#############################################################################
sleeptime = 1/(runRate*1.0)

#Functions:
############################################################################
def random_color():
	de=("%02x"%0)
	re=("%02x"%random.randint(100,255))
	we=("%02x"%0)
	ge="#"
	return ge+de+re+we

def greeness(value):
	de=("%02x"%0)
	re=("%02x"%value)
	we=("%02x"%0)
	ge="#"
	return ge+de+re+we

def plotData(xpos):
	plt.figure(0)
	plt.plot(xpos,random.uniform(-2,2),"or")
	plt.tight_layout()
	
	plt.figure(1)
	plt.plot(xpos,random.uniform(-2,2),"or")
	plt.tight_layout()


def drawGrid(canvas,rows,columns):
	width, height = canvas.winfo_width(),canvas.winfo_height()
	xstep = width/columns
	ystep = height/rows
	canvas.delete('all')
	for row in range(0,rows):
		for col in range(0,columns):
			canvas.create_rectangle(row*xstep,col*ystep,(row+1)*xstep,(col+1)*ystep,fill=random_color(),outline="")

def drawGridSimulation(canvas,simulation):
	width, height = canvas.winfo_width(),canvas.winfo_height()
	overallterrain = simulation.terrain

	rows,columns = len(overallterrain)-1,len(overallterrain[0])-1
	xstep = width/columns
	ystep = height/rows
	canvas.delete('all')
	
	for row in range(0,rows):
		for col in range(0,columns):
			block = overallterrain[row][col]
			fertility = block.fertility/2
			if block.river:
				color = 'blue'
			elif block.settlement:
				color = 'red'
			else:
				color = greeness(int(100+fertility*155))

			
			#print("Fertility was: " + str(overallterrain[columns][rows].fertility))
			canvas.create_rectangle(row*xstep,col*ystep,(row+1)*xstep,(col+1)*ystep,fill=color,outline="")

	#settlements = simulation.settlements
	#for settlement in settlements:
	#		terrain = settlement.terrain

	#	for block in terrain:
	#		row = block.x
	#		col = block.y
	#		canvas.create_rectangle(row*xstep,col*ystep,(row+1)*xstep,(col+1)*ystep,fill='red',outline="")

	for row in range(0,rows):
		for col in range(0,columns):
			parent = overallterrain[row][col].owner
			if parent != None:
				target = parent.location
				canvas.create_line((row+0.5)*xstep,(col+0.5)*ystep,(target.x+0.5)*xstep,(target.y+0.5)*ystep)


#GUI setup frames:
############################################################################
tk = Tk()
tk.configure(background=general_background)

topframe = Frame(tk,bg=top_panel_color,width=(w1+w2+w3)*s,height=h1*s,relief='raised')
topframe.grid(row=0,column=0,columnspan=7,rowspan=1,sticky=N+S+E+W)
topframe.grid_propagate(False)

sliderframe = Frame(tk,bg=general_background,width=w1*s,height=(h2+h3)*s)
sliderframe.grid(row=1,column=0,columnspan=1,rowspan=6,sticky=N+S+E+W)
sliderframe.grid_rowconfigure(0,weight=1)
sliderframe.grid_columnconfigure(0,weight=1)

animationframe = Frame(tk,bg=general_background,width=w2*s,height=h2*s)
animationframe.grid(row=1,column=1,columnspan=3,rowspan=3,sticky=N+S+E+W,padx=padx,pady=pady)
animationframe.grid_propagate(False)

bottomframe = Frame(tk,bg=general_background,width=w2*s,height=h3*s)
bottomframe.grid(row=4,column=1,columnspan=3,rowspan=3,sticky=N+S+E+W)
bottomframe.grid_propagate(False)

graphsframe = Frame(tk,bg=general_background,width=w3*s,height=(h2+h3)*s)
graphsframe.grid(row=1,column=4,columnspan=3,rowspan=6,sticky=N+S+E+W)
graphsframe.grid_propagate(False)

tk.grid_columnconfigure(4,weight=1,minsize=w2*s)
tk.grid_rowconfigure(4,weight=1,minsize=h3*s)
tk.grid_columnconfigure(1,weight=1,minsize=w2*s)
tk.grid_rowconfigure(1,weight=1,minsize=h2*s)
tk.grid_columnconfigure(4,weight=1,minsize=w2*s)
tk.grid_rowconfigure(4,weight=1,minsize=h3*s)
tk.grid_columnconfigure(0,weight=1,minsize=w1*s)
tk.grid_rowconfigure(0,weight=1,minsize=h1*s)	

tk.minsize((w1+w2+w3)*s,(h1+h2+h3)*s)

canvas = Canvas(animationframe,width=w2*s,height=h2*s,bg=general_background)
canvas.grid(row=0,column=0)

#Top panel
############################################################################
button_reset = Button(topframe,text='Reset',bg=button_color)
button_reset.grid(row=0,column=0,padx=padx,pady=pady)

button_go = Button(topframe,text='Go',bg=button_color)
button_go.grid(row=0,column=1,padx=padx,pady=pady)

button_pause = Button(topframe,text='Pause',bg=button_color)
button_pause.grid(row=0,column=2,padx=padx,pady=pady)

speed_scale = Scale(topframe,from_=1,to=100,resolution=1,orient=HORIZONTAL,sliderrelief="raised",length=(w2*s),label="Simulation speed (fps)",bg=top_panel_color,troughcolor=trough_color)
speed_scale.grid(row=0,column=3,padx=padx*5)

#Slider panel
############################################################################

slider_canvas = Canvas(sliderframe,bg='white smoke',width=w1*s,height=(h2+h3)*s)
slider_canvas.grid(row=0,column=0,columnspan=1,rowspan=1,sticky=N+S+E+W)

yscrollbar = Scrollbar(sliderframe,command=slider_canvas.yview)
yscrollbar.grid(row=0,column=1,sticky=N+S+E+W)

frame_in_canvas = Frame(slider_canvas,bg='white smoke',width = w1*s,height=(h2+h3)*s)
frame_in_canvas.grid(row=0,column=0,columnspan=1,rowspan=1,sticky=N+S+E+W)

slider_info = [("model-time-span",100,500,50),
				("starting-settlements",5,20,1),
				("starting-households",1,10,1),
				("starting-household-size",1,10,1),
				("starting-grain",100,8000,100),
				("min-ambition",0,1,0.1),
				("min-competency",0,1,0.1),
				("generational-variation",0,1,0.1),
				("knowledge-radius",5,40,5),
				("distance-cost",1,15,1),
				("fallow-limit",0,10,1),
				("pop-growth-rate",0,0.5,0.01),
				("min-fission-chance",0.5,0.9,0.1),
				("land-rental-rate",30,60,5)]

slider_frames = []
sliders = []
currentRow = 0
for name in slider_info:
	slider_frames.append(Frame(frame_in_canvas,bg='white smoke',bd=2,width=w1*s-2*padx,height=sfHeight+pady))
	slider_frames[-1].grid(row=currentRow,column=0,padx=padx)
	slider_frames[-1].grid_propagate(False)
	sliders.append(Scale(slider_frames[-1],from_=slider_info[currentRow][1],
		to=slider_info[currentRow][2],resolution=slider_info[currentRow][3],
		orient=HORIZONTAL,sliderrelief="raised",length=sliWidth,
		label=slider_info[currentRow][0],bg=bg_slider_color,troughcolor=trough_color))
	sliders[-1].grid(row=0,column=0,padx=1)
	currentRow += 1

slider_canvas.create_window(0, 0, anchor='nw', window=frame_in_canvas)
slider_canvas.update_idletasks()
slider_canvas.configure(scrollregion=(0,0,w1*s,(sfHeight + pady)*len(slider_info)), 
                 yscrollcommand=yscrollbar.set)


#Graph panel
#############################################################################
options = ["One","Two","Three","Four"]


###############
#Graph 1
graph1frame = Frame(graphsframe,bg=general_background,width=w3*s)
graph1frame.grid(row=0,column=0,columnspan=1,rowspan=1,sticky=N+S+E+W)

plt.figure(num=0,figsize=(2*4,1*4),dpi=graphW)
graph1 = FigureCanvasTkAgg(plt.figure(0),graph1frame)
graph1.get_tk_widget().grid(row=0,column=0,columnspan=2,rowspan=1,padx=padx,pady=pady)
graph1.get_tk_widget().configure(background = 'BLACK', borderwidth = 1, relief = SUNKEN)

graph1var = StringVar(graph1frame)
graph1menu = OptionMenu(graph1frame,graph1var,*options)
graph1menu.config(width=int(graphW/4))
graph1menu.grid(row=1,column=1,columnspan=1,rowspan=1,padx=padx,pady=pady)

toolbarframe1 = Frame(graph1frame)
toolbarframe1.grid(row=1,column=0)

toolbar1 = NavigationToolbar2Tk(graph1, toolbarframe1)
toolbar1.update()
toolbarframe1.grid_propagate(False)

################
#Graph 2
graph2frame = Frame(graphsframe,bg=general_background,width=w3*s)
graph2frame.grid(row=1,column=0,columnspan=1,rowspan=1,sticky=N+S+E+W)

plt.figure(num=1,figsize=(2*4,1*4),dpi=graphW)
graph2 = FigureCanvasTkAgg(plt.figure(1),graph2frame)
graph2.get_tk_widget().grid(row=0,column=0,columnspan=2,rowspan=1,padx=padx,pady=pady)
graph2.get_tk_widget().configure(background = 'BLACK', borderwidth = 1, relief = SUNKEN)

graph2var = StringVar(graph2frame)
graph2menu = OptionMenu(graph2frame,graph2var,*options)
graph2menu.config(width=int(graphW/4))
graph2menu.grid(row=1,column=1,columnspan=1,rowspan=1,padx=padx,pady=pady)

toolbarframe2 = Frame(graph2frame,width=w3,bg='red')
toolbarframe2.grid(row=1,column=0)


toolbar2 = NavigationToolbar2Tk(graph2, toolbarframe2)
toolbar2.update()
toolbarframe2.grid_propagate(False)


#Initialisation
#############################################################################
animationcount = 0
xpos = 0
graphcount = 0
#

#slider_values = [x.get()*1.0 for x in sliders]
#slider_values = slider_values[0:7]
#sim = Simulation(*slider_values)
#paused = False


#Button functions
#############################################################################
def button_pause():
	pass

def button_reset():
	pass

def button_go():
	pass

sim = Simulation(10,0,0,0,0,0,0)
#info = Info()

#Mainloop:
#############################################################################
while 1:
	animationEvery = 1/(1.0*speed_scale.get())*runRate
	graphEvery = 30 * animationEvery

	animationcount += 1
	if (animationcount >= animationEvery):
		animationcount = 0
		sim.tick()
		drawGridSimulation(canvas,sim)

	#graphcount += 1
	#if (graphcount >= graphEvery/2):
	#	pass
	#if (graphcount >= graphEvery):
		#show the plots
		#plotData(xpos)
		#graph1.show()
		#graph2.show()
	#	graphcount=0

	xpos += 1

	tk.update_idletasks()
	tk.update()
	time.sleep(sleeptime)