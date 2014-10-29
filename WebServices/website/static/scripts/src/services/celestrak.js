/**
 * Copyright 2014 Ricardo Tubio-Pardavila
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Created by rtubio on 10/24/14.
 */

// Base URL
var __CELESTRAK_URL_BASE = 'http://celestrak.com/NORAD/elements/';
// Weather and Earth Resources
var __CELESTRAK_SECTION_1 = 'Weather & Earth Resources';
var __CELESTRAK_WEATHER = __CELESTRAK_URL_BASE + 'weather.txt';
var __CELESTRAK_NOAA = __CELESTRAK_URL_BASE + 'noaa.txt';
var __CELESTRAK_GOES = __CELESTRAK_URL_BASE + 'goes.txt';
var __CELESTRAK_EARTH_RESOURCES = __CELESTRAK_URL_BASE + 'resource.txt';
var __CELESTRAK_SARSAT = __CELESTRAK_URL_BASE + 'sarsat.txt';
var __CELESTRAK_DISASTER_MONITORING = __CELESTRAK_URL_BASE + 'dmc.txt';
var __CELESTRAK_TRACKING_DATA_RELAY = __CELESTRAK_URL_BASE + 'tdrss.txt';
var __CELESTRAK_ARGOS = __CELESTRAK_URL_BASE + 'argos.txt';
// Communications
var __CELESTRAK_SECTION_2 = 'Communications';
var __CELESTRAK_GEOSTATIONARY = __CELESTRAK_URL_BASE + 'geo.txt';
var __CELESTRAK_INTELSAT = __CELESTRAK_URL_BASE + 'intelsat.txt';
var __CELESTRAK_GORIZONT = __CELESTRAK_URL_BASE + 'gorizont.txt';
var __CELESTRAK_RADUGA = __CELESTRAK_URL_BASE + 'raduga.txt';
var __CELESTRAK_MOLNIYA = __CELESTRAK_URL_BASE + 'molniya.txt';
var __CELESTRAK_IRIDIUM = __CELESTRAK_URL_BASE + 'iridium.txt';
var __CELESTRAK_ORBCOMM = __CELESTRAK_URL_BASE + 'orbcomm.txt';
var __CELESTRAK_GLOBALSTAR = __CELESTRAK_URL_BASE + 'globalstar.txt';
var __CELESTRAK_AMATEUR_RADIO = __CELESTRAK_URL_BASE + 'amateur.txt';
var __CELESTRAK_EXPERIMENTAL = __CELESTRAK_URL_BASE + 'x-comm.txt';
var __CELESTRAK_COMMS_OTHER = __CELESTRAK_URL_BASE + 'other-comm.txt';
// Navigation
var __CELESTRAK_SECTION_3 = 'Navigation';
var __CELESTRAK_GPS_OPERATIONAL = __CELESTRAK_URL_BASE + 'gps-ops.txt';
var __CELESTRAK_GLONASS_OPERATIONAL = __CELESTRAK_URL_BASE + 'glo-ops.txt';
var __CELESTRAK_GALILEO = __CELESTRAK_URL_BASE + 'galileo.txt';
var __CELESTRAK_BEIDOU = __CELESTRAK_URL_BASE + 'beidou.txt';
var __CELESTRAK_SATELLITE_AUGMENTATION = __CELESTRAK_URL_BASE + 'sbas.txt';
var __CELESTRAK_NNSS = __CELESTRAK_URL_BASE + 'nnss.txt';
var __CELESTRAK_RUSSIAN_LEO_NAVIGATION = __CELESTRAK_URL_BASE + 'musson.txt';
// Scientific
var __CELESTRAK_SECTION_4 = 'Scientific';
var __CELESTRAK_SPACE_EARTH_SCIENCE = __CELESTRAK_URL_BASE + 'science.txt';
var __CELESTRAK_GEODETIC = __CELESTRAK_URL_BASE + 'geodetic.txt';
var __CELESTRAK_ENGINEERING = __CELESTRAK_URL_BASE + 'engineering.txt';
var __CELESTRAK_EDUCATION = __CELESTRAK_URL_BASE + 'education.txt';
// Miscellaneous
var __CELESTRAK_SECTION_5 = 'Miscellaneous';
var __CELESTRAK_MILITARY = __CELESTRAK_URL_BASE + 'military.txt';
var __CELESTRAK_RADAR_CALLIBRATION = __CELESTRAK_URL_BASE + 'radar.txt';
var __CELESTRAK_CUBESATS = __CELESTRAK_URL_BASE + 'cubesat.txt';
var __CELESTRAK_OTHER = __CELESTRAK_URL_BASE + 'other.txt';
// CELESTRAK resources within a structured data type...
var __CELESTRAK_RESOURCES = {
    'Weather': __CELESTRAK_WEATHER,
    'NOAA': __CELESTRAK_NOAA,
    'GOES': __CELESTRAK_GOES,
    'Earth Resources': __CELESTRAK_EARTH_RESOURCES,
    'SARSAT': __CELESTRAK_SARSAT,
    'Disaster Monitoring': __CELESTRAK_DISASTER_MONITORING,
    'Tracking & Data Relay': __CELESTRAK_TRACKING_DATA_RELAY,
    'ARGOS': __CELESTRAK_ARGOS,
    'Geostationary': __CELESTRAK_GEOSTATIONARY,
    'Intelsat': __CELESTRAK_INTELSAT,
    'Gorizont': __CELESTRAK_GORIZONT,
    'Raduga': __CELESTRAK_RADUGA,
    'Molniya': __CELESTRAK_MOLNIYA,
    'Iridium': __CELESTRAK_IRIDIUM,
    'Orbcomm': __CELESTRAK_ORBCOMM,
    'Globalstar': __CELESTRAK_GLOBALSTAR,
    'Amateur Radio': __CELESTRAK_AMATEUR_RADIO,
    'Experimental': __CELESTRAK_EXPERIMENTAL,
    'Others': __CELESTRAK_COMMS_OTHER,
    'GPS Operational': __CELESTRAK_GPS_OPERATIONAL,
    'Glonass Operational': __CELESTRAK_GLONASS_OPERATIONAL,
    'Galileo': __CELESTRAK_GALILEO,
    'Beidou': __CELESTRAK_BEIDOU,
    'Satellite-based Augmentation System': __CELESTRAK_SATELLITE_AUGMENTATION,
    'Navy Navigation Satellite System': __CELESTRAK_NNSS,
    'Russian LEO Navigation': __CELESTRAK_RUSSIAN_LEO_NAVIGATION,
    'Space & Earth Science': __CELESTRAK_SPACE_EARTH_SCIENCE,
    'Geodetic': __CELESTRAK_GEODETIC,
    'Engineering': __CELESTRAK_ENGINEERING,
    'Education': __CELESTRAK_EDUCATION,
    'Military': __CELESTRAK_MILITARY,
    'Radar Callibration': __CELESTRAK_RADAR_CALLIBRATION,
    'CubeSats': __CELESTRAK_CUBESATS,
    'Other': __CELESTRAK_OTHER
};

