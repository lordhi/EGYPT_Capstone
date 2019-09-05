from tkinter import *
import tkinter.simpledialog as simpledialog
import time
import matplotlib.pyplot as plt
import numpy
import random
import time
import threading
from CreateToolTip import CreateToolTip

try:
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk as NavigationToolbar2Tk
except:
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg as NavigationToolbar2Tk

from Simulation import Simulation
import sys

from PIL import Image, ImageTk

############################################################################
#Colors
bg_slider_color = '#82bcb7'
trough_color = '#415e5b'
slider_knob_color = '#c86767'
top_panel_color = '#f0f0f0'
button_color = '#bcbce6'
general_background = '#ffffff'
circle_border_outline = '#9d6e48'
PINK = 0
BLUE = 1
YELLOW = 2
GREY = 3

pink_hex = '#a71b6a'
blue_hex = '#294b89'
yellow_hex = '#f0f05a'
grey_hex = '#8d8d8d'

color_hexes = [pink_hex,blue_hex,yellow_hex,grey_hex] 

############################################################################
#Set up root
tk = Tk()
tk.title("Egypt simulation")
tk.configure(background=general_background)

#Imported functions
#############################################################################
def resizeImage(img,basewidth):
	wpercent = (basewidth/float(img.size[0]))
	hsize = int((float(img.size[1])*float(wpercent)))
	img = img.resize((basewidth,hsize), Image.ANTIALIAS)
	return img

#Button functions
#############################################################################
def button_step_on_click():
	info.paused = False
	info.stepping = True
	updateGraphs()
	showGraphs()
	drawGridSimulation(canvas,info)

	if (info.sim.done):
			button_run_all['state'] = 'disabled'


def button_reset_on_click():
	button_play_pause['state']='normal'
	#button_run_all['state']='normal'
	if not (info.clicked_once and not info.paused):
		button_step['state']='normal'

	slider_values = [x.get()*1.0 for x in sliders]
	check_values = [x.get() for x in check_var]
	info.sim = Simulation(*slider_values,*check_values,info.seed)

	info.animationcount = 0
	info.xpos = 0
	info.graphcount = 0

	width = canvas.winfo_width()
	columns = len(info.sim.terrain[0])
	xstep = int(width/columns - 1)

	#Barley images
	info.barley_images = [None,None,None]
	info.barley_images[PINK] = Image.open("images/pink_background_barley.png")
	info.barley_images[BLUE] = Image.open("images/blue_background_barley.png")
	info.barley_images[YELLOW] = Image.open("images/yellow_background_barley.png")

	info.barley_images = [ImageTk.PhotoImage(resizeImage(img,int(xstep*4/5.0))) for img in info.barley_images]

	#House images
	info.house_images = [None,None,None]
	info.house_images[PINK] = Image.open("images/pink_background_house.png")
	info.house_images[BLUE] = Image.open("images/blue_background_house.png")
	info.house_images[YELLOW] = Image.open("images/yellow_background_house.png")

	info.house_images = [ImageTk.PhotoImage(resizeImage(img,int(2/3.0*xstep))) for img in info.house_images]

	options = [("Total Grain","Years","Total grain"),("Total Population","Years","Population"),("Total households and settlements","",""),
		("Gini-index","Time","Gini"),("Grain Grain-equalityy","%-population","%-wealth"),
		("Households holding stated as percentage of the wealthiest households grain","Time","no of households"),
		("Settlement population","Years","Population"),("Max mean min settlement popuplation","Years","No of households"),
		("Mean min max wealth levels of households","Years","Grain"),("Household wealth households 20-24","Years","Wealth"),
		("Household wealth households 25-29","Years","Wealth")]

	info.graphs_data = [
					[ [], [[]] ],		[ [], [[]] ],		[ [], [[]] ],
					[[], [[]] ],		[ [], [[]] ],
					[ [], [[],[],[]] ],
					[[],[]],			[[], [[],[],[]] ],
					[[], [[],[],[]] ],			[[],[[],[],[],[],[]]],
					[[],[[],[],[],[],[]]]
					]

	info.graphs_data[6][1] = []
	for i in range(len(info.sim.all_settlements)):
		info.graphs_data[6][1].append([])

	info.changed = [True,True]

	info.chosen_households_one = info.sim.all_households[20:25]
	info.chosen_households_two = info.sim.all_households[25:30]

	years_label.set("")

	#info.sim.tick()
	drawGridSimulation(canvas,info)
	info.changed[0] = True
	info.changed[1] = True
	updateGraphs()
	showGraphs()

