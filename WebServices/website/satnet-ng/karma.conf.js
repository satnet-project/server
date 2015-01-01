// Karma configuration
// Generated on Wed Dec 31 2014 18:16:51 GMT-0800 (PST)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
      'http://cdnjs.cloudflare.com/ajax/libs/angular.js/1.3.8/angular.min.js',
      'https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.15/require.min.js',
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
      'specs/**/*.js'
    ],


    // list of files to exclude
    exclude: [
    ],


    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['Chrome'],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: false
  });
};
