#!/bin/bash

# TO-DO Mejorar la gestion de errores

echo "Descarga de los elementos orbitales"

rm ~/TLEs/*

wget -qr www.celestrak.com/NORAD/elements/amateur.txt -O ~/TLEs/amateur.txt
echo "amateur.txt updated!     [1/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/beidou.txt -O ~/TLEs/beidou.txt
echo "beidou.txt updated!      [2/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/cubesat.txt -O ~/TLEs/cubesat.txt
echo "cubesat.txt updated!     [3/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/dmc.txt -O ~/TLEs/dmc.txt
echo "dmc.txt updated!         [4/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/education.txt -O ~/TLEs/education.txt
echo "education.txt updated!   [5/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/engineering.txt -O ~/TLEs/engineering.txt
echo "engineering.txt updated! [6/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/galileo.txt -O ~/TLEs/galileo.txt
echo "galileo.txt updated!     [7/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/geo.txt -O ~/TLEs/geo.txt
echo "geo.txt updated!         [8/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/geodetic.txt -O ~/TLEs/geodetic.txt
echo "geodetic.txt updated!    [9/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/glo-ops.txt -O ~/TLEs/glo-ops.txt
echo "glo-ops.txt updated!    [10/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/globalstar.txt -O ~/TLEs/globalstar.txt
echo "globalstar.txt updated! [11/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/gorizont.txt -O ~/TLEs/gorizont.txt
echo "gorizont.txt updated!   [12/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/gps-ops.txt -O ~/TLEs/gps-ops.txt
echo "gps-ops.txt updated!    [13/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/intelsat.txt -O ~/TLEs/intelsat.txt
echo "intelsat.txt updated!   [14/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/iridium.txt -O ~/TLEs/iridium.txt
echo "iridium.txt updated!    [15/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/military.txt -O ~/TLEs/military.txt
echo "military.txt updated!   [16/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/molniya.txt -O ~/TLEs/molniya.txt
echo "molniya.txt updated!    [17/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/musson.txt -O ~/TLEs/musson.txt
echo "musson.txt updated!     [18/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/nnss.txt -O ~/TLEs/nnss.txt
echo "nnss.txt updated!       [19/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/noaa.txt -O ~/TLEs/noaa.txt
echo "noaa.txt updated!       [20/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/orbcomm.txt -O ~/TLEs/orbcomm.txt
echo "orbcomm.txt updated!    [21/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/other-comm.txt -O ~/TLEs/other-comm.txt
echo "other-comm.txt updated! [22/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/radar.txt -O ~/TLEs/radar.txt
echo "radar.txt updated!      [23/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/raduga.txt -O ~/TLEs/raduga.txt
echo "raduga.txt updated!     [24/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/resource.txt -O ~/TLEs/resource.txt
echo "resource.txt updated!   [25/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/sarsat.txt -O ~/TLEs/sarsat.txt
echo "sarsat.txt updated!     [26/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/sbas.txt -O ~/TLEs/sbas.txt
echo "sbas.txt updated!       [27/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/science.txt -O ~/TLEs/science.txt
echo "science.txt updated!    [28/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/tdrss.txt -O ~/TLEs/tdrss.txt
echo "tdrss.txt updated!      [29/30]"
sleep 0.3

wget -qr www.celestrak.com/NORAD/elements/x-comm.txt -O ~/TLEs/x-comm.txt
echo -e "x-comm.txt updated!     [30/30]\n"
sleep 0.3