def button_run_all_on_click():
	while not info.sim.done:
		info.sim.tick()
		plotData()

	info.changed[0] = True
	info.changed[1] = True
	drawGridSimulation(canvas,info)
	updateGraphs()
	showGraphs()
	years_label.set("Years passed: " + str(info.sim.years_passed))
	button_run_all['state'] = 'disabled'




def button_play_pause_on_click():
	if (not info.clicked_once):
		button_reset_on_click()
		info.clicked_once = True
	info.paused = not info.paused
	if info.paused:
		button_run_all['state']='normal'

	if info.paused:
		info.pause_play_text.set("Play   ")
		button_run_all['state']='normal'
		button_step['state']='normal'
	else:
		info.pause_play_text.set("Pause")
		button_run_all['state']='disabled'
		button_step['state']='disabled'
		plotData()
		updateGraphs()
		showGraphs()

	if (info.sim.done):
		button_run_all['state'] = 'disabled'



def popup_window():
	if check_var[0].get():
		info.seed = simpledialog.askstring("Enter a seed:","e.g. 12341234")

def graphMenuOneClick(selection):
	names = [x[0] for x in options]
	info.pointers[0] = names.index(selection)
	info.changed[0] = True
	updateGraphs()
	showGraphs()

def graphMenuTwoClick(selection):
	names = [x[0] for x in options]
	info.pointers[1] = names.index(selection)
	info.changed[1] = True
	updateGraphs()
	showGraphs()

#Parameters:
############################################################################

w1 = 2 	#slider frame width
w2 = 6 	#animation frame + graphs frame width
w3 = 8	#graphs2 frame width
h1 = 0.6 	#top frame height
h2 = 6	#animation frame height
h3 = 2  #graphs 1 frame height
		#graphs 2 frame height is h2 + h3

s = 90 / 864 * tk.winfo_screenheight() #how many pixels is the side of one cell worth
 
padx = int(s/9)
pady = int(s/18)
sfHeight = s*0.95 #the heights of the side slider blocks
sliHeight = sfHeight - 2*pady #slider heights
sliWidth = w1*s-2*padx-5
chkHeight = s/2 #the heights of the check boxes
graphW = 0.8*s

#Functions:
############################################################################
def greeness(value):
	de=("%02x"%0)
	re=("%02x"%value)
	we=("%02x"%0)
	ge="#"
	return ge+de+re+we

def padListWithZeros(l,length):
	d = length-len(l)
	if d > 0:
		l += [0]*d
	return l