var __CELESTRAK_SELECT_SECTIONS = [
    /////////////////////////////////////////////////////////////////  SECTION 1
    { 'section': __CELESTRAK_SECTION_1, 'subsection': 'Weather' },
    { 'section': __CELESTRAK_SECTION_1, 'subsection': 'NOAA' },
    { 'section': __CELESTRAK_SECTION_1, 'subsection': 'GOES' },
    { 'section': __CELESTRAK_SECTION_1, 'subsection': 'Earth Resources' },
    { 'section': __CELESTRAK_SECTION_1, 'subsection': 'SARSAT' },
    { 'section': __CELESTRAK_SECTION_1, 'subsection': 'Disaster Monitoring' },
    { 'section': __CELESTRAK_SECTION_1, 'subsection': 'Tracking & Data Relay' },
    { 'section': __CELESTRAK_SECTION_1, 'subsection': 'ARGOS' },
    /////////////////////////////////////////////////////////////////  SECTION 2
    { 'section': __CELESTRAK_SECTION_2, 'subsection': 'Geostationary' },
    { 'section': __CELESTRAK_SECTION_2, 'subsection': 'Intelsat' },
    { 'section': __CELESTRAK_SECTION_2, 'subsection': 'Gorizont' },
    { 'section': __CELESTRAK_SECTION_2, 'subsection': 'Raduga' },
    { 'section': __CELESTRAK_SECTION_2, 'subsection': 'Molniya' },
    { 'section': __CELESTRAK_SECTION_2, 'subsection': 'Iridium' },
    { 'section': __CELESTRAK_SECTION_2, 'subsection': 'Orbcomm' },
    { 'section': __CELESTRAK_SECTION_2, 'subsection': 'Globalstar' },
    { 'section': __CELESTRAK_SECTION_2, 'subsection': 'Amateur Radio' },
    { 'section': __CELESTRAK_SECTION_2, 'subsection': 'Experimental' },
    { 'section': __CELESTRAK_SECTION_2, 'subsection': 'Others' },
    /////////////////////////////////////////////////////////////////  SECTION 3
    { 'section': __CELESTRAK_SECTION_3, 'subsection': 'GPS Operational' },
    { 'section': __CELESTRAK_SECTION_3, 'subsection': 'Glonass Operational' },
    { 'section': __CELESTRAK_SECTION_3, 'subsection': 'Galileo' },
    { 'section': __CELESTRAK_SECTION_3, 'subsection': 'Beidou' },
    { 'section': __CELESTRAK_SECTION_3, 'subsection': 'Satellite-based Augmentation System' },
    { 'section': __CELESTRAK_SECTION_3, 'subsection': 'Navy Navigation Satellite System' },
    { 'section': __CELESTRAK_SECTION_3, 'subsection': 'Russian LEO Navigation' },
    /////////////////////////////////////////////////////////////////  SECTION 4
    { 'section': __CELESTRAK_SECTION_4, 'subsection': 'Space & Earth Science' },
    { 'section': __CELESTRAK_SECTION_4, 'subsection': 'Geodetic' },
    { 'section': __CELESTRAK_SECTION_4, 'subsection': 'Engineering' },
    { 'section': __CELESTRAK_SECTION_4, 'subsection': 'Education' },
    /////////////////////////////////////////////////////////////////  SECTION 5
    { 'section': __CELESTRAK_SECTION_5, 'subsection': 'Military' },
    { 'section': __CELESTRAK_SECTION_5, 'subsection': 'Radar Callibration' },
    { 'section': __CELESTRAK_SECTION_5, 'subsection': 'CubeSats' },
    { 'section': __CELESTRAK_SECTION_5, 'subsection': 'Other' }
];

