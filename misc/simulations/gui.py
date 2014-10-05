import matplotlib

class GUI:

	def __init__(self): 

		self.index = 0
		self.pyephem = 0
		self.predict = 0
		self.pyorbital = 0
		self.STK = 0
		self.orbitron = 0

		import get_elements
		object_elements = get_elements.Get_list_length()
		self.length = object_elements.length - 1

		self.crear_figura()


	def crear_figura(self):

		import Tkinter as tk

		from matplotlib.figure import Figure

		from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

		# Default
		available_predict = 'no'
		available_pyephem = 'no'
		available_pyorbital = 'no'
		available_orbitron = 'no'
		available_STK = 'no'

		import output_data
		available = output_data.Check_data(self.index)
		available_predict = available.predict
		available_pyephem = available.pyephem
		available_pyorbital = available.pyorbital

		figure_predict = output_data.Read_predict_data(self.predict)
		figure_pyephem = output_data.Read_pyephem_data(self.pyephem)
		figure_pyorbital = output_data.Read_pyorbital_data(self.pyorbital)
		figure_STK = output_data.Read_STK_data(self.STK)
		figure_orbitron = output_data.Read_orbitron_data(self.orbitron)

		time = figure_pyephem.pyephem_simulation_time

		figure = output_data.Read_data(self.pyephem, self.predict, self.pyorbital)
		difference_alt, difference_az = figure.pyephem_minus_predict()


		# Satellite name
		import get_elements
		object_name = get_elements.Get_name(self.index)

		# Plot
		self.f = Figure(figsize=(6,7), dpi = 80)
		self.f.suptitle(object_name.name, fontsize=16)

		# Subplot altitude
		self.a = self.f.add_subplot(211)
		# Check if data is available
		if available_predict == 'yes':
			predict_alt = figure_predict.predict_alt_satellite
			self.a.plot(time, predict_alt, 'r', label="predict")
		if available_pyephem == 'yes':
			pyephem_alt = figure_pyephem.pyephem_alt_satellite
			self.a.plot(time, pyephem_alt, 'b', label="PyEphem")
		if available_pyorbital == 'yes':
			pyorbital_alt = figure_pyorbital.pyorbital_alt_satellite
			self.a.plot(time, pyorbital_alt, 'y', label="pyorbital")

		STK_alt = figure_STK.STK_alt_satellite
		STK_time = figure_STK.STK_simulation_time
		self.a.plot(STK_time, STK_alt, 'g', label ="STK")

		self.a.legend(loc = 2, borderaxespad = 0., prop={'size':12})
		self.a.set_ylabel("Degrees")
		# Grid is on
		self.a.grid(True)

		# Subplot azimuth
		self.b = self.f.add_subplot(212)
		# Check if data is available
		if available_predict == 'yes':
			predict_az = figure_predict.predict_az_satellite
			self.b.plot(time, predict_az, 'r', label="predict")
		if available_pyephem == 'yes':
			pyephem_az = figure_pyephem.pyephem_az_satellite
			self.b.plot(time, pyephem_az, 'b', label="PyEphem")
		if available_pyorbital == 'yes':
			pyorbital_az = figure_pyorbital.pyorbital_az_satellite
			self.b.plot(time, pyorbital_az, 'y', label="pyorbital")

		STK_az = figure_STK.STK_az_satellite
		STK_time = figure_STK.STK_simulation_time
		self.b.plot(STK_time, STK_az, 'g', label ="STK")

                self.b.legend(loc = 2, borderaxespad = 0., prop={'size':12})
                self.b.set_ylabel("Degrees")
		# Grid is on
		self.b.grid(True)

		import Tkinter as tk
		left_frame = tk.Frame(root, height = 800, width = 500, padx = 5, pady = 5)
		left_frame.grid(column = 0, row = 0, columnspan = 1, rowspan = 3)

		# Figure controls	
		self.canvas = FigureCanvasTkAgg(self.f, master = left_frame)
		self.canvas.show()
		self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

		toolbar = NavigationToolbar2TkAgg(self.canvas, left_frame )
		toolbar.update()
		self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=0)

		# Plot g
		self.g = Figure(figsize=(6,4), dpi = 80)
		self.g.suptitle("Comparation", fontsize=16)
		
		# Subplot c
		self.c = self.g.add_subplot(111)
		self.c.plot(time, difference_alt, label="difference")

		self.c.legend(loc = 2, borderaxespad = 0., prop={'size':12})

		self.c.set_ylabel("Altitude - Degrees")

		self.c.grid(True)

		right_frame = tk.Frame(root, height = 330, width = 500, bd = 0)
		right_frame.grid(column = 1, row = 0, columnspan = 1, rowspan = 1, padx = 5, pady = 5)
		right_frame.grid_propagate(0)

		self.canvas2 = FigureCanvasTkAgg(self.g, master=right_frame)
		self.canvas2.show()
		self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)

		data_frame = tk.LabelFrame(root, text = "Data", height = 215, width = 500, padx = 5, pady = 5)
		data_frame.grid(column = 1, row = 1, columnspan = 1, rowspan = 1)
		data_frame.columnconfigure(0, minsize = 110)
		data_frame.columnconfigure(1, minsize = 110)
		data_frame.columnconfigure(2, minsize = 110)
		data_frame.columnconfigure(3, minsize = 110)
		data_frame.grid_propagate(0)

		# Name
		label_name = tk.Label(data_frame, text="Name")
		label_name.grid(column = 0, row = 0, columnspan = 1, rowspan = 1, sticky = tk.W)

		self.text_name = tk.StringVar()
		import get_elements
                object_name = get_elements.Get_name(self.index)
		self.text_name.set(object_name.name)

		name = tk.Label(data_frame, textvariable = self.text_name)
		name.grid(column = 1, row = 0, columnspan = 1, rowspan = 1, sticky = tk.E)

		# File
		file_name = tk.Label(data_frame, text="File")
		file_name.grid(column = 0, row = 1, columnspan = 1, rowspan = 1, sticky = tk.W)

		import sys
		self.file_name = tk.StringVar()
		self.file_name.set(sys.argv[1])

		file = tk.Label(data_frame, textvariable = self.file_name)
		file.grid(column = 1, row = 1, columnspan = 1, rowspan = 1, sticky = tk.E)