def plotData():
	total_grain = info.sim.total_grain
	total_households = len(info.sim.all_households)
	total_population = info.sim.total_population
	total_ambition = max([x.ambition for x in info.sim.all_households])
	total_competency = max([x.competency for x in info.sim.all_households])
	start_population = info.sim.starting_population
	
	average_ambition = total_ambition/total_households
	average_competency = total_competency/total_households

	sorted_grain = sorted([x.grain for x in info.sim.all_households])
	wealth_so_far = 0
	index = 0
	gini_index_reserve = 0

	lorenz_points = []


	for i in range(total_households):
		wealth_so_far += sorted_grain[0]
		sorted_grain = sorted_grain[1:]

		if total_grain > 0:
			lorenz_points += [(wealth_so_far/total_grain)*100]
			index += 1
			if (total_households>0):
				gini_index_reserve += (index/total_households) - (wealth_so_far/total_grain)


	#Total Grain
	info.graphs_data[0][0].append(info.sim.years_passed)
	info.graphs_data[0][1][0].append(info.sim.total_grain)

	#Total Population
	info.graphs_data[1][0].append(info.sim.years_passed)
	info.graphs_data[1][1][0].append(info.sim.total_population)

	#Total households and settlements
	info.graphs_data[2][0].append(info.sim.years_passed)
	info.graphs_data[2][1][0].append(len(info.sim.settlements) + len(info.sim.all_households))

	#Gini-index
	info.graphs_data[3][0].append(info.sim.years_passed)
	info.graphs_data[3][1][0].append(gini_index_reserve/total_households/2)

	#Grain-equality
	x = range(len(lorenz_points))
	info.graphs_data[4][0]= x
	info.graphs_data[4][1][0]=lorenz_points

	 #Households holding
	t_pink = 0
	t_blue = 0
	t_yellow = 0
	info.graphs_data[5][0] = info.graphs_data[3][0]
	for settlement in info.sim.settlements:
	 	for household in settlement.households:
	 		if household.color == PINK:
	 			t_pink += 1
	 		if household.color == BLUE:
	 			t_blue += 1
	 		if household.color == YELLOW:
	 			t_yellow += 1

	info.graphs_data[5][1][0].append(t_pink)
	info.graphs_data[5][1][1].append(t_blue)
	info.graphs_data[5][1][2].append(t_yellow)
	 

	#Settlements population
	info.graphs_data[6][0].append(info.sim.years_passed)
	for i in range(len(info.sim.all_settlements)):
		info.graphs_data[6][1][i].append(info.sim.all_settlements[i].population)
	

	#Max mean min settlement popuplation
	populations = [x.population for x in info.sim.settlements]
	info.graphs_data[7][0].append(info.sim.years_passed)
	info.graphs_data[7][1][0].append(max(populations))
	info.graphs_data[7][1][1].append(sum(populations)/len(populations))
	info.graphs_data[7][1][2].append(min(populations))
	
	#Mean min max wealth levels of households
	grains = [x.grain for x in info.sim.all_households]
	info.graphs_data[8][0].append(info.sim.years_passed)
	info.graphs_data[8][1][0].append(max(grains))
	info.graphs_data[8][1][1].append(sum(grains)/len(grains))
	info.graphs_data[8][1][2].append(min(grains))

	#Household wealth households 20-24
	chosen_households = info.chosen_households_one

	info.graphs_data[9][0].append(info.sim.years_passed)
	length=len(chosen_households)
	for household,  i   in zip(chosen_households,  range(length)):
		info.graphs_data[9][1][i].append(household.grain)
	for j in range(length,5):
		info.graphs_data[9][1][i].append(0)

	#Household wealth households 25-29
	chosen_households = info.chosen_households_two

	info.graphs_data[10][0].append(info.sim.years_passed)
	length=len(chosen_households)
	for household,  i in zip(chosen_households,  range(length)):
		info.graphs_data[10][1][i].append(household.grain)
	for j in range(length,5):
		info.graphs_data[10][1][i].append(0)

