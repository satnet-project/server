#sys.argv[1] = FAMILY

class Read_orbitron_data:

	def __init__(self, index_satellite):

		import os

		index_satellite = index_satellite + 1
		directorio_script = os.getcwd()
		file = '/home/case/Orbitron/Output/output.txt'
		
		# Orbitron routine
		self.open_file_orbitron(index_satellite, file)

		os.chdir(directorio_script)

	def open_file_orbitron(self, index_satellite, file):

		open_file = open(file, 'r')
		file_lines = open_file.readlines()

		file_lines_converted = []

		for i in range(len(file_lines)):
			file_lines_converted.append(file_lines[i].rstrip('\r\n'))

		self.lineas_validas = []
		for i in range(len(file_lines_converted)):
			self.extract_data(file_lines_converted[i])

#		self.process_data()


	def extract_data(self, line):

		# Si la linea empieza por 2014 se agrega, si no, no.
		if line[0:4] == '2014':
			self.lineas_validas.append(line)


#	def process_data(self):

#		print self.lineas_validas

class Read_STK_data:

	def __init__(self, index_satellite):

		import os

		index_satellite = index_satellite + 1
		directorio_script = os.getcwd()
		directorio_datos = '/media/windows7share'
		
		# STK routine
		self.open_STK(directorio_datos)
		self.open_files_STK(index_satellite)

		os.chdir(directorio_script)

	def open_STK(self, directorio_datos):

		import os

		# PyEphem data
                os.chdir(directorio_datos)

		self.files_STK = os.listdir(os.getcwd())
		self.files_STK.sort()

	def open_files_STK(self, index_satellite):

		# Deberia abrir el fichero que le pidamos
		for i in range(index_satellite):
			self.open_file_STK(self.files_STK[i])

	def open_file_STK(self, name):
	
		self.STK_simulation_time = []
		self.STK_alt_satellite = []
		self.STK_az_satellite = []
		
		import csv

		print "El nombre del fichero es"
		print name

		with open(name, 'rb') as open_file:
			reader = csv.reader(open_file)
			for row in reader:
				# Tengo que comprobar si la linea esta vacia
				valor = int((float(row[0]) - 2440587.5)*86400)
				self.STK_simulation_time.append(valor)
				self.STK_az_satellite.append((row[1]))
				self.STK_alt_satellite.append((row[2]))

class Read_pyephem_data:

	def __init__(self, index_satellite):

		import os

		index_satellite = index_satellite + 1
		directorio_script = os.getcwd()
		
		# Pyephem routine
		self.open_pyephem(directorio_script)
		self.open_files_pyephem(index_satellite)

		os.chdir(directorio_script)

	def open_pyephem(self, directorio_script):

		import os

		# PyEphem data
                os.chdir(directorio_script + '/PyEphem')

		self.files_pyephem = os.listdir(os.getcwd())
		self.files_pyephem.remove('temp')
		self.files_pyephem.sort()

	def open_files_pyephem(self, index_satellite):

		for i in range(index_satellite):
			self.open_file_pyephem(self.files_pyephem[i])
			self.satellite_name = self.files_pyephem[i]

	def open_file_pyephem(self, name):
	
		self.pyephem_simulation_time = []
		self.pyephem_alt_satellite = []
		self.pyephem_az_satellite = []
		
		import csv

		with open(name) as tsv:
			for line in csv.reader(tsv, delimiter = "\t"):
				self.pyephem_simulation_time.append(int(line[0]))
				self.pyephem_alt_satellite.append(float(line[1]))
				self.pyephem_az_satellite.append(float(line[2]))


class Read_predict_data:

	def __init__(self, index_satellite):

		import os

		index_satellite = index_satellite + 1
		directorio_script = os.getcwd()

		# predict routine
		self.open_predict(directorio_script)
		self.open_files_predict(index_satellite)

		os.chdir(directorio_script)

	def open_predict(self, directorio_script):

		import os

		os.chdir(directorio_script + '/predict')

		self.files_predict = os.listdir(os.getcwd())
		self.files_predict.remove('temp')
		self.files_predict.sort()
	
	def open_files_predict(self, index_satellite):

		for i in range(index_satellite):
			self.open_file_predict(self.files_predict[i])

	def open_file_predict(self, name):

		self.predict_simulation_time = []
		self.predict_alt_satellite = []
		self.predict_az_satellite = []

		import csv

		with open(name) as tsv:
			for line in csv.reader(tsv, delimiter = "\t"):
				self.predict_simulation_time.append(line[0])
				self.predict_alt_satellite.append(float(line[1]))
				self.predict_az_satellite.append(float(line[2]))


class Read_pyorbital_data:

	def __init__(self, index_satellite):

		import os

		index_satellite = index_satellite + 1
		directorio_script = os.getcwd()

		# pyorbital routine
		self.open_pyorbital(directorio_script, index_satellite)

		os.chdir(directorio_script)

        def open_pyorbital(self, directorio_script, index_satellite):

                import os

                # pyorbital data
                os.chdir(directorio_script + '/pyorbital')
		
                self.files_pyorbital = os.listdir(os.getcwd())
		self.files_pyorbital.remove('temp')
		self.files_pyorbital.sort()

		if not self.files_pyorbital:
			print "PyOrbital hasn't data available!"
		else:
			self.open_files_pyorbital(index_satellite)

        def open_files_pyorbital(self, index_satellite):

                for i in range(index_satellite):
                        self.open_file_pyorbital(self.files_pyorbital[i])

        def open_file_pyorbital(self, name):

                self.pyorbital_simulation_time = []
                self.pyorbital_alt_satellite = []
                self.pyorbital_az_satellite = []

                import csv

                with open(name) as tsv:
                        for line in csv.reader(tsv, delimiter = "\t"):
                                self.pyorbital_simulation_time.append(line[0])
                                self.pyorbital_alt_satellite.append(float(line[1]))
                                self.pyorbital_az_satellite.append(float(line[2]))


