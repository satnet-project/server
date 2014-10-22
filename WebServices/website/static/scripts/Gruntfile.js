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
    qunit: {
	    all:
        {
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
  grunt.loadNpmTasks('grunt-contrib-qunit');
  // register one or more task lists (you should ALWAYS have a "default" task list)
  grunt.registerTask('default', ['qunit']);
};
