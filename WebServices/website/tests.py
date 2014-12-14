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

import sys
import urllib2
from django.test.runner import DiscoverRunner
from services.common.testing import helpers as db_tools
from services.configuration.models import tle


class SatnetTestRunner(DiscoverRunner):
    """Custom Test Runner.
    Custom test runner for the SATNet services that pre-loads some information
    in the database for the tests.
    """

    def setup_databases(self, **kwargs):

        db = DiscoverRunner(SatnetTestRunner, self).setup_databases(
            **kwargs
        )
        sys.stdout.write('>>> Loading CELESTRAK tles: ')
        sys.stdout.flush()

        try:

            tle.TwoLineElementsManager.load_tles()
            # tle.TwoLineElementsManager.load_celestrak()
            print ' done!'

            sys.stdout.write('>>> Adding <CANX-2> as testing Spacecraft...')
            sys.stdout.flush()
            db_tools.create_sc(
                user_profile=db_tools.create_user_profile(
                    username='globaluser'
                ),
                identifier='sc-canx-2', tle_id='CANX-2'
            )
            print ' done!'

        except urllib2.URLError:
            print ' No internet connection! Could not load TLEs.'

        sys.stdout.write('>>> Initializing available bands...')
        sys.stdout.flush()
        db_tools.init_available()
        print ' done!'

        return db