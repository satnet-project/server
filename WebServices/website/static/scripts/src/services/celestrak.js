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

/** Module definition (empty array is vital!). */
angular.module('celestrak-services', [ 'common' ]);

/**
 * CELESTRAK service that permits retrieving the TLE's for the spacecraft from
 * the information at celestrak.com. It uses a CORSS proxy to avoid that
 * limitation.
 */
angular.module('celestrak-services').service('celestrak', [
    '$http', '$q', '$log', 'common',
    function($http, $q, $log, common) {

    'use strict';

    // Base URL
    this.CELESTRAK_URL_BASE = 'http://celestrak.com/NORAD/elements/';
    // Weather and Earth Resources
    this.CELESTRAK_SECTION_1 = 'Weather & Earth Resources';
    this.CELESTRAK_WEATHER = this.CELESTRAK_URL_BASE + 'weather.txt';
    this.CELESTRAK_NOAA = this.CELESTRAK_URL_BASE + 'noaa.txt';
    this.CELESTRAK_GOES = this.CELESTRAK_URL_BASE + 'goes.txt';
    this.CELESTRAK_EARTH_RESOURCES = this.CELESTRAK_URL_BASE + 'resource.txt';
    this.CELESTRAK_SARSAT = this.CELESTRAK_URL_BASE + 'sarsat.txt';
    this.CELESTRAK_DISASTER_MONITORING = this.CELESTRAK_URL_BASE + 'dmc.txt';
    this.CELESTRAK_TRACKING_DATA_RELAY = this.CELESTRAK_URL_BASE + 'tdrss.txt';
    this.CELESTRAK_ARGOS = this.CELESTRAK_URL_BASE + 'argos.txt';
    // Communications
    this.CELESTRAK_SECTION_2 = 'Communications';
    this.CELESTRAK_GEOSTATIONARY = this.CELESTRAK_URL_BASE + 'geo.txt';
    this.CELESTRAK_INTELSAT = this.CELESTRAK_URL_BASE + 'intelsat.txt';
    this.CELESTRAK_GORIZONT = this.CELESTRAK_URL_BASE + 'gorizont.txt';
    this.CELESTRAK_RADUGA = this.CELESTRAK_URL_BASE + 'raduga.txt';
    this.CELESTRAK_MOLNIYA = this.CELESTRAK_URL_BASE + 'molniya.txt';
    this.CELESTRAK_IRIDIUM = this.CELESTRAK_URL_BASE + 'iridium.txt';
    this.CELESTRAK_ORBCOMM = this.CELESTRAK_URL_BASE + 'orbcomm.txt';
    this.CELESTRAK_GLOBALSTAR = this.CELESTRAK_URL_BASE + 'globalstar.txt';
    this.CELESTRAK_AMATEUR_RADIO = this.CELESTRAK_URL_BASE + 'amateur.txt';
    this.CELESTRAK_EXPERIMENTAL = this.CELESTRAK_URL_BASE + 'x-comm.txt';
    this.CELESTRAK_COMMS_OTHER = this.CELESTRAK_URL_BASE + 'other-comm.txt';
    // Navigation
    this.CELESTRAK_SECTION_3 = 'Navigation';
    this.CELESTRAK_GPS_OPERATIONAL = this.CELESTRAK_URL_BASE + 'gps-ops.txt';
    this.CELESTRAK_GLONASS_OPERATIONAL = this.CELESTRAK_URL_BASE + 'glo-ops.txt';
    this.CELESTRAK_GALILEO = this.CELESTRAK_URL_BASE + 'galileo.txt';
    this.CELESTRAK_BEIDOU = this.CELESTRAK_URL_BASE + 'beidou.txt';
    this.CELESTRAK_SATELLITE_AUGMENTATION = this.CELESTRAK_URL_BASE + 'sbas.txt';
    this.CELESTRAK_NNSS = this.CELESTRAK_URL_BASE + 'nnss.txt';
    this.CELESTRAK_RUSSIAN_LEO_NAVIGATION = this.CELESTRAK_URL_BASE + 'musson.txt';
    // Scientific
    this.CELESTRAK_SECTION_4 = 'Scientific';
    this.CELESTRAK_SPACE_EARTH_SCIENCE = this.CELESTRAK_URL_BASE + 'science.txt';
    this.CELESTRAK_GEODETIC = this.CELESTRAK_URL_BASE + 'geodetic.txt';
    this.CELESTRAK_ENGINEERING = this.CELESTRAK_URL_BASE + 'engineering.txt';
    this.CELESTRAK_EDUCATION = this.CELESTRAK_URL_BASE + 'education.txt';
    // Miscellaneous
    this.CELESTRAK_SECTION_5 = 'Miscellaneous';
    this.CELESTRAK_MILITARY = this.CELESTRAK_URL_BASE + 'military.txt';
    this.CELESTRAK_RADAR_CALLIBRATION = this.CELESTRAK_URL_BASE + 'radar.txt';
    this.CELESTRAK_CUBESATS = this.CELESTRAK_URL_BASE + 'cubesat.txt';
    this.CELESTRAK_OTHER = this.CELESTRAK_URL_BASE + 'other.txt';
    // CELESTRAK resources within a structured data type...
    this.CELESTRAK_RESOURCES = {
        'Weather': this.CELESTRAK_WEATHER,
        'NOAA': this.CELESTRAK_NOAA,
        'GOES': this.CELESTRAK_GOES,
        'Earth Resources': this.CELESTRAK_EARTH_RESOURCES,
        'SARSAT': this.CELESTRAK_SARSAT,
        'Disaster Monitoring': this.CELESTRAK_DISASTER_MONITORING,
        'Tracking & Data Relay': this.CELESTRAK_TRACKING_DATA_RELAY,
        'ARGOS': this.CELESTRAK_ARGOS,
        'Geostationary': this.CELESTRAK_GEOSTATIONARY,
        'Intelsat': this.CELESTRAK_INTELSAT,
        'Gorizont': this.CELESTRAK_GORIZONT,
        'Raduga': this.CELESTRAK_RADUGA,
        'Molniya': this.CELESTRAK_MOLNIYA,
        'Iridium': this.CELESTRAK_IRIDIUM,
        'Orbcomm': this.CELESTRAK_ORBCOMM,
        'Globalstar': this.CELESTRAK_GLOBALSTAR,
        'Amateur Radio': this.CELESTRAK_AMATEUR_RADIO,
        'Experimental': this.CELESTRAK_EXPERIMENTAL,
        'Others': this.CELESTRAK_COMMS_OTHER,
        'GPS Operational': this.CELESTRAK_GPS_OPERATIONAL,
        'Glonass Operational': this.CELESTRAK_GLONASS_OPERATIONAL,
        'Galileo': this.CELESTRAK_GALILEO,
        'Beidou': this.CELESTRAK_BEIDOU,
        'Satellite-based Augmentation System': this.CELESTRAK_SATELLITE_AUGMENTATION,
        'Navy Navigation Satellite System': this.CELESTRAK_NNSS,
        'Russian LEO Navigation': this.CELESTRAK_RUSSIAN_LEO_NAVIGATION,
        'Space & Earth Science': this.CELESTRAK_SPACE_EARTH_SCIENCE,
        'Geodetic': this.CELESTRAK_GEODETIC,
        'Engineering': this.CELESTRAK_ENGINEERING,
        'Education': this.CELESTRAK_EDUCATION,
        'Military': this.CELESTRAK_MILITARY,
        'Radar Callibration': this.CELESTRAK_RADAR_CALLIBRATION,
        'CubeSats': this.CELESTRAK_CUBESATS,
        'Other': this.CELESTRAK_OTHER
    };

    this.CELESTRAK_SELECT_SECTIONS = [
        /////////////////////////////////////////////////////////////////  SECTION 1
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'Weather' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'NOAA' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'GOES' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'Earth Resources' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'SARSAT' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'Disaster Monitoring' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'Tracking & Data Relay' },
        { 'section': this.CELESTRAK_SECTION_1, 'subsection': 'ARGOS' },
        /////////////////////////////////////////////////////////////////  SECTION 2
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Geostationary' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Intelsat' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Gorizont' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Raduga' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Molniya' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Iridium' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Orbcomm' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Globalstar' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Amateur Radio' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Experimental' },
        { 'section': this.CELESTRAK_SECTION_2, 'subsection': 'Others' },
        /////////////////////////////////////////////////////////////////  SECTION 3
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'GPS Operational' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Glonass Operational' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Galileo' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Beidou' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Satellite-based Augmentation System' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Navy Navigation Satellite System' },
        { 'section': this.CELESTRAK_SECTION_3, 'subsection': 'Russian LEO Navigation' },
        /////////////////////////////////////////////////////////////////  SECTION 4
        { 'section': this.CELESTRAK_SECTION_4, 'subsection': 'Space & Earth Science' },
        { 'section': this.CELESTRAK_SECTION_4, 'subsection': 'Geodetic' },
        { 'section': this.CELESTRAK_SECTION_4, 'subsection': 'Engineering' },
        { 'section': this.CELESTRAK_SECTION_4, 'subsection': 'Education' },
        /////////////////////////////////////////////////////////////////  SECTION 5
        { 'section': this.CELESTRAK_SECTION_5, 'subsection': 'Military' },
        { 'section': this.CELESTRAK_SECTION_5, 'subsection': 'Radar Callibration' },
        { 'section': this.CELESTRAK_SECTION_5, 'subsection': 'CubeSats' },
        { 'section': this.CELESTRAK_SECTION_5, 'subsection': 'Other' }
    ];

    /**
     * This function reads the TLE information for a given file (called
     * subsection) stored at celestrak.com.
     * @param subsection The file to be processed.
     * @returns {*} (promise)
     */
    this.getSubsectionFile = function (subsection) {
        var uri = this.CELESTRAK_RESOURCES[subsection];
        var cUri = common.getCORSSURL(uri);
        return $http.get(cUri).then(function (data) { return data.data; });
    };

    /**
     * This function reads all the TLE elements from a given file into an
     * array containing TLE-like structures ({id, l1, l2}).
     * @param subsection The file to be processed.
     * @returns {Array} Array of structures following the format {id, l1, l2}.
     */
    this.getTleArray = function (subsection) {

        return this.getSubsectionFile(subsection).then(function(data) {

            if ( data === null )
                { throw 'No data retrieved from server...'; }

            var lines = data.split('\r');
            var sArray = [];
            var sInfo = {};

            for ( var i = 0; i < lines.length; i++ ) {

                var line = lines[i].trim();

                if ( ( i % 3 ) === 0 ) { sInfo.id = line; }
                if ( ( i % 3 ) === 1 ) { sInfo.l1 = line; }
                if ( ( i % 3 ) === 2 ) {
                    sArray.push({
                        'id': sInfo.id,
                        'l1': sInfo.l1,
                        'l2': line
                    });
                }

            }
            return sArray;

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
        return this.getTleArray(subsection).then(function(data) {
            for ( var i = 0; i < data.length; i++ ) {
                $log.info('i = ' + i + ', data = ' + JSON.stringify(data));
                if ( data[i].id === tleId ) { return data[i]; }
            }
        });
    };

    /**
     * This function finds the TLE information for a given Spacecraft from 
     * among all the available ones in the Celestrak database.
     * @param   {String} tleId The identifier for the Spacecraft in the
     *                         Celestrak database.
     * @returns {$q} Promise that returns the TLE object.
     */
    this.findTle = function (tleId) {

        var promises = [];

        for ( var i = 0; i < this.CELESTRAK_RESOURCES; i++ ) {
            promises.push(this._tleObject(tleId, this.CELESTRAK_RESOURCES[i]));
        }

        return $q.all(promises).then(function(data) {
            $log.info('data = ' + JSON.stringify(data));
        });

    };

}]);