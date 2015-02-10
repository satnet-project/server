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

import logging
from periodically import decorators

logger = logging.getLogger('accounts')


@decorators.daily()
def accounts_delete_expired_users():
    """
    Task to be executed periodically for cleaning up all users whose activation
    key is expired and they did not complete still their registration process.
    """
    logger.debug("DeleteExpiredUsers, daily task execution!")
    # ### TODO :: check user experation for django-allauth