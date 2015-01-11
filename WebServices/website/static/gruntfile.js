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

module.exports = function (grunt) {
    'use strict';

    grunt.initConfig({

        pkg: grunt.file.readJSON('package.json'),
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
        cssmin: {
            main: {
                files: [
                    {
                        expand: true,
                        cwd: 'dist',
                        src: ['<%= pkg.name %>.css'],
                        dest: 'dist',
                        ext: '.min.css'
                    }
                ]
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
            }
        },
        watch: {
            sass: {
                files: ['src/css/sass/*.scss'],
                tasks: ['sass']
            },
            cssmin: {
                files: ['dist/<%= pkg.name %>.css'],
                tasks: ['cssmin']
            },
            images: {
                files: ['src/images/*'],
                tasks: ['copy']
            }
        }
    });

    // load up your plugins
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-copy');
    // register one or more task lists (you should ALWAYS have a "default" task list)
    // this would be run by typing "grunt test" on the command line
    grunt.registerTask('test', ['sass']);
    // the default task can be run just by typing "grunt" on the command line
    grunt.registerTask('default', ['sass', 'cssmin', 'copy']);

};