class Read_data:

	def __init__(self, index_pyephem, index_predict, index_pyorbital):

		import os

		self.index_pyephem = index_pyephem + 1
		self.index_predict = index_predict + 1
		self.index_pyorbital = index_pyorbital + 1

		self.directorio_script = os.getcwd()
	
	def pyephem_minus_predict(self):

		import os

		# Pyephem routine
		self.open_pyephem()
		self.open_files_pyephem()

		# predict routine
		self.open_predict()
		self.open_files_predict()

		difference_alt = []
		difference_az = []

		for i in range(len(self.predict_simulation_time)):
			resta_alt = float(self.predict_alt_satellite[i]) - float(self.pyephem_alt_satellite[i])
			difference_alt.append(resta_alt)

			resta_az = float(self.predict_az_satellite[i]) - float(self.pyephem_az_satellite[i])
			difference_az.append(resta_az)

		os.chdir(self.directorio_script)

		return (difference_alt, difference_az)

	def pyephem_minus_pyorbital(self):

		# pyorbital routine
		self.open_pyorbital()

	def predict_minus_pyorbital(self):

		print "1"

	def predict_minus_pyephem(self):

		print "2"

	def pyorbital_minus_pyephem(self):

		print "3"

	def pyorbital_minus_predict(self):

		print "4"

	def open_pyephem(self):

		import os

		# PyEphem data
                os.chdir(self.directorio_script + '/PyEphem')

		directorio_actual = os.getcwd()

		self.files_pyephem = os.listdir(directorio_actual)
		self.files_pyephem.remove('temp')
		self.files_pyephem.sort()
	
	def open_files_pyephem(self):

		for i in range(self.index_pyephem):
			self.open_file_pyephem(self.files_pyephem[i])
			self.satellite_name = self.files_pyephem[i]

	def open_predict(self):

		import os

		# predict data
		os.chdir(self.directorio_script + '/predict')

		directorio_actual = os.getcwd()

		self.files_predict = os.listdir(directorio_actual)
		self.files_predict.remove('temp')
		self.files_predict.sort()
	

	def open_files_predict(self):

		for i in range(self.index_predict):
			self.open_file_predict(self.files_predict[i])

        def open_pyorbital(self):

                import os

                # pyorbital data
                os.chdir(self.directorio_script + '/pyorbital')

                directorio_actual = os.getcwd()
		
                self.files_pyorbital = os.listdir(directorio_actual)
		self.files_pyorbital.remove('temp')
		self.files_pyorbital.sort()

		if not self.files_pyorbital:
			print "lista vacia"
		else:
			self.open_files_pyorbital()

        def open_files_pyorbital(self):

                for i in range(self.index_satellite):
                        self.open_file_pyorbital(self.files_pyorbital[i])

	def open_file_pyephem(self, name):
	
		self.pyephem_simulation_time = []
		self.pyephem_alt_satellite = []
		self.pyephem_az_satellite = []
		
		import csv

		with open(name) as tsv:
			for line in csv.reader(tsv, delimiter = "\t"):
				self.pyephem_simulation_time.append(int(line[0]))
				self.pyephem_alt_satellite.append(float(line[1]))
				self.pyephem_az_satellite.append(float(line[2]))


	def open_file_predict(self, name):

		self.predict_simulation_time = []
		self.predict_alt_satellite = []
		self.predict_az_satellite = []

		import csv

		with open(name) as tsv:
			for line in csv.reader(tsv, delimiter = "\t"):
#				import datetime	
#				date = datetime.datetime.fromtimestamp(int(line[0])).strftime('%Y-%m-%d %H:%M:%S')
				self.predict_simulation_time.append(line[0])
				self.predict_alt_satellite.append(float(line[1]))
				self.predict_az_satellite.append(float(line[2]))

        def open_file_pyorbital(self, name):

                self.pyorbital_simulation_time = []
                self.pyorbital_alt_satellite = []
                self.pyorbital_az_satellite = []

                import csv

                with open(name) as tsv:
                        for line in csv.reader(tsv, delimiter = "\t"):
                                self.pyorbital_simulation_time.append(line[0])
                                self.pyorbital_alt_satellite.append(float(line[1]))
                                self.pyorbital_az_satellite.append(float(line[2]))

#		minimo = min(enumerate(self.predict_alt_satellite), key=lambda x: abs(x[1]-0))

class Check_data:

	def __init__(self, index_satellite):

		index = index_satellite + 1
		satellite_name = "SAT%s" %(index)

		import os
		self.directorio_actual = os.getcwd()

		self.check_predict(index_satellite, satellite_name)
		self.check_pyephem(index_satellite, satellite_name)
		self.check_pyorbital(index_satellite, satellite_name)

                os.chdir(self.directorio_actual)

	def check_predict(self, index, satellite_name):

		import os
		os.chdir(self.directorio_actual + '/predict')
		
		files = os.listdir(os.getcwd())

		if satellite_name in files:
			self.predict = 'yes'
		else:
			self.predict = 'no'

	def check_pyephem(self, index, satellite_name):

                import os
                os.chdir(self.directorio_actual + '/PyEphem')

                files = os.listdir(os.getcwd())

                if satellite_name in files:
                        self.pyephem = 'yes'
                else:
                        self.pyephem = 'no'

	def check_pyorbital(self, index, satellite_name):

                import os
                os.chdir(self.directorio_actual + '/pyorbital')

                files = os.listdir(os.getcwd())

		if satellite_name in files:
			self.pyorbital = 'yes'
		else:
			self.pyorbital = 'no'