#		import os		
#		directorio_actual = os.getcwd()
		
		# LOGO
#		from PIL import Image, ImageTk
#		image = Image.open(directorio_actual + '/LOGO.png')
#		image = Image.open('/home/case/LOGO.png')
#		logo = ImageTk.PhotoImage(image)

#		label_logo = tk.Label(self.data_root, image = logo)
#		label_logo.grid(column = 1, row = 0, columnspan = 1, rowspan = 1)

		label_sims = tk.Label(data_frame, text = "Simulations availables")
		label_sims.grid(column = 0, row = 2, columnspan = 2, rowspan = 1, sticky = tk.W)

		# Generate data
		import scrolledlist
		sims_availables = scrolledlist.ScrolledList(data_frame, width = 20, height = 3, callback = self.pick_simulation)
		sims_availables.grid(column = 0, row = 3, columnspan = 3, rowspan = 1, sticky = tk.W)

		# Generate list of simulations
		self.sims_availables(available_predict, available_pyephem, available_pyorbital, available_orbitron, available_STK)

		for i in range(len(self.list_of_simulations)):
			sims_availables.append(self.list_of_simulations[i])

		label_std = tk.Label(data_frame, text = "Standard desviation")
		label_std.grid(column = 0, row = 4, columnspan = 2, rowspan = 1, sticky = tk.W)

		# StringVar para la desviacion
		
		# Boton para realizar de nuevo las simulaciones
		redo = tk.Button(data_frame, text = "Redo sims")
		redo.grid(column = 3, row = 5, columnspan = 1, rowspan = 1, sticky = tk.W)

		# Inclination
		elements = get_elements.Get_elements(sys.argv[1], self.index)
		label_incl = tk.Label(data_frame, text="Inclination")
		label_incl.grid(column = 2, row = 0, columnspan = 1, rowspan = 1, sticky = tk.W)
		
		self.text_incl = tk.DoubleVar()
		self.text_incl.set(elements.inclination)

		incl = tk.Label(data_frame, textvariable = self.text_incl)
		incl.grid(column = 3, row = 0, columnspan = 1, rowspan = 1, sticky = tk.E)

		# Mean motion
		label_motion = tk.Label(data_frame, text = "Mean motion")
		label_motion.grid(column = 2, row = 1, columnspan = 1, rowspan = 1, sticky = tk.W)

		self.text_motion = tk.DoubleVar()
		self.text_motion.set(elements.mean_motion)

		motion = tk.Label(data_frame, textvariable = self.text_motion)
		motion.grid(column = 3, row = 1, columnspan = 1, rowspan = 1, sticky = tk.E)

		# Control frame
		control_frame = tk.LabelFrame(root, text = "Controls", height = 55, width = 500, padx = 5, pady = 5)
		control_frame.grid(column = 1, row = 2, columnspan = 1, rowspan = 1)
		control_frame.grid_propagate(0)

		self.next = tk.Button(master = control_frame, text='Next', command=self.next)
		self.next.grid(column = 0, row = 0, columnspan = 1, rowspan = 1)
		self.forward = tk.Button(master = control_frame, text='Forward', command=self.forward)
		self.forward.grid(column = 1, row = 0, columnspan = 1, rowspan = 1)
		button = tk.Button(master = control_frame, text='Quit', command=self._quit)
		button.grid(column = 2, row = 0, columnspan = 1, rowspan = 1)

		# Check buttons state
		if self.index == 0:
			self.forward.configure(state = tk.DISABLED)
			self.next.configure(state = tk.NORMAL)
		elif self.index == self.length:
			self.forward.configure(state = tk.NORMAL)
			self.next.configure(state = tk.DISABLED)
		else:
			self.forward.configure(state = tk.NORMAL)
			self.next.configure(state = tk.NORMAL)


	def next(self):

		import output_data
		available = output_data.Check_data(self.index) 		

		available_predict = available.predict
		if available_predict == 'yes':
			self.predict = self.predict + 1
		
		available_pyephem = available.pyephem
		if available_pyephem == 'yes':
			self.pyephem = self.pyephem + 1
		
		available_pyorbital = available.pyorbital
		if available_pyorbital == 'yes':
			self.pyorbital = self.pyorbital + 1

		self.index = self.index + 1

		self.a.clear()
		self.b.clear()
		self.c.clear()

		figure = output_data.Read_data(self.pyephem, self.predict, self.pyorbital)
		difference_alt, difference_az = figure.pyephem_minus_predict()

		figure_predict = output_data.Read_predict_data(self.predict)
		figure_pyephem = output_data.Read_pyephem_data(self.pyephem)
		figure_pyorbital = output_data.Read_pyorbital_data(self.pyorbital)

		time = figure_pyephem.pyephem_simulation_time

		available = output_data.Check_data(self.index)
		available_predict = available.predict
		available_pyephem = available.pyephem
		available_pyorbital = available.pyorbital

                import get_elements
                object_name = get_elements.Get_name(self.index)
		
		self.f.clf()
                self.f.suptitle(object_name.name, fontsize=16)

		# Subplot a
                self.a = self.f.add_subplot(211)
		if available_predict == 'yes':
			predict_alt = figure_predict.predict_alt_satellite
			self.a.plot(time, predict_alt, 'r', label="predict")
		if available_pyephem == 'yes':
			pyephem_alt = figure_pyephem.pyephem_alt_satellite
			self.a.plot(time, pyephem_alt, 'b', label="PyEphem")
		if available_pyorbital == 'yes':
			pyorbital_alt = figure_pyorbital.pyorbital_alt_satellite
			self.a.plot(time, pyorbital_alt, 'y', label="pyorbital")

                self.a.legend(loc = 2, borderaxespad = 0., prop={'size':12})

                self.a.set_ylabel("Degrees")

		self.a.grid(True)

		# Subplot c
                self.c = self.g.add_subplot(111)
		self.c.plot(time, difference_alt, label = "Difference")

                self.c.legend(loc = 2, borderaxespad = 0., prop={'size':12})

		self.c.set_ylabel("Altitude - Degrees")

		self.c.grid(True)

		# Subplot c
		self.b = self.f.add_subplot(212)
		if available_predict == 'yes':
			predict_az = figure_predict.predict_az_satellite
			self.b.plot(time, predict_az, 'r', label="predict")
		if available_pyephem == 'yes':
			pyephem_az = figure_pyephem.pyephem_az_satellite
			self.b.plot(time, pyephem_az, 'b', label="PyEphem")
		if available_pyorbital == 'yes':
			pyorbital_az = figure_pyorbital.pyorbital_az_satellite
			self.b.plot(time, pyorbital_az, 'y', label="pyorbital")

                self.b.legend(loc = 2, borderaxespad = 0., prop={'size':12})

                self.b.set_ylabel("Degrees")

		self.b.grid(True)
		
		self.canvas.draw()

		# Check buttons state
                if self.index == 0:
                        self.forward.configure(state = tk.DISABLED)
			self.next.configure(state = tk.NORMAL)
                elif self.index == self.length:
			self.forward.configure(state = tk.NORMAL)
                        self.next.configure(state = tk.DISABLED)
                else:
                        self.forward.configure(state = tk.NORMAL)
			self.next.configure(state = tk.NORMAL)		

	def forward(self):

		import output_data
		available = output_data.Check_data(self.index) 		

		available_predict = available.predict
		if available_predict == 'yes':
			self.predict = self.predict - 1
		
		available_pyephem = available.pyephem
		if available_pyephem == 'yes':
			self.pyephem = self.pyephem - 1
		
		available_pyorbital = available.pyorbital
		if available_pyorbital == 'yes':
			self.pyorbital = self.pyorbital - 1

		self.index = self.index - 1

                self.a.clear()
                self.b.clear()
		self.c.clear()

                import output_data
		figure = output_data.Read_data(self.pyephem, self.predict, self.pyorbital)
		difference_alt, difference_az = figure.pyephem_minus_predict()

		figure_predict = output_data.Read_predict_data(self.predict)
		figure_pyephem = output_data.Read_pyephem_data(self.pyephem)
		figure_pyorbital = output_data.Read_pyorbital_data(self.pyorbital)

		time = figure_pyephem.pyephem_simulation_time

		available = output_data.Check_data(self.index)
		available_predict = available.predict
		available_pyephem = available.pyephem
		available_pyorbital = available.pyorbital

                import get_elements
                object_name = get_elements.Get_name(self.index)

                self.f.clf()
                self.f.suptitle(object_name.name, fontsize=16)

		# Subplot a
                self.a = self.f.add_subplot(211)
		if available_predict == 'yes':
			predict_alt = figure_predict.predict_alt_satellite
			self.a.plot(time, predict_alt, 'r', label="predict")
		if available_pyephem == 'yes':
			pyephem_alt = figure_pyephem.pyephem_alt_satellite
			self.a.plot(time, pyephem_alt, 'b', label="PyEphem")
		if available_pyorbital == 'yes':
			pyorbital_alt = figure_pyorbital.pyorbital_alt_satellite
			self.a.plot(time, pyorbital_alt, 'y', label="pyorbital")

                self.a.set_ylabel("Degrees")
                self.a.legend(loc = 2, borderaxespad = 0., prop={'size':12})

		self.a.grid(True)

		# Subplot b
		self.b = self.f.add_subplot(212)
		if available_predict == 'yes':
			predict_az = figure_predict.predict_az_satellite
			self.b.plot(time, predict_az, 'r', label="predict")
		if available_pyephem == 'yes':
			pyephem_az = figure_pyephem.pyephem_az_satellite
			self.b.plot(time, pyephem_az, 'b', label="PyEphem")
		if available_pyorbital == 'yes':
			pyorbital_az = figure_pyorbital.pyorbital_az_satellite
			self.b.plot(time, pyorbital_az, 'y', label="pyorbital")

                self.b.legend(loc = 2, borderaxespad = 0., prop={'size':12})

                self.b.set_ylabel("Degrees")

		self.b.grid(True)

                self.canvas.draw()

		# Subplot c
                self.c = self.f.add_subplot(111)
                self.c.plot(time, difference_alt, label = "Difference")
                self.c.legend(loc = 2, borderaxespad = 0., prop={'size':12})
                self.c.set_ylabel("Altitude - Degrees")

		self.c.grid(True)

		# Check buttons state
                if self.index == 0:
                        self.forward.configure(state = tk.DISABLED)
                        self.next.configure(state = tk.NORMAL)
                elif self.index == self.length:
                        self.forward.configure(state = tk.NORMAL)
                        self.next.configure(state = tk.DISABLED)
                else:
                        self.forward.configure(state = tk.NORMAL)
                        self.next.configure(state = tk.NORMAL)

	def sims_availables(self, available_predict, available_pyephem, available_pyorbital, available_orbitron, available_STK):
		list_of_simulations = [ ]		
		if available_STK == 'yes':
			if available_predict == 'yes':
				list_of_simulations.append("STK vs. predict")
			if available_pyephem == 'yes':
				list_of_simulations.append("STK vs. PyEphem")
			if available_pyorbital == 'yes':
				list_of_simulations.append("STK vs. PyOrbital")
			if available_orbitron == 'yes':
				list_of_simulations.append("STK vs. Orbitron")
		else:
			list_of_simulations.append("STK not available")
		self.list_of_simulations = list_of_simulations		

	def pick_simulation(self, index):
		print "hola"
		print index

	def _quit(self):
		root.quit()     # stops mainloop


if __name__ == '__main__':
	import Tkinter as tk
	root = tk.Tk()
	interfaz = GUI()
	root.title("Simulaciones")
	root.geometry("1010x620")
	root.resizable(0, 0)
	root.mainloop()
