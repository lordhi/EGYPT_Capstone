from Constants import *

class Animations:
	plt = None
	canvas = None
	info = None
	graph1 = None
	graph2 = None

	def __init__(self,plt,canvas,info,graph1,graph2):
		self.plt = plt
		self.canvas = canvas
		self.info = info
		self.graph1 = graph1
		self.graph2 = graph2

	def plotData(self):
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


		#Total Grain
		self.info.graphs_data[0][0].append(self.info.sim.years_passed)
		self.info.graphs_data[0][1][0].append(self.info.sim.total_grain)

		#Total Population
		self.info.graphs_data[1][0].append(self.info.sim.years_passed)
		self.info.graphs_data[1][1][0].append(self.info.sim.total_population)

		#Total households and settlements
		self.info.graphs_data[2][0].append(self.info.sim.years_passed)
		self.info.graphs_data[2][1][0].append(len(self.info.sim.settlements) + len(self.info.sim.all_households))

		#Gini-index
		self.info.graphs_data[3][0].append(self.info.sim.years_passed)
		self.info.graphs_data[3][1][0].append(gini_index_reserve/total_households/2)

		#Grain-equality
		x = range(len(lorenz_points))
		self.info.graphs_data[4][0]= x
		self.info.graphs_data[4][1][0]=lorenz_points

		#Households holding
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

		self.info.graphs_data[5][1][0].append(t_pink)
		self.info.graphs_data[5][1][1].append(t_blue)
		self.info.graphs_data[5][1][2].append(t_yellow)
		 

		#Settlements population
		self.info.graphs_data[6][0].append(self.info.sim.years_passed)
		for i in range(len(self.info.sim.all_settlements)):
			self.info.graphs_data[6][1][i].append(self.info.sim.all_settlements[i].population)
		

		#Max mean min settlement popuplation
		populations = [x.population for x in self.info.sim.settlements]
		self.info.graphs_data[7][0].append(self.info.sim.years_passed)
		self.info.graphs_data[7][1][0].append(max(populations))
		self.info.graphs_data[7][1][1].append(sum(populations)/len(populations))
		self.info.graphs_data[7][1][2].append(min(populations))
		
		#Mean min max wealth levels of households
		grains = [x.grain for x in self.info.sim.all_households]
		self.info.graphs_data[8][0].append(self.info.sim.years_passed)
		self.info.graphs_data[8][1][0].append(max(grains))
		self.info.graphs_data[8][1][1].append(sum(grains)/len(grains))
		self.info.graphs_data[8][1][2].append(min(grains))

		#Household wealth households 20-24
		chosen_households = self.info.chosen_households_one

		self.info.graphs_data[9][0].append(self.info.sim.years_passed)
		length=len(chosen_households)
		for household,  i   in zip(chosen_households,  range(length)):
			self.info.graphs_data[9][1][i].append(household.grain)
		for j in range(length,5):
			self.info.graphs_data[9][1][i].append(0)

		#Household wealth households 25-29
		chosen_households = self.info.chosen_households_two

		self.info.graphs_data[10][0].append(self.info.sim.years_passed)
		length=len(chosen_households)
		for household,  i in zip(chosen_households,  range(length)):
			self.info.graphs_data[10][1][i].append(household.grain)
		for j in range(length,5):
			self.info.graphs_data[10][1][i].append(0)

	def updateGraphs(self):
		for fig in [0,1]:
			pointer = self.info.pointers[fig]
			data = self.info.graphs_data[pointer]
			xdata = data[0]
			ydata = data[1]
			redraw_graph = self.info.count_since_last_graph_draw >= self.info.force_draw_every

			self.plt.figure(fig)
			if (pointer == 4):
				self.plt.clf()
				if (len(xdata)>1):
					self.plt.plot(xdata,ydata[0],label='Wealth',color=colors[0])
					self.plt.plot([xdata[0],xdata[-1]],[ydata[0][0],ydata[0][-1]],label='Equality',color=colors[1])
					self.plt.legend()

			elif (self.info.changed[fig] or redraw_graph):
				if redraw_graph:
					self.info.count_since_last_graph_draw = 0
				self.info.changed[fig] = False
				self.plt.clf()

				if (pointer == 5):
					line, = self.plt.plot(xdata,ydata[0],label='>66%')
					line.set_color(color_hexes[PINK])
					line, = self.plt.plot(xdata,ydata[1],label='33-66%')
					line.set_color(color_hexes[BLUE])
					line, = self.plt.plot(xdata,ydata[2],label='<33%')
					line.set_color(color_hexes[YELLOW])
					self.plt.legend()

				elif (pointer == 7 or pointer == 8):
					self.plt.plot(xdata,ydata[0],label='max',color=colors[0])
					self.plt.plot(xdata,ydata[1],label='avg',color=colors[1])
					self.plt.plot(xdata,ydata[2],label='min',color=colors[2]) 
					self.plt.legend()

				else: #pointer = 0,1,2,3,6,9,10
					#print(len(ydata))
					for i in range(len(ydata)):
					#for i in range(len(self.info.sim.all_settlements)):
						line = ydata[i]
						color = colors[i]
						self.plt.plot(xdata,line,color=color)
			
				self.plt.title(options[pointer][0])
				self.plt.xlabel(options[pointer][1])
				self.plt.ylabel(options[pointer][2])
				self.plt.tight_layout()

			elif (len(xdata)>1):	
				g = self.info.graphEvery

				if (pointer == 5):
					line, = self.plt.plot(xdata[-(g+2):-1],ydata[0][-(g+2):-1])
					line.set_color(color_hexes[PINK])
					line, = self.plt.plot(xdata[-(g+2):-1],ydata[1][-(g+2):-1])
					line.set_color(color_hexes[BLUE])
					line, = self.plt.plot(xdata[-(g+2):-1],ydata[2][-(g+2):-1])
					line.set_color(color_hexes[YELLOW])
					self.plt.legend()

				elif (pointer == 7 or pointer == 8):
					self.plt.plot(xdata[-(g+2):-1],ydata[0][-(g+2):-1],color=colors[0])
					self.plt.plot(xdata[-(g+2):-1],ydata[1][-(g+2):-1],color=colors[1])
					self.plt.plot(xdata[-(g+2):-1],ydata[2][-(g+2):-1],color=colors[2]) 
					self.plt.legend()

				else: #pointer = 0,1,2,3,6,9,10
					for i in range(len(ydata)):
					#for i in range(len(self.info.sim.all_settlements)):
						line = ydata[i]
						color = colors[i]
						self.plt.plot(xdata[-(g+2):-1],line[-(g+2):-1],color=color)

	def getColor(self,max_grain,grain):
		if (grain > 2/3*max_grain):
			return PINK
		elif (grain > 1/3*max_grain):
			return BLUE
		else:
			return YELLOW

	def drawCircle(self,canvas,x,y,r,color=False):
		if (not color):
			canvas.create_oval(x-r,y-r,x+r,y+r,fill='black',outline=circle_border_outline,width=r/6)
		else:
			canvas.create_oval(x-r,y-r,x+r,y+r,fill=color,width=0)

	def drawGridSimulation(self):
		simulation = self.info.sim
		width, height = self.canvas.winfo_width(),self.canvas.winfo_height()
		overallterrain = simulation.terrain

		rows,columns = len(overallterrain),len(overallterrain[0])
		xstep = width/columns - 1
		ystep = height/rows - 1
		self.canvas.delete('all')
		if (len(self.info.sim.all_households)>0):
			overall_biggest_grain = max([x.grain for x in self.info.sim.all_households])
		else:
			overall_biggest_grain = 0

		for row in range(0,rows):
			for col in range(0,columns):
				block = overallterrain[row][col]		
				fertility = block.fertility/2 #still need to fix this!
				if block.river:
					color = 'blue'
				else:
					color = self.info.greeness(int(245-fertility*205))
				self.canvas.create_rectangle(row*xstep,col*ystep,(row+1)*xstep,(col+1)*ystep,fill=color,outline="")

		for settlement in self.info.sim.settlements:
			row = settlement.x
			col = settlement.y
			for household in settlement.households:
				main_color = self.getColor(overall_biggest_grain,household.grain)
				household.color = main_color
				for field in household.fields_owned:
					self.canvas.create_line((row+0.5)*xstep,(col+0.5)*ystep,(field.x+0.5)*xstep,(field.y+0.5)*ystep,fill=color_hexes[main_color])		


		for settlement in self.info.sim.settlements:
			row = settlement.x
			col = settlement.y

			#draw lines
			for household in settlement.households:
				main_color = household.color#getColor(overall_biggest_grain,household.grain)
				for field in household.fields_owned:	
					if field.harvested:
						self.canvas.create_image(((field.x+0.5)*xstep,(field.y+0.5)*xstep),image=self.info.barley_images[main_color])
					else: 	
						self.drawCircle(self.canvas,(field.x+0.5)*xstep,(field.y+0.5)*xstep,xstep/5,color_hexes[main_color])
			
			#draw settlements
			temp = settlement.population//50
			if temp > 2:
				temp = 2
			radius = ((temp+1)*xstep)/2

			biggest_household_grain = max([x.grain for x in settlement.households])
			main_color = self.getColor(overall_biggest_grain,biggest_household_grain)
			
			self.drawCircle(self.canvas,(row+0.5)*xstep,(col+0.5)*xstep,radius)
			self.canvas.create_image(((row+0.5)*xstep,(col+0.5)*xstep),image=self.info.house_images[main_color])	


		#create rectangles at edges to prevent ugly stuff
		self.canvas.create_rectangle(xstep*columns,0,xstep*(columns+2),ystep*rows,fill=general_background,outline=general_background)
		self.canvas.create_rectangle(0,ystep*rows,xstep*(columns+2),ystep*(rows+2),fill=general_background,outline=general_background)


	def showGraphs(self):
		self.info.count_since_last_graph_draw += 1
		self.graph1.draw()
		self.graph2.draw() 
