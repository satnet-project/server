/*
   Copyright 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        jshint: {
            // define the files to lint
            files: ['gruntfile.js', 'src/scripts/**/*.js', 'test/**/*.js'],
            // configure JSHint (documented at http://www.jshint.com/docs/)
            options: {
                // more options here if you want to override JSHint defaults
                globals: {
                    jQuery: true,
                    console: true,
                    module: true
                }
            }
        },
        clean : ['dist'],
        sass: {
            main: {
                files: [
                    {
                        expand: true,
                        cwd: 'src/css/sass',
                        src: ['*.scss'],
                        dest: 'dist',
                        ext: '.css'
                    }
                ]
            }
        },
        concat: {
            options: {
                // define a string to put in between each file in the output
                separator: ';'
            },
            main: {
                src: [
                    'src/scripts/services/celestrak.js',
                    'src/scripts/services/broadcaster.js',
                    'src/scripts/services/maps.js',
                    'src/scripts/services/satnet.js',
                    'src/scripts/services/x.satnet.js',
                    'src/scripts/models/marker.js',
                    'src/scripts/models/x.servers.js',
                    'src/scripts/models/x.groundstation.js',
                    'src/scripts/models/x.spacecraft.js',
                    'src/scripts/controllers/**/*.js',
                    'src/scripts/satnet.ui.js',
                    'src/scripts/leop.ui.js'
                ],
                dest: 'dist/<%= pkg.name %>.js'
            }
        },
        copy: {
            images: {
                files: [
                    {
                        expand: true,
                        cwd: 'src/images',
                        src: ['*'],
                        dest: 'dist/images',
                        filter: 'isFile'
                    }
                ]
            },
            lib: {
                files: [
                    {
                        expand: true,
                        flatten: true,
                        filter: 'isFile',
                        cwd: 'lib',
                        src: [
                            '*.js',
                            '*.css',
                            'bower/angular-ui-bootstrap-bower/ui-bootstrap-tpls.min.js',
                            'bower/nya-bootstrap-select/src/nya-bootstrap-select.js',
                            'bower/ng-remote-validate/release/ngRemoteValidate.js',
                            'bower/angular-uuid/uuid.min.js',
                            'bower/angular-jsonrpc/jsonrpc.min.js',
                            'bower/Leaflet.label/dist/leaflet.label.js',
                            'bower/Leaflet.label/dist/leaflet.label.css'
                        ],
                        dest: 'dist/lib'
                    }
                ]
            }
        },
        cssmin: {
            main: {
                files: [
                    {
                        expand: true,
                        cwd: 'dist',
                        src: ['<%= pkg.name %>.css'],
                        dest: 'dist',
                        ext: '.min.css',
                    }
                ]
            },
            lib: {
                files: [
                    {
                        expand: true,
                        cwd: 'lib',
                        src: ['*.css'],
                        dest: 'dist/lib',
                        ext: '.min.css',
                    }
                ]
            }
        },
        uglify: {
            options: {
                // the banner is inserted at the top of the output
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n'
            },
            dist: {
                files: {
                    'dist/<%= pkg.name %>.min.js': ['<%= concat.main.dest %>']
                }
            }
        },
        watch: {
            js: {
                files: ['<%= jshint.files %>'],
                tasks: ['jshint', 'concat', 'copy', 'uglify']
            },
            sass: {
                files: ['src/css/sass/*.scss', 'css/sass/*.scss'],
                tasks: ['sass']
            },
            cssmin: {
                files: ['dist/<%= pkg.name %>.css'],
                tasks: ['cssmin']
            },
            libs: {
                files: ['lib/*.js'],
                tasks: ['copy']
            }
        },
        qunit: {
	        all: {
                options: {
                    urls: ['tests/index.html'],
                    '--web-security' : false,
                    '--local-to-remote-url-access' : true,
                    '--ignore-ssl-errors' : true
                }
            }
        }
    });

    // load up your plugins
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-qunit');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-clean');
    // register one or more task lists (you should ALWAYS have a "default" task list)
    // this would be run by typing "grunt test" on the command line
    grunt.registerTask('test', ['jshint', 'qunit']);
    // the default task can be run just by typing "grunt" on the command line
    grunt.registerTask('default', ['clean', 'sass', 'concat', 'copy', 'cssmin', 'uglify']);
    
};
