"""
   Copyright 2015 Ricardo Tubio-Pardavila

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

from django import dispatch as django_dispatch

from services.common import simulation
from services.configuration.models import tle as tle_models


update_tle_signal = django_dispatch.Signal(
    providing_args=['identifier', 'tle_l1', 'tle_l2']
)


# noinspection PyUnusedLocal
@django_dispatch.receiver(update_tle_signal)
def update_tle_handler(sender, identifier, tle_l1, tle_l2, **kwargs):
    """
    Signal receiver that updates the given TLE with the new first and second
    lines.
    :param sender: Any sender is accepted
    :param identifier: Identifier of the TLE to be updated
    :param tle_l1: New first line for the TLE
    :param tle_l2: New second line for the TLE
    :param kwargs: Additional parameters
    """
    simulation.OrbitalSimulator.check_tle_format(identifier, tle_l1, tle_l2)

    # 1) we directly update the TLE
    tle = tle_models.TwoLineElement.objects.get(identifier=identifier)
    tle.first_line = tle_l1
    tle.second_line = tle_l2
    tle.save(update_fields=['first_line', 'second_line'])
