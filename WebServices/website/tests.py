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
from django.test.runner import DiscoverRunner
from services.simulation.models import tle


class SatnetTestRunner(DiscoverRunner):
    """
    """

    def setup_databases(self, **kwargs):

        db = DiscoverRunner(SatnetTestRunner, self).setup_databases(
            **kwargs
        )
        sys.stdout.write('>>> Loading CELESTRAK tles: ')
        sys.stdout.flush()
        tle.TwoLineElementsManager.load_celestrak()
        print ' done!'

        """
        sys.stdout.write('>>> Adding <SWISSCUBE> as testing Spacecraft...')
        sys.stdout.flush()
        db_tools.create_sc(
            user_profile=db_tools.create_user_profile(),
            identifier='sc-swisscube', tle_id='SWISSCUBE'
        )
        print ' done!'
        """

        return db