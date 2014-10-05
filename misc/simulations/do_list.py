# Python
# sys.argv[1] = FILE
# sys.argv[2] = REFRACTION
# sys.argv[3] = START_TIME
# sys.argv[4] = END_TIME



class Do_list:

	def __init__(self):

		import sys

		abrir_tle = open(sys.argv[1], 'r')
		lista_nombres_satelites = abrir_tle.readlines()
		lista_nombres_satelites = [item.rstrip('\n') for item in lista_nombres_satelites]

		tamano_lista = len(lista_nombres_satelites)
		y = tamano_lista/3

		numeros_lista = map(self.devuelve_lista, range(y))
		
		self.mostrar_lista_satelites = []
		self.mostrar_lista_linea1 = []
		self.mostrar_lista_linea2 = []
		i = 0
		j = 1
		k = 2

		for i in range(len(numeros_lista)):
			self.mostrar_lista_satelites.append(lista_nombres_satelites[numeros_lista[i]])
			self.mostrar_lista_linea1.append(lista_nombres_satelites[j])
			self.mostrar_lista_linea2.append(lista_nombres_satelites[k])
			j = numeros_lista[i] + 4
			k = numeros_lista[i] + 5				
			
		# Funcion para sacar los valores de la clase
		self.devuelve_valores()

	def devuelve_lista(self, x):
		return 3*x

	def devuelve_valores(self):
		return self.mostrar_lista_satelites
		return self.mostrar_lista_linea1
		return self.mostrar_lista_linea2

class Solve_coordinates:

	def __init__(self, lista_elementos, lista_prueba, lista_prueba2):
	
		import ephem
		import sys
		import os

		self.satellites_number = len(lista_elementos)

		self.observer = ephem.Observer()
		self.get_location()

		self.observer.lon = ephem.degrees(self.lon)
		self.observer.lat = ephem.degrees(self.lat)
		self.observer.elevation = self.ele

		self.observer.date = ephem.now()
		self.observer.epoch = ephem.now() 

		self.observer.horizon = '0'


		# Provide data to pyephem_routine
		for i in range(len(lista_elementos)):
			self.pyephem_routine(lista_elementos[i], lista_prueba[i], lista_prueba2[i], i)
			i = i + 1
		

	def pyephem_routine(self, satellite_name, line1, line2, i):

		import sys
		import ephem
		import math
	
		satellite = ephem.readtle(satellite_name, line1, line2)
		satellite.compute(self.observer)

		start_time = int(sys.argv[2])
		end_time = int(sys.argv[3])

		iteraciones = end_time - start_time

		iteraciones = iteraciones - 1

		n1 = (start_time + 2440587.5*86400)/86400 - 2415020

		self.observer.date = n1

		satellite.compute(self.observer)
		alt1 = float(repr(satellite.alt))
		alt1 = math.degrees(alt1)
		az1 = float(repr(satellite.az))
		az1 = math.degrees(az1)

		self.output_data(satellite_name, start_time, alt1, az1)

		for j in range(iteraciones):
			time = ephem.Date(self.observer.date + ephem.second)
			self.observer.date = time
			# UNIX Time
			UnixTimeN = float(time)


			UnixTimeN = int((UnixTimeN - 25567.5)*86400)

			satellite.compute(self.observer)
			altN = float(repr(satellite.alt))
			altN = math.degrees(altN)
			azN = float(repr(satellite.az))
			azN = math.degrees(azN)
			self.output_data(satellite_name, UnixTimeN, altN, azN)

			j = j + 1


                i = i + 1

                print "PyEphem - Simulation [%s/%d] done!" %(i, self.satellites_number)


	def output_data(self, name, time, alt, az):

		import os

                directorio_script = os.getcwd()
                os.chdir(directorio_script + '/PyEphem')

		create_file = open(name, 'a')
		create_file.writelines("%d\t" % time)
		create_file.writelines("%0.6f\t" % alt)
		create_file.writelines("%0.6f\n" % az)
		create_file.close

		os.chdir(directorio_script)

	def get_location(self):
		# Implementar una llamada al fichero de configuracion de predict
		self.lon = '-8.712866' 
		self.lat = '42.241433'
		self.ele = 0

if __name__ == '__main__':
	print ""
	print "PyEphem data"
	do_list = Do_list()

	# Time will be in UNIX units

	solve_coordinates = Solve_coordinates(do_list.mostrar_lista_satelites, do_list.mostrar_lista_linea1, do_list.mostrar_lista_linea2)