/** Module definition (empty array is vital!). */
angular.module('celestrak-services', []);

/**
 * CELESTRAK service that permits retrieving the TLE's for the spacecraft from
 * the information at celestrak.com. It uses a CORSS proxy to avoid that
 * limitation.
 */
angular.module('celestrak-services').service('celestrak', function($http) {

    /**
     * This function reads the TLE information for a given file (called
     * subsection) stored at celestrak.com.
     * @param subsection The file to be processed.
     * @returns {*} (promise)
     */
    this.tleFile = function (subsection) {
        var uri = __CELESTRAK_RESOURCES[subsection];
        var corss_uri = getCORSSURL(uri);
        return $http.get(corss_uri).then(function (data) { return data.data; });
    };

    /**
     * This function reads all the TLE elements from a given file into an
     * array containing TLE-like structures ({id, l1, l2}).
     * @param subsection The file to be processed.
     * @returns {Array} Array of structures following the format {id, l1, l2}.
     */
    this.tleArray = function (subsection) {

        return this.tleFile(subsection).then(function(data) {

            if ( data == null )
                { throw 'No data retrieved from server...'; }

            var lines = data.split('\r');
            var s_array = [];
            var s_info = {};

            for ( var i = 0; i < lines.length; i++ ) {

                var l_i = lines[i].trim();

                if ( ( i % 3 ) == 0 ) { s_info['id'] = l_i; }
                if ( ( i % 3 ) == 1 ) { s_info['line_1'] = l_i; }
                if ( ( i % 3 ) == 2 ) {
                    s_array.push({
                        'id': s_info['id'],
                        'line_1': s_info['line_1'],
                        'line_2': l_i
                    });
                }

            }
            return s_array;

        });

    };

    /**
     * This function searchs for the TLE object of the spacecraft identifier
     * with the given TLE identifier string. If not found, an exception is
     * thrown.
     * @param tleId Identifier of the TLE object that is requested.
     * @param subsection The subsection within the Celestrak database where to
     *                      search for the TLE object.
     * @returns {*} ($http promise) TLE object ({id, l1, l2}) if found.
     * @private
     */
    this._tleObject = function (tleId, subsection) {
        return this.tleArray(subsection).then(function(data) {
            for ( var i = 0; i < data.length; i++ ) {
                $log.info('i = ' + i + ', data = ' + JSON.stringify(data));
                if ( data[i]['id'] == tleId ) { return data[i]; }
            }
        });
    };

    this.findTle = function (tleId) {

        var defer = $q.defer();
        var promises = [];

        for ( var i = 0; i < __CELESTRAK_RESOURCES; i++ ) {
            promises.push(this._tleObject(tleId, __CELESTRAK_RESOURCES[i]));
        }

        $q.all(promises).then(function(data) {
            $log.info('data = ' + JSON.stringify(data));
        });

        return defer;

    };

});
