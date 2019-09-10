from Constants import *

class Animations:
	def __init__(self,plt,canvas,info,graph1,graph2):
		#Intialise the variables
		self.plt = plt
		self.canvas = canvas
		self.info = info
		self.graph1 = graph1
		self.graph2 = graph2

		self.xstep = 0
		self.ystep = 0

	def plotData(self):
		#This method computes each new point of data for this tick of the simulation and adds the data to the appropriate graph


		#Compute the gini index graph according to the algorithm given in the original code
		total_grain = self.info.sim.total_grain
		total_households = len(self.info.sim.all_households)
		total_population = self.info.sim.total_population
		total_ambition = max([x.ambition for x in self.info.sim.all_households])
		total_competency = max([x.competency for x in self.info.sim.all_households])
		start_population = self.info.sim.starting_population
		
		average_ambition = total_ambition/total_households
		average_competency = total_competency/total_households

		sorted_grain = sorted([x.grain for x in self.info.sim.all_households])
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

		#Store the data point for the Total Grain graph
		self.info.graphs_data[0][0].append(self.info.sim.years_passed)
		self.info.graphs_data[0][1][0].append(self.info.sim.total_grain)

		#Store the data point for the Total Population graph
		self.info.graphs_data[1][0].append(self.info.sim.years_passed)
		self.info.graphs_data[1][1][0].append(self.info.sim.total_population)

		#Store the data point for the Total households and settlements graph
		self.info.graphs_data[2][0].append(self.info.sim.years_passed)
		self.info.graphs_data[2][1][0].append(len(self.info.sim.all_households))
		self.info.graphs_data[2][1][1].append(len(self.info.sim.settlements))

		#Store the data point for the Gini-index graph
		self.info.graphs_data[3][0].append(self.info.sim.years_passed)
		self.info.graphs_data[3][1][0].append(gini_index_reserve/total_households/0.5)

		#Store the data point for the Grain-equality graph
		x = range(len(lorenz_points))
		self.info.graphs_data[4][0]= x
		self.info.graphs_data[4][1][0]=lorenz_points

		#Compute how many houses fall within each color category
		t_pink = 0
		t_blue = 0
		t_yellow = 0
		self.info.graphs_data[5][0] = self.info.graphs_data[3][0]
		for settlement in self.info.sim.settlements:
		 	for household in settlement.households:
		 		if household.color == PINK:
		 			t_pink += 1
		 		if household.color == BLUE:
		 			t_blue += 1
		 		if household.color == YELLOW:
		 			t_yellow += 1


		#Store the data point for the "percentage of wealthiest household's grain" graph
		self.info.graphs_data[5][1][0].append(t_pink)
		self.info.graphs_data[5][1][1].append(t_blue)
		self.info.graphs_data[5][1][2].append(t_yellow)
		 

		#Store the data points for the Settlements population graph
		self.info.graphs_data[6][0].append(self.info.sim.years_passed)
		for i in range(len(self.info.sim.all_settlements)):
			self.info.graphs_data[6][1][i].append(self.info.sim.all_settlements[i].population)
		

		#Store the data points for the Max mean min settlement popuplation graph
		populations = [x.population for x in self.info.sim.settlements]
		self.info.graphs_data[7][0].append(self.info.sim.years_passed)
		self.info.graphs_data[7][1][0].append(max(populations))
		self.info.graphs_data[7][1][1].append(sum(populations)/len(populations))
		self.info.graphs_data[7][1][2].append(min(populations))
		
		#Store the data points for the Mean min max wealth levels of households graph
		grains = [x.grain for x in self.info.sim.all_households]
		self.info.graphs_data[8][0].append(self.info.sim.years_passed)
		self.info.graphs_data[8][1][0].append(max(grains))
		self.info.graphs_data[8][1][1].append(sum(grains)/len(grains))
		self.info.graphs_data[8][1][2].append(min(grains))

		#Store the data points for the Household wealth households 20-24 graph
		chosen_households = self.info.chosen_households_one

		self.info.graphs_data[9][0].append(self.info.sim.years_passed)
		length=len(chosen_households)
		for household,  i   in zip(chosen_households,  range(length)):
			self.info.graphs_data[9][1][i].append(household.grain)
		for j in range(length,5):
			self.info.graphs_data[9][1][i].append(0)

		#Store the data points for the Household wealth households 25-29 graph
		chosen_households = self.info.chosen_households_two

		self.info.graphs_data[10][0].append(self.info.sim.years_passed)
		length=len(chosen_households)
		for household,  i in zip(chosen_households,  range(length)):
			self.info.graphs_data[10][1][i].append(household.grain)
		for j in range(length,5):
			self.info.graphs_data[10][1][i].append(0)

	def updateGraphs(self):
		#This method checks which graph is currently being displayed using info.pointer and then does one of two things. 
		#If the user has recently selected a different graph to be drawn, or a period defined by info.force_draw_every has passed:
		#		The entire graph is cleared and redrawn using all the data. This prevents the data from becoming too segmented by 
		#		being drawn in parts as descrived 
		#Otherwise,
		#		Only new data which has been added to the graph since the last draw is added

		for fig in [0,1]: #for each graph which is displayed
			pointer = self.info.pointers[fig]
			data = self.info.graphs_data[pointer]
			xdata = data[0]
			ydata = data[1]
			redraw_graph = self.info.count_since_last_graph_draw >= self.info.force_draw_every

			self.plt.figure(fig)

			if (pointer == 4):	#if drawing the grain-equality figure, which is the only figure that doesn't have time on the x-axis 
								# and so must be redrawn each frame
				self.plt.clf()
				if (len(xdata)>1):
					self.plt.plot(xdata,ydata[0],label='Wealth',color=colors[0])
					self.plt.plot([xdata[0],xdata[-1]],[ydata[0][0],ydata[0][-1]],label='Equality',color=colors[1])
					self.plt.legend()

			elif (self.info.changed[fig] or redraw_graph): #if user changed displayed graph or the graph should be redrawn
				if redraw_graph:
					self.info.count_since_last_graph_draw = 0
				self.info.changed[fig] = False
				self.plt.clf()

				if (pointer == 5):	#if drawing the "percentage of wealthiest household's grain" graph
					line, = self.plt.plot(xdata,ydata[0],label='>66%')
					line.set_color(color_hexes[PINK])
					line, = self.plt.plot(xdata,ydata[1],label='33-66%')
					line.set_color(color_hexes[BLUE])
					line, = self.plt.plot(xdata,ydata[2],label='<33%')
					line.set_color(color_hexes[YELLOW])
					self.plt.legend()

				elif (pointer == 7 or pointer == 8):	#if drawing one of the max-min-avg graphs
					self.plt.plot(xdata,ydata[0],label='max',color=colors[0])
					self.plt.plot(xdata,ydata[1],label='avg',color=colors[1])
					self.plt.plot(xdata,ydata[2],label='min',color=colors[2]) 
					self.plt.legend()

				elif (pointer == 2):
					self.plt.plot(xdata,ydata[0],label='No. households',color=colors[0])
					self.plt.plot(xdata,ydata[1],label='No. settlements',color=colors[1])
					self.plt.legend()

				else: 
					for i in range(len(ydata)):	#if drawing any other graph. These graphs just have lots of lines which are plotted
						line = ydata[i]
						color = colors[i]
						self.plt.plot(xdata,line,color=color)
			
				self.plt.title(options[pointer][0])
				self.plt.xlabel(options[pointer][1])
				self.plt.ylabel(options[pointer][2])
				self.plt.tight_layout()

			else: 	#or else we simply add the points which have changed
				if (len(xdata)>1):
					g = self.info.graphEvery

					if (pointer == 5):#if drawing the "percentage of wealthiest household's grain" graph
						line, = self.plt.plot(xdata[-(g+2):-1],ydata[0][-(g+2):-1])
						line.set_color(color_hexes[PINK])
						line, = self.plt.plot(xdata[-(g+2):-1],ydata[1][-(g+2):-1])
						line.set_color(color_hexes[BLUE])
						line, = self.plt.plot(xdata[-(g+2):-1],ydata[2][-(g+2):-1])
						line.set_color(color_hexes[YELLOW])
						self.plt.legend()

					elif (pointer == 7 or pointer == 8):#if drawing one of the max-min-avg graphs
						self.plt.plot(xdata[-(g+2):-1],ydata[0][-(g+2):-1],color=colors[0])
						self.plt.plot(xdata[-(g+2):-1],ydata[1][-(g+2):-1],color=colors[1])
						self.plt.plot(xdata[-(g+2):-1],ydata[2][-(g+2):-1],color=colors[2]) 
						self.plt.legend()

					elif (pointer == 2):
						self.plt.plot(xdata[-(g+2):-1],ydata[0][-(g+2):-1],color=colors[0])
						self.plt.plot(xdata[-(g+2):-1],ydata[1][-(g+2):-1],color=colors[1])

					else: #if drawing any other graph. These graphs just have lots of lines which are plotted
						for i in range(len(ydata)):
							line = ydata[i]
							color = colors[i]
							self.plt.plot(xdata[-(g+2):-1],line[-(g+2):-1],color=color)

	def getColor(self,max_grain,grain):
		#Given the value of the household with the biggest grain, and the value of any other household, determines the color the 
		# household should have
		if (grain > 2/3*max_grain):
			return PINK
		elif (grain > 1/3*max_grain):
			return BLUE
		else:
			return YELLOW

	def drawCircle(self,canvas,x,y,r,color=False):
		#Draws a circle on canvas centered at position (x,y) with radius r. Draws this default as a black circle with a grey outline. If 
		# given a color, instead draws the entire circle just that color (for drawing the colored circles on land that is owned by not planted)
		if (not color):
			canvas.create_oval(x-r,y-r,x+r,y+r,fill='black',outline=circle_border_outline,width=r/6)
		else:
			canvas.create_oval(x-r,y-r,x+r,y+r,fill=color,width=0)

	def drawGridSimulation(self):
		#Draws one frame of the simulation to the canvas. 

		#rename for easier use
		simulation = self.info.sim
		overallterrain = simulation.terrain

		#calculate the width and height of each block of the simulation
		width, height = self.canvas.winfo_width(),self.canvas.winfo_height()
		rows,columns = len(overallterrain),len(overallterrain[0])
		self.xstep = width/columns - 1
		self.ystep = height/rows - 1
		self.clearCanvas()

		#calculate the household which has the biggest grain. Used to determine the color of households
		if (len(self.info.sim.all_households)>0):
			overall_biggest_grain = max([x.grain for x in self.info.sim.all_households])
		else:
			overall_biggest_grain = 0

		#color every block in the grid either as blue for the river or green for normal land
		for row in range(0,rows):
			for col in range(0,columns):
				block = overallterrain[row][col]		
				fertility = block.fertility/2
				if block.river:
					color = 'blue'
				elif block.was_settlement:
					color='yellow'
				else:
					color = self.info.greeness(int(245-fertility*205))
				self.canvas.create_rectangle(row*self.xstep,col*self.ystep,(row+1)*self.xstep,(col+1)*self.ystep,fill=color,outline="")

		#draw the lines from the settlements to the fields
		for settlement in self.info.sim.settlements:
			row = settlement.x
			col = settlement.y
			for household in settlement.households:
				main_color = self.getColor(overall_biggest_grain,household.grain)
				household.color = main_color
				for field in household.fields_owned:
					self.canvas.create_line((row+0.5)*self.xstep,(col+0.5)*self.ystep,(field.x+0.5)*self.xstep,(field.y+0.5)*self.ystep,fill=color_hexes[main_color])		

		#draw the settlements and give them their appropriate color. Also draw the circle around them with the appropriate radius
		for settlement in self.info.sim.settlements:
			row = settlement.x
			col = settlement.y

			#draw the barleys with the appropriate colors on the blocks
			for household in settlement.households:
				main_color = household.color#getColor(overall_biggest_grain,household.grain)
				for field in household.fields_owned:	
					if field.harvested:
						self.canvas.create_image(((field.x+0.5)*self.xstep,(field.y+0.5)*self.xstep),image=self.info.barley_images[main_color])
					else: 	
						self.drawCircle(self.canvas,(field.x+0.5)*self.xstep,(field.y+0.5)*self.xstep,self.xstep/5,color_hexes[main_color])
			
			#calculate size of circle
			temp = settlement.population//50
			if temp > 2:
				temp = 2
			radius = ((temp+1)*self.xstep)/2

			if len(settlement.households)>0:
				biggest_household_grain = max([x.grain for x in settlement.households])
			else:
				biggest_household_grain = 0
			main_color = self.getColor(overall_biggest_grain,biggest_household_grain)
			
			self.drawCircle(self.canvas,(row+0.5)*self.xstep,(col+0.5)*self.xstep,radius)
			self.canvas.create_image(((row+0.5)*self.xstep,(col+0.5)*self.xstep),image=self.info.house_images[main_color])	


		#create rectangles at edges to prevent ugly stuff
		self.canvas.create_rectangle(self.xstep*columns,0,self.xstep*(columns+2),self.ystep*rows,fill=general_background,outline=general_background)
		self.canvas.create_rectangle(0,self.ystep*rows,self.xstep*(columns+2),self.ystep*(rows+2),fill=general_background,outline=general_background)


	def showGraphs(self):
		#Updates the onscreen displays of the data 
		self.info.count_since_last_graph_draw += 1
		self.graph1.draw()
		self.graph2.draw() 

	def clearCanvas(self):
		self.canvas.delete('all')
