module.exports = function (config) {
    'use strict';

    config.set({

        basePath: '',
        frameworks: ['jasmine'],

        files: [
            'lib/bower/angular/angular.js',
            'node_modules/angular-mocks/angular-mocks.js',
            'src/scripts/services/celestrak.js',
            'src/scripts/services/broadcaster.js',
            'src/scripts/services/satnet.js',
            'src/scripts/services/x.satnet.js',
            'src/scripts/services/maps.js',
            'src/scripts/models/marker.js',
            'src/scripts/models/x.servers.js',
            'src/scripts/models/x.groundstation.js',
            'src/scripts/models/x.spacecraft.js',
            'src/scripts/controllers/**/*.js',
            'src/scripts/satnet.ui.js',
            'src/scripts/leop.ui.js',
            'specs/unit/**/*.js'
        ],

        exclude: [],
        preprocessors: {},
        reporters: ['progress'],
        port: 9876,
        colors: true,
        logLevel: config.LOG_DEBUG,
        autoWatch: true,
        browsers: ['Chrome'],
        singleRun: false

    });
};