def updateGraphs():
	for fig in [0,1]:
		pointer = info.pointers[fig]
		data = info.graphs_data[pointer]
		xdata = data[0]
		ydata = data[1]
		redraw_graph = info.count_since_last_graph_draw >= info.force_draw_every

		plt.figure(fig)
		if (pointer == 4):
			plt.clf()
			if (len(xdata)>1):
				plt.plot(xdata,ydata[0],label='Wealth',color=info.colors[0])
				plt.plot([xdata[0],xdata[-1]],[ydata[0][0],ydata[0][-1]],label='Equality',color=info.colors[1])
				plt.legend()

		elif (info.changed[fig] or redraw_graph):
			if redraw_graph:
				info.count_since_last_graph_draw = 0
			info.changed[fig] = False
			plt.clf()

			if (pointer == 5):
				line, = plt.plot(xdata,ydata[0],label='>66%')
				line.set_color(color_hexes[PINK])
				line, = plt.plot(xdata,ydata[1],label='33-66%')
				line.set_color(color_hexes[BLUE])
				line, = plt.plot(xdata,ydata[2],label='<33%')
				line.set_color(color_hexes[YELLOW])
				plt.legend()

			elif (pointer == 7 or pointer == 8):
				plt.plot(xdata,ydata[0],label='max',color=info.colors[0])
				plt.plot(xdata,ydata[1],label='avg',color=info.colors[1])
				plt.plot(xdata,ydata[2],label='min',color=info.colors[2]) 
				plt.legend()

			else: #pointer = 0,1,2,3,6,9,10
				#print(len(ydata))
				for i in range(len(ydata)):
				#for i in range(len(info.sim.all_settlements)):
					line = ydata[i]
					color = info.colors[i]
					plt.plot(xdata,line,color=color)
		
			plt.title(options[pointer][0])
			plt.xlabel(options[pointer][1])
			plt.ylabel(options[pointer][2])
			plt.tight_layout()

		elif (len(xdata)>1):	
			g = info.graphEvery

			if (pointer == 5):
				line, = plt.plot(xdata[-(g+2):-1],ydata[0][-(g+2):-1])
				line.set_color(color_hexes[PINK])
				line, = plt.plot(xdata[-(g+2):-1],ydata[1][-(g+2):-1])
				line.set_color(color_hexes[BLUE])
				line, = plt.plot(xdata[-(g+2):-1],ydata[2][-(g+2):-1])
				line.set_color(color_hexes[YELLOW])
				plt.legend()

			elif (pointer == 7 or pointer == 8):
				plt.plot(xdata[-(g+2):-1],ydata[0][-(g+2):-1],color=info.colors[0])
				plt.plot(xdata[-(g+2):-1],ydata[1][-(g+2):-1],color=info.colors[1])
				plt.plot(xdata[-(g+2):-1],ydata[2][-(g+2):-1],color=info.colors[2]) 
				plt.legend()

			else: #pointer = 0,1,2,3,6,9,10
				for i in range(len(ydata)):
				#for i in range(len(info.sim.all_settlements)):
					line = ydata[i]
					color = info.colors[i]
					plt.plot(xdata[-(g+2):-1],line[-(g+2):-1],color=color)



def showGraphs():
	current_milli_time = lambda: int(round(time.time() * 1000))

	info.count_since_last_graph_draw += 1

	time1 = current_milli_time()
	graph1.draw()
	graph2.draw()
	time2 = current_milli_time()


def drawCircle(canvas,x,y,r,color=False):
	if (not color):
		canvas.create_oval(x-r,y-r,x+r,y+r,fill='black',outline=circle_border_outline,width=r/6)
	else:
		canvas.create_oval(x-r,y-r,x+r,y+r,fill=color,width=0)

def getColor(max_grain,grain):
	if (grain > 2/3*max_grain):
		return PINK
	elif (grain > 1/3*max_grain):
		return BLUE
	else:
		return YELLOW

def drawGridSimulation(canvas,info):
	simulation = info.sim
	width, height = canvas.winfo_width(),canvas.winfo_height()
	overallterrain = simulation.terrain

	rows,columns = len(overallterrain),len(overallterrain[0])
	xstep = width/columns - 1
	ystep = height/rows - 1
	canvas.delete('all')
	if (len(info.sim.all_households)>0):
		overall_biggest_grain = max([x.grain for x in info.sim.all_households])
	else:
		overall_biggest_grain = 0

	for row in range(0,rows):
		for col in range(0,columns):
			block = overallterrain[row][col]		
			fertility = block.fertility/2 #still need to fix this!
			if block.river:
				color = 'blue'
			else:
				color = greeness(int(245-fertility*205))
			canvas.create_rectangle(row*xstep,col*ystep,(row+1)*xstep,(col+1)*ystep,fill=color,outline="")

	for settlement in info.sim.settlements:
		row = settlement.x
		col = settlement.y
		for household in settlement.households:
			main_color = getColor(overall_biggest_grain,household.grain)
			household.color = main_color
			for field in household.fields_owned:
				canvas.create_line((row+0.5)*xstep,(col+0.5)*ystep,(field.x+0.5)*xstep,(field.y+0.5)*ystep,fill=color_hexes[main_color])		


	for settlement in info.sim.settlements:
		row = settlement.x
		col = settlement.y

		#draw lines
		for household in settlement.households:
			main_color = household.color#getColor(overall_biggest_grain,household.grain)
			for field in household.fields_owned:	
				if field.harvested:
					canvas.create_image(((field.x+0.5)*xstep,(field.y+0.5)*xstep),image=info.barley_images[main_color])
				else: 	
					drawCircle(canvas,(field.x+0.5)*xstep,(field.y+0.5)*xstep,xstep/5,color_hexes[main_color])
		
		#draw settlements
		temp = settlement.population//50
		if temp > 2:
			temp = 2
		radius = ((temp+1)*xstep)/2

		biggest_household_grain = max([x.grain for x in settlement.households])
		main_color = getColor(overall_biggest_grain,biggest_household_grain)
		
		drawCircle(canvas,(row+0.5)*xstep,(col+0.5)*xstep,radius)
		canvas.create_image(((row+0.5)*xstep,(col+0.5)*xstep),image=info.house_images[main_color])	


	#create rectangles at edges to prevent ugly stuff
	canvas.create_rectangle(xstep*columns,0,xstep*(columns+2),ystep*rows,fill=general_background,outline=general_background)
	canvas.create_rectangle(0,ystep*rows,xstep*(columns+2),ystep*(rows+2),fill=general_background,outline=general_background)




############################################################################
#Close window behaviour
def onClose():
	info.ending = True
tk.protocol('WM_DELETE_WINDOW', onClose)  

#GUI setup frames:
############################################################################
topframe = Frame(tk,bg=top_panel_color,width=int((w1+w2+w3)*s),height=int(h1*s),relief='raised')
topframe.grid(row=0,column=0,columnspan=7,rowspan=1,sticky=N+S+E+W)
#topframe.grid_propagate(False)

sliderframe = Frame(tk,bg=general_background,width=int(w1*s),height=int((h2+h3)*s))
sliderframe.grid(row=1,column=0,columnspan=1,rowspan=6,sticky=N+S+E+W)
sliderframe.grid_rowconfigure(0,weight=1)
sliderframe.grid_columnconfigure(0,weight=1)

animationframe = Frame(tk,bg=general_background,width=int(w2*s),height=int(h2*s))
animationframe.grid(row=1,column=1,columnspan=3,rowspan=3,sticky=N+S+E+W,padx=padx,pady=pady)
animationframe.grid_propagate(False)

bottomframe = Frame(tk,bg=general_background,width=int(w2*s),height=int(h3*s))
bottomframe.grid(row=4,column=1,columnspan=3,rowspan=3,sticky=N+S+E+W)
bottomframe.grid_propagate(False)

graphsframe = Frame(tk,bg=general_background,width=int(w3*s),height=int((h2+h3)*s))
graphsframe.grid(row=1,column=4,columnspan=3,rowspan=6,sticky=N+S+E+W)
graphsframe.grid_propagate(False)

tk.grid_columnconfigure(4,weight=1,minsize=int(w2*s))
tk.grid_rowconfigure(4,weight=1,minsize=int(h3*s))
tk.grid_columnconfigure(1,weight=1,minsize=int(w2*s))
tk.grid_rowconfigure(1,weight=1,minsize=int(h2*s))
tk.grid_columnconfigure(4,weight=1,minsize=int(w2*s))
tk.grid_rowconfigure(4,weight=1,minsize=int(h3*s))
tk.grid_columnconfigure(0,weight=1,minsize=int(w1*s))
tk.grid_rowconfigure(0,weight=1,minsize=int(h1*s))

tk.minsize(int((w1+w2+w3)*s),int((h1+h2+h3)*s))

canvas = Canvas(animationframe,width=int(w2*s),height=int(h2*s),bg=general_background)
canvas.grid(row=0,column=0)

