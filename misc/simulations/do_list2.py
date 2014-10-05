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

                self.devuelve_valores()

        def devuelve_lista(self, x):
                return 3*x

        def devuelve_valores(self):
                return self.mostrar_lista_satelites
                return self.mostrar_lista_linea1
                return self.mostrar_lista_linea2


class Solve_coordinates:

        def __init__(self, lista_elementos, lista_prueba, lista_prueba2):

                self.satellites_number = len(lista_elementos)
		self.get_location()
		
                # Provide data to pyephem_routine
                for i in range(len(lista_elementos)):
			j = i + 1
			try:
                        	self.pyephem_routine(lista_elementos[i], lista_prueba[i], lista_prueba2[i], i)
                        except NotImplementedError:
				print "pyorbital - Simulation [%d/%d] error!" %(j, len(lista_elementos))
				print "Deep space satellite - Propagation not available"
			i = i + 1


        def pyephem_routine(self, satellite_name, line1, line2, i):

                import sys
                import pyorbital.orbital
		import datetime

                satellite = pyorbital.orbital.Orbital(satellite_name, line1 = line1, line2 = line2)

                start_time = int(sys.argv[2])
                end_time = int(sys.argv[3])

                iteraciones = end_time - start_time

                iteraciones = iteraciones - 1
		
		time1 = datetime.datetime.fromtimestamp(start_time)

		az1, alt1 = satellite.get_observer_look(time1, self.lon, self.lat, self.ele)

                self.output_data(satellite_name, start_time, alt1, az1)

		n2 = start_time

                for j in range(iteraciones):
                        import datetime
			n2 = n2 + 1
                        
			timeN = datetime.datetime.fromtimestamp(n2)
                        
			azN, altN = satellite.get_observer_look(timeN, self.lon, self.lat, self.ele)

                        self.output_data(satellite_name, n2, altN, azN)

                        j = j + 1


                i = i + 1

                print "pyorbital - Simulation [%s/%d] done!" %(i, self.satellites_number)


        def output_data(self, name, time, alt, az):

                import os

                directorio_script = os.getcwd()
                os.chdir(directorio_script + '/pyorbital')

                create_file = open(name, 'a')
                create_file.writelines("%d\t" % time)
                create_file.writelines("%0.6f\t" % alt)
                create_file.writelines("%0.6f\n" % az)
                create_file.close

                os.chdir(directorio_script)

	def get_location(self):
		self.lon = -8.712866
		self.lat = 42.241433
		self.ele = 0

if __name__ == '__main__':
	print ""
	print "pyorbit data"
	do_list = Do_list()

        solve_coordinates = Solve_coordinates(do_list.mostrar_lista_satelites, do_list.mostrar_lista_linea1, do_list.mostrar_lista_linea2)

