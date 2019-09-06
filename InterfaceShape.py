#External imports
from tkinter import *
import tkinter.simpledialog as simpledialog
import time
import matplotlib.pyplot as plt
import sys

try:
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk as NavigationToolbar2Tk
except:
	from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg as NavigationToolbar2Tk

#Imports from our own classes
from CreateToolTip import CreateToolTip
from Simulation import Simulation
from Info import *
from Constants import *

############################################################################
#Set up root
tk = Tk()
tk.title("Egypt simulation")
tk.configure(background=general_background)

#Parameters:
############################################################################
w1 = 2 	#slider frame width
w2 = 8.9 	#animation frame + graphs frame width
w3 = 7	#graphs2 frame width
h1 = 0.6 	#top frame height
h2 = w2	#animation frame height
h3 = 0.4  #graphs 1 frame height
		#graphs 2 frame height is h2 + h3

s = 80 / 864 * tk.winfo_screenheight() #how many pixels is the side of one cell worth
padx = int(s/9)
pady = int(s/18)
sfHeight = s*0.95 #the heights of the side slider blocks
sliHeight = sfHeight - 2*pady #slider heights
sliWidth = w1*s-2*padx-5
chkHeight = s/2 #the heights of the check boxes
graphW = 0.8*s

#Responding to user clicks
#############################################################################
def button_step_on_click():
	info.paused = False
	info.stepping = True
	info.updateGraphs()
	info.showGraphs()
	info.drawGridSimulation()

	if (info.sim.done):
			button_run_all['state'] = 'disabled'
			button_play_pause['state'] = 'disabled'

def button_reset_on_click():
	button_play_pause['state'] = 'normal'
	#button_run_all['state']='normal'
	if not (info.clicked_once and not info.paused):
		button_step['state'] = 'normal'

	slider_values = [x.get()*1.0 for x in sliders]
	check_values = [x.get() for x in check_var]
	info.sim = Simulation(*slider_values,*check_values,info.seed)

	info.animationcount = 0
	info.xpos = 0
	info.graphcount = 0

	width = canvas.winfo_width()
	columns = len(info.sim.terrain[0])
	xstep = int(width/columns - 1)

	info.barley_images = [info.resizeImage(img,int(xstep*4/5.0)) for img in info.barley_images_permanent]
	info.house_images = [info.resizeImage(img,int(2/3.0*xstep)) for img in info.house_images_permanent]

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

	info.years_label.set("")

	#info.sim.tick()
	info.drawGridSimulation()
	info.changed[0] = True
	info.changed[1] = True
	info.updateGraphs()
	info.showGraphs()

def button_run_all_on_click():
	button_run_all['state']='disabled'
	button_play_pause['state']='disabled'
	button_reset['state']='disabled'
	button_step['state']='disabled'
	
	count = 0
	while not info.sim.done:
		count += 1
		if (count >= 100):
			setYearsPassed()
			count = 0
		info.sim.tick()
		info.plotData()
		tk.update()
		tk.update_idletasks()

	button_run_all['state']='normal'
	button_play_pause['state']='normal'
	button_reset['state']='normal'
	button_step['state']='normal'

	info.changed[0] = True
	info.changed[1] = True
	info.drawGridSimulation()
	info.updateGraphs()
	info.showGraphs()
	setYearsPassed()
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
		info.plotData()
		info.updateGraphs()
		info.showGraphs()

	if (info.sim.done):
		button_run_all['state'] = 'disabled'
		button_play_pause['state'] = 'disabled'

def graphMenuOneClick(selection):
	names = [x[0] for x in options]
	info.pointers[0] = names.index(selection)
	info.changed[0] = True
	info.updateGraphs()
	info.showGraphs()

def graphMenuTwoClick(selection):
	names = [x[0] for x in options]
	info.pointers[1] = names.index(selection)
	info.changed[1] = True
	info.updateGraphs()
	info.showGraphs()

def popup_window():
	if check_var[0].get():
		info.seed = simpledialog.askstring("Enter a seed:","e.g. 12341234")

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

tk.grid_columnconfigure(1,weight=1,minsize=int(w2*s))
tk.grid_rowconfigure(1,weight=1,minsize=int(h2*s))
tk.grid_columnconfigure(4,weight=1,minsize=int(w3*s))
tk.grid_rowconfigure(4,weight=1,minsize=int(h3*s))
tk.grid_columnconfigure(0,weight=1,minsize=int(w1*s*1.05))
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

simulation_speed_scale = Scale(topframe,from_=1,to=100,resolution=1,orient=HORIZONTAL,sliderrelief="raised",length=(int(0.87*w2*s)),label="Simulation speed",bg=top_panel_color,troughcolor=trough_color)
simulation_speed_scale.grid(row=0,column=3,padx=padx*5)
simulation_speed_scale_tooltip = CreateToolTip(simulation_speed_scale,"Set speed of simulation in fps. Note that at higher speeds, not all frames are drawn.")

graph_speed_scale = Scale(topframe,from_=1,to=100,resolution=1,orient=HORIZONTAL,sliderrelief="raised",length=(int(w2/2*s)),label="Graphing speed",bg=top_panel_color,troughcolor=trough_color)
graph_speed_scale.grid(row=0,column=4,padx=padx*5)
graph_speed_scale.set(30)	
simulation_speed_scale_tooltip = CreateToolTip(graph_speed_scale,"How many years pass between points being added to the graph")


#Slider panel
############################################################################

slider_canvas = Canvas(sliderframe,bg='white smoke',width=int(w1*s),height=int((h2+h3)*s))
slider_canvas.grid(row=0,column=0,columnspan=1,rowspan=1,sticky=N+S+E+W)

yscrollbar = Scrollbar(sliderframe,command=slider_canvas.yview)
yscrollbar.grid(row=0,column=1,sticky=N+S+E+W)

frame_in_canvas = Frame(slider_canvas,bg='white smoke',width = int(w1*s),height=int((h2+h3)*s))
frame_in_canvas.grid(row=0,column=0,columnspan=1,rowspan=1,sticky=N+S+E+W)

slider_info = [("model-time-span",1000,100,1000,50),
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
info = Info(plt,canvas,graph1,graph2)
info.pause_play_text = pause_play_text
info.years_label = years_label
info.updateGraphs()
info.showGraphs()


#A helper function
#############################################################################
def setYearsPassed():
	info.years_label.set("Years passed: " + str(info.sim.years_passed))

#Mainloop:
#############################################################################
current_milli_time = lambda: int(round(time.time() * 1000))
def mainLoop():
	time1 = current_milli_time()
	if (not info.paused and not info.sim.done):	#if simulation is not paused
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
			info.drawGridSimulation()

		info.sim.tick()
		setYearsPassed()

		if (len(info.sim.settlements)==0):
			info.paused = True
			info.drawGridSimulation()
			tk.after(30,mainLoop)
			return

		info.plotData()
	
		info.graphcount += 1
		if (info.graphcount >= info.graphEvery):
			info.graphcount = 0
			info.updateGraphs()
			info.showGraphs()
			
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