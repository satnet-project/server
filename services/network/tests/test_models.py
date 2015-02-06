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

from django import test
import logging
from services.network.models import server as server_models


class NetworkModels(test.TestCase):

    def setUp(self):
        """Test database setup.
        """
        self.__verbose_testing = False
        if not self.__verbose_testing:
            logging.getLogger('network').setLevel(level=logging.CRITICAL)

    def test_load_server(self):

        server_models.Server.objects.load_local_server()