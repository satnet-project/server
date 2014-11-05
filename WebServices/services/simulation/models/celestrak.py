"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'rtubiopa@calpoly.edu'


class CelestrakDatabase(object):

    # Base URL
    CELESTRAK_URL_BASE = 'http://celestrak.com/NORAD/elements/'
    # Weather and Earth Resources
    CELESTRAK_SECTION_1 = 'Weather & Earth Resources'
    CELESTRAK_WEATHER = CELESTRAK_URL_BASE + 'weather.txt'
    CELESTRAK_NOAA = CELESTRAK_URL_BASE + 'noaa.txt'
    CELESTRAK_GOES = CELESTRAK_URL_BASE + 'goes.txt'
    CELESTRAK_EARTH_RESOURCES = CELESTRAK_URL_BASE + 'resource.txt'
    CELESTRAK_SARSAT = CELESTRAK_URL_BASE + 'sarsat.txt'
    CELESTRAK_DISASTER_MONITORING = CELESTRAK_URL_BASE + 'dmc.txt'
    CELESTRAK_TRACKING_DATA_RELAY = CELESTRAK_URL_BASE + 'tdrss.txt'
    CELESTRAK_ARGOS = CELESTRAK_URL_BASE + 'argos.txt'
    # Communications
    CELESTRAK_SECTION_2 = 'Communications'
    CELESTRAK_GEOSTATIONARY = CELESTRAK_URL_BASE + 'geo.txt'
    CELESTRAK_INTELSAT = CELESTRAK_URL_BASE + 'intelsat.txt'
    CELESTRAK_GORIZONT = CELESTRAK_URL_BASE + 'gorizont.txt'
    CELESTRAK_RADUGA = CELESTRAK_URL_BASE + 'raduga.txt'
    CELESTRAK_MOLNIYA = CELESTRAK_URL_BASE + 'molniya.txt'
    CELESTRAK_IRIDIUM = CELESTRAK_URL_BASE + 'iridium.txt'
    CELESTRAK_ORBCOMM = CELESTRAK_URL_BASE + 'orbcomm.txt'
    CELESTRAK_GLOBALSTAR = CELESTRAK_URL_BASE + 'globalstar.txt'
    CELESTRAK_AMATEUR_RADIO = CELESTRAK_URL_BASE + 'amateur.txt'
    CELESTRAK_EXPERIMENTAL = CELESTRAK_URL_BASE + 'x-comm.txt'
    CELESTRAK_COMMS_OTHER = CELESTRAK_URL_BASE + 'other-comm.txt'
    # Navigation
    CELESTRAK_SECTION_3 = 'Navigation'
    CELESTRAK_GPS_OPERATIONAL = CELESTRAK_URL_BASE + 'gps-ops.txt'
    CELESTRAK_GLONASS_OPERATIONAL = CELESTRAK_URL_BASE + 'glo-ops.txt'
    CELESTRAK_GALILEO = CELESTRAK_URL_BASE + 'galileo.txt'
    CELESTRAK_BEIDOU = CELESTRAK_URL_BASE + 'beidou.txt'
    CELESTRAK_SATELLITE_AUGMENTATION = CELESTRAK_URL_BASE + 'sbas.txt'
    CELESTRAK_NNSS = CELESTRAK_URL_BASE + 'nnss.txt'
    CELESTRAK_RUSSIAN_LEO_NAVIGATION = CELESTRAK_URL_BASE + 'musson.txt'
    # Scientific
    CELESTRAK_SECTION_4 = 'Scientific'
    CELESTRAK_SPACE_EARTH_SCIENCE = CELESTRAK_URL_BASE + 'science.txt'
    CELESTRAK_GEODETIC = CELESTRAK_URL_BASE + 'geodetic.txt'
    CELESTRAK_ENGINEERING = CELESTRAK_URL_BASE + 'engineering.txt'
    CELESTRAK_EDUCATION = CELESTRAK_URL_BASE + 'education.txt'
    # Miscellaneous
    CELESTRAK_SECTION_5 = 'Miscellaneous'
    CELESTRAK_MILITARY = CELESTRAK_URL_BASE + 'military.txt'
    CELESTRAK_RADAR_CALLIBRATION = CELESTRAK_URL_BASE + 'radar.txt'
    CELESTRAK_CUBESATS = CELESTRAK_URL_BASE + 'cubesat.txt'
    CELESTRAK_OTHER = CELESTRAK_URL_BASE + 'other.txt'

    # Decodes the name of a section into the position of that section within
    # the array of available sections for the CELESTRAK database.
    CELESTRAK_SECTION_2_POSITION = {
        CELESTRAK_SECTION_1: 0,
        CELESTRAK_SECTION_2: 1,
        CELESTRAK_SECTION_3: 2,
        CELESTRAK_SECTION_4: 3,
        CELESTRAK_SECTION_5: 4
    }

    # All choices for the TLE database sources.
    CELESTRAK_SECTIONS = (
        (
            CELESTRAK_SECTION_1, (
                (CELESTRAK_WEATHER, 'Weather Satellites'),
                (CELESTRAK_NOAA, 'NOAA Satellites'),
                (CELESTRAK_GOES, 'GOES Satellites'),
                (CELESTRAK_EARTH_RESOURCES, 'Earth Resources Satellites'),
                (CELESTRAK_SARSAT, 'SAR Satellites'),
                (CELESTRAK_DISASTER_MONITORING, 'Disaster Monitoring'),
                (CELESTRAK_TRACKING_DATA_RELAY, 'Tracking & Data Relay'),
                (CELESTRAK_ARGOS, 'ARGOS Constellation Satellites')
            )
        ),
        (
            CELESTRAK_SECTION_2, (
                (CELESTRAK_GEOSTATIONARY, 'Geostastionary Satellites'),
                (CELESTRAK_INTELSAT, 'Intelsat Satellites'),
                (CELESTRAK_GORIZONT, 'Gorizont Satellites'),
                (CELESTRAK_RADUGA, 'Raduga Satellites'),
                (CELESTRAK_MOLNIYA, 'Molniya Satellites'),
                (CELESTRAK_IRIDIUM, 'Iridum Constellation'),
                (CELESTRAK_ORBCOMM, 'Orbcomm Satellites'),
                (CELESTRAK_GLOBALSTAR, 'Globalstar Satellites'),
                (CELESTRAK_AMATEUR_RADIO, 'Amateur Radio Satellites'),
                (CELESTRAK_EXPERIMENTAL, 'Experimental Satellites'),
                (CELESTRAK_COMMS_OTHER, 'Other Communications Satellites')
            )
        ),
        (
            CELESTRAK_SECTION_3, (
                (CELESTRAK_GPS_OPERATIONAL, 'GPS Operational Satellites'),
                (CELESTRAK_GLONASS_OPERATIONAL, 'Glonass Satellites'),
                (CELESTRAK_GALILEO, 'Galileo Satellites'),
                (CELESTRAK_BEIDOU, 'Beidou Satellites'),
                (CELESTRAK_SATELLITE_AUGMENTATION, 'EGNOS Satellites'),
                (CELESTRAK_NNSS, 'NNSS Satellites'),
                (CELESTRAK_RUSSIAN_LEO_NAVIGATION, 'Russian LEO Navigation')
            )
        ),
        (
            CELESTRAK_SECTION_4, (
                (CELESTRAK_SPACE_EARTH_SCIENCE, 'Space and Earth Science'),
                (CELESTRAK_GEODETIC, 'Geodetic Satellites'),
                (CELESTRAK_ENGINEERING, 'Engineering Satellites'),
                (CELESTRAK_EDUCATION, 'Educational Satellites')
            )
        ),
        (
            CELESTRAK_SECTION_5, (
                (CELESTRAK_MILITARY, 'Military Satellites'),
                (CELESTRAK_RADAR_CALLIBRATION, 'Radar Callibration'),
                (CELESTRAK_CUBESATS, 'CubeSats'),
                (CELESTRAK_OTHER, 'OTher Miscellaneous Satellites')
            )
        )
    )