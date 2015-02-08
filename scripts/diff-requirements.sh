#!/bin/bash

for i in $( cat ../master/WebServices/requirements.txt )
do
    lib=$( echo $i | cut -d'=' -f1)
    [[ -z $( cat requirements.txt | grep $lib ) ]] && echo "NOT: $lib"
done