labelFrame = Frame(bottomframe,bg=general_background,width=int(2*s),height=int(s/3))
labelFrame.grid(row=1,column=0,padx=padx,pady=pady)
labelFrame.grid_propagate(False)

years_label = StringVar()
years = Label(labelFrame,textvariable=years_label,bg=general_background,)
years_label.set("")
years.grid(row=0,column=0)

#Top panel
############################################################################
button_reset = Button(topframe,text='Reset',bg=button_color,command = button_reset_on_click)
button_reset.grid(row=0,column=0,padx=padx,pady=pady)

pause_play_text = StringVar()
pause_play_text.set("Play   ")
button_play_pause = Button(topframe,textvariable=pause_play_text,bg=button_color,command = button_play_pause_on_click,state='disabled')
button_play_pause.grid(row=0,column=1,padx=padx,pady=pady)

button_step = Button(topframe,text='Step',bg=button_color,command = button_step_on_click,state='disabled')
button_step.grid(row=0,column=2,padx=padx,pady=pady)

button_run_all = Button(topframe,text='Run whole simulation',bg=button_color,command = button_run_all_on_click,state='disabled')
button_run_all.grid(row=0,column=5,padx=padx,pady=pady)

simulation_speed_scale = Scale(topframe,from_=1,to=100,resolution=1,orient=HORIZONTAL,sliderrelief="raised",length=(int(w2*s)),label="Simulation speed",bg=top_panel_color,troughcolor=trough_color)
simulation_speed_scale.grid(row=0,column=3,padx=padx*5)
simulation_speed_scale_tooltip = CreateToolTip(simulation_speed_scale,"Set speed of simulation in fps. Note that at higher speeds, not all frames are drawn.")

graph_speed_scale = Scale(topframe,from_=1,to=100,resolution=1,orient=HORIZONTAL,sliderrelief="raised",length=(int(w2/2*s)),label="Graphing speed",bg=top_panel_color,troughcolor=trough_color)
graph_speed_scale.grid(row=0,column=4,padx=padx*5)
graph_speed_scale.set(30)	
simulation_speed_scale_tooltip = CreateToolTip(graph_speed_scale,"How many updates pass between points being added to the graph")


#Slider panel
############################################################################

slider_canvas = Canvas(sliderframe,bg='white smoke',width=int(w1*s),height=int((h2+h3)*s))
slider_canvas.grid(row=0,column=0,columnspan=1,rowspan=1,sticky=N+S+E+W)

yscrollbar = Scrollbar(sliderframe,command=slider_canvas.yview)
yscrollbar.grid(row=0,column=1,sticky=N+S+E+W)

frame_in_canvas = Frame(slider_canvas,bg='white smoke',width = int(w1*s),height=int((h2+h3)*s))
frame_in_canvas.grid(row=0,column=0,columnspan=1,rowspan=1,sticky=N+S+E+W)

slider_info = [("model-time-span",500,100,500,50),
				("starting-settlements",14,5,20,1),
				("starting-households",7,1,10,1),
				("starting-household-size",5,2,10,1),
				("starting-grain",3000,100,8000,100),
				("min-ambition",0.1,0,1,0.1),
				("min-competency",0.5,0,1,0.1),
				("generational-variation",0.9,0,1,0.1),
				("knowledge-radius",5,3,40,1),
				("distance-cost",10,1,15,1),
				("fallow-limit",4,0,10,1),
				("pop-growth-rate",0.1,0,0.5,0.01),
				("min-fission-chance",0.5,0.5,0.9,0.1),
				("land-rental-rate",30,30,60,5)]

slider_frames = []
sliders = []
currentRow = 0
pos = 0
for name in slider_info:
	slider_frames.append(Frame(frame_in_canvas,bg='white smoke',bd=2,width=int(w1*s-2*padx),height=int(sliHeight)))
	slider_frames[-1].grid(row=currentRow,column=0,padx=padx)
	slider_frames[-1].grid_propagate(False)
	sliders.append(Scale(slider_frames[-1],from_=slider_info[pos][2],
		to=slider_info[pos][3],resolution=slider_info[pos][4],
		orient=HORIZONTAL,sliderrelief="raised",length=sliWidth,
		label=slider_info[pos][0],bg=bg_slider_color,troughcolor=trough_color))
	sliders[-1].grid(row=0,column=0,padx=1)
	sliders[-1].set(slider_info[pos][1])
	currentRow += 1
	pos += 1



check_box_info = [("manual-seed"),("allow-household-fission"),("allow-land-rental"),("legacy-mode")]
check_box_frames = []
check_boxes = []
check_var = []

pos = 0
for name in check_box_info:
	check_box_frames.append(Frame(frame_in_canvas,bg='white smoke',bd=2,width=int(w1*s-2*padx),height=int(chkHeight)))
	check_box_frames[-1].grid(row=currentRow,column=0,padx=padx)
	check_box_frames[-1].grid_propagate(False)

	var = IntVar()

	check_boxes.append(Checkbutton(check_box_frames[-1],text=check_box_info[pos],bg=bg_slider_color))
	if pos == 0:
		check_boxes.append(Checkbutton(check_box_frames[-1],text=check_box_info[pos],bg=bg_slider_color,command=popup_window,variable=var))
	else:
		check_boxes.append(Checkbutton(check_box_frames[-1],text=check_box_info[pos],bg=bg_slider_color,variable=var))

	check_var.append(var)
	check_boxes[-1].grid(row=0,column=0,padx=1)

	currentRow += 1
	pos += 1

slider_canvas.create_window(0, 0, anchor='nw', window=frame_in_canvas)
slider_canvas.update_idletasks()
slider_canvas.configure(scrollregion=(0,0,int(w1*s),(sliHeight)*len(slider_info)+(chkHeight)*len(check_box_info)), 
                 yscrollcommand=yscrollbar.set)


#Graph panel
#############################################################################
options = [("Total Grain","Years","Total grain"),("Total Population","Years","Population"),("Total households and settlements","",""),
		("Gini-index","Time","Gini"),("Grain equality","%-population","%-wealth"),
		("Households holding stated as percentage of the wealthiest households grain","Time","no of households"),
		("Settlement population","Years","Population"),("Max mean min settlement popuplation","Years","No of households"),
		("Mean min max wealth levels of households","Years","Grain"),("Household wealth households 20-24","Years","Wealth"),
		("Household wealth households 25-29","Years","Wealth")]



###############
#Graph 1
graph1frame = Frame(graphsframe,bg=general_background,width=int(w3*s))
graph1frame.grid(row=0,column=0,columnspan=1,rowspan=1,sticky=N+S+E+W)

plt.figure(num=0,figsize=(2*4,1*4),dpi=graphW)
graph1 = FigureCanvasTkAgg(plt.figure(0),graph1frame)
graph1.get_tk_widget().grid(row=0,column=0,columnspan=2,rowspan=1,padx=padx,pady=pady)
graph1.get_tk_widget().configure(background = 'BLACK', borderwidth = 1, relief = SUNKEN)

graph1var = StringVar(graph1frame)
graph1menu = OptionMenu(graph1frame,graph1var,*[x[0] for x in options],command=graphMenuOneClick)
graph1menu.config(width=int(graphW))
graph1menu.grid(row=2,column=0,columnspan=1,rowspan=1,padx=padx,sticky='W')

toolbarframe1 = Frame(graph1frame)
toolbarframe1.grid(row=1,column=0,stick='W',padx=padx)

toolbar1 = NavigationToolbar2Tk(graph1, toolbarframe1)
toolbar1.update()
toolbarframe1.grid_propagate(False)

################
#Graph 2
graph2frame = Frame(graphsframe,bg=general_background,width=int(w3*s))
graph2frame.grid(row=1,column=0,columnspan=1,rowspan=1,sticky=N+S+E+W)

plt.figure(num=1,figsize=(2*4,1*4),dpi=graphW)
graph2 = FigureCanvasTkAgg(plt.figure(1),graph2frame)
graph2.get_tk_widget().grid(row=0,column=0,columnspan=2,rowspan=1,padx=padx,pady=pady)
graph2.get_tk_widget().configure(background = 'BLACK', borderwidth = 1, relief = SUNKEN)

graph2var = StringVar(graph2frame)
graph2menu = OptionMenu(graph2frame,graph2var,*[x[0] for x in options],command=graphMenuTwoClick)
graph2menu.config(width=int(graphW))
graph2menu.grid(row=2,column=0,columnspan=1,rowspan=1,padx=padx,sticky='W')

toolbarframe2 = Frame(graph2frame,width=int(w3),bg='red')
toolbarframe2.grid(row=1,column=0,sticky='W',padx=padx)


toolbar2 = NavigationToolbar2Tk(graph2, toolbarframe2)
toolbar2.update()
toolbarframe2.grid_propagate(False)

#Info initialisation
#############################################################################
class Info:
	sim = None
	paused = None
	animationcount = None
	xpos = None
	graphcount = None
	clicked_once = None
	ending = None
	house_images = None
	barley_images = None
	seed = None
	graphs_data = None
	changed = None
	pointers = None
	chosen_households_one = None
	chosen_households_two = None
	pause_play_text = None
	stepping = None
	animationEvery = None
	graphEvery = None
	colors = None
	count_since_last_graph_draw = None
	force_draw_every = None

info = Info()
info.clicked_once = False
info.paused = True
info.ending = False
info.graphs_data = []
info.pointers = [6,7] #what does each graph point to 
info.changed = [False,False]
info.pause_play_text = pause_play_text
info.stepping = False
info.graphs_data = [
					[ [], [[]] ],		[ [], [[]] ],		[ [], [[]] ],
					[[], [[]] ],		[ [], [[]] ],
					[ [], [[],[],[]] ],
					[[],[]],			[[], [[],[],[]] ],
					[[], [[],[],[]] ],			[[],[[],[],[],[],[]]],
					[[],[[],[],[],[],[]]]
					]
info.seed = ""
info.colors = ["darkblue","darkred","darkgreen","orange","indigo","yellow","purple","red","green",
				"darkgoldenrod","pink","cyan","magenta","black","violet","maroon","brown","purple","gold","violet","darkorange"]


info.animationEvery = 1
info.count_since_last_graph_draw = 0
info.force_draw_every = 10

updateGraphs()
showGraphs()

#Mainloop:
#############################################################################
current_milli_time = lambda: int(round(time.time() * 1000))


def mainLoop():
	time1 = current_milli_time()
	if (not info.paused): #and not info.sim.done):	#if simulation is not paused

		if info.stepping:
			info.paused = True
			info.stepping = False

		info.animationEvery = 1

		if not info.stepping:
			info.animationEvery = int(simulation_speed_scale.get()//10)+1

		info.graphEvery = graph_speed_scale.get()

		info.animationcount += 1
		if (info.animationcount >= info.animationEvery):
			info.animationcount = 0
			drawGridSimulation(canvas,info)

		info.sim.tick()
		years_label.set("Years passed: " + str(info.sim.years_passed))

		if (len(info.sim.settlements)==0):
			info.paused = True
			drawGridSimulation(canvas,info)
			tk.after(30,mainLoop)
			return

		

		plotData()
	
		info.graphcount += 1
		if (info.graphcount >= info.graphEvery):
			info.graphcount = 0
			updateGraphs()
			showGraphs()
			
				

	if info.ending: #user has closed the program 
		tk.destroy()
		sys.exit()
		return	


	time2 = current_milli_time()

	sleep = int(1000/(1.0*simulation_speed_scale.get())) - time2 + time1
	if (sleep < 0):
		sleep = 0
	
	tk.after(sleep,mainLoop)

graph1var.set(options[info.pointers[0]][0])
graph2var.set(options[info.pointers[1]][0])

button_reset_on_click()
info.clicked_once = True

mainLoop()
tk.mainloop()

