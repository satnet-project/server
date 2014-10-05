#!/bin/bash

FILE=$1
FAMILY=$2
START_TIME=$3
END_TIME=$4

END_TIME=`expr $END_TIME - 1`


# Obtener el numero total de lineas
lines=`wc $FILE | awk {'print $1'}`

# Dividirlas entre tres
sats_number=`expr $lines / 3`


declare -i LIMIT=`expr $sats_number + 1`
declare -i n1=1
declare -i j1=1
IDEN=SAT

# Script que cambia los nombres de los archivos.
until [ $n1 -eq $LIMIT ]
do
	export FAMILY
	export n1
	export j1
	export IDEN

	perl -pi -e 's/.*/$ENV{IDEN}$ENV{n1}/ if $. == $ENV{j1}' $FILE

        j1=$[$n1 * 3]
        j1=$[$j1 + 1]
        n1=$[$n1 + 1]
done	

declare -i k=0
declare -i n=0
declare -i l=-1
declare -i j=0
#declare -i LIMIT2=`expr $sats_number + 1`

until [ $n -eq $sats_number ]
do

	l=$[$l + 1]
	j=$[$l * 3]
	j=$[$j + 1]

	cd TLEs

        # Divide el archivo de la familia en archivos de 24 satelites cada uno
        split -l 72 $FILE

        # Cuenta los archivos disponibles con ese nombre
        FILES_SPLITED="`ls x* | wc -l`"

	# Crea una lista para los nombres de los archivos
        declare -a LIST_FILES_SPLITED
        LIST_FILES_SPLITED=(`ls x*`)

	# Export both vars for Perl script
	export j
	export FAMILY
	export n

	SATELLITE="`awk 'NR==j2' j2="${j}" ${LIST_FILES_SPLITED[k]}`"
	FILESPLITTED="${LIST_FILES_SPLITED[k]}"

	predict -t $FILESPLITTED -f $SATELLITE $START_TIME $END_TIME -o ~/predict/$SATELLITE

	cd ..

	m=$[$n + 1]

	echo -e "Predict - Simulation [$m/$sats_number] done!"

        n=$[$n + 1]

	if [ $l -eq 23 ]; then
		l=-1
		k=$[$k + 1]
	fi

 
done
