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

from django.contrib.auth.models import User
from django.test.client import RequestFactory
from accounts.models import UserProfile
from configuration.jrpc import rules
from configuration.models.channels import AvailableModulations, \
    AvailableBands, AvailableBandwidths, AvailablePolarizations,  \
    AvailableBitrates
from configuration.models.segments import GroundStationConfiguration
from registration.models import RegistrationProfile


def testdb_create_user(username='testuser', password='testuser.'):
    """
    This method creates a new user in the database.
    :return: Reference to the just-created user.
    """
    user = User.objects.create_user(
        username=username, email='test@test.test', password=password)
    user.save()
    return user


def testdb_create_user_profile(username='testuser', password='testuser.'):
    """
    This method creates a new user profile and its associated User, with the
    parameteres provided, in case the given user object is None.
    :param username: Name for the new user, in case this had to be created.
    :param password: Password for the new user, in case this had to be created.
    :return: The UserProfile object created.
    """

    email = 'test@test.test'
    first_name, last_name = 'test_first_name', 'test_last_name'
    organization, country = 'test_organization', 'US'

    user_profile = UserProfile.objects.create(username=username,
                                              first_name=first_name,
                                              last_name=last_name,
                                              email=email,
                                              organization=organization,
                                              country=country,
                                              is_active=False,
                                              is_verified=False,
                                              is_blocked=False)
    user_id = user_profile.user_ptr_id
    new_user = User.objects.get(id=user_id)
    new_user.set_password(password)
    new_user.save()
    RegistrationProfile.objects.create_profile(new_user)

    return user_profile


def testdb_create_request(url='/test', user_profile=None):
    """
    This method creates an HTTP request linked to a test user that, in case
    it is not provided, it is created through the method
    :param url: URL for the HTTP request.
    :return: The created HTTP request.
    """

    factory = RequestFactory()
    request = factory.get(url)

    if user_profile:
        request.user = user_profile
    else:
        request.user = testdb_create_user_profile()

    return request


def testdb_create_gs(user_profile=None, identifier='gs-castrelos',
                     ch_identifier='chan-test'):
    """
    This method creates a GroundStationConfiguration object in the database
    that is owned by the given user_profile. In case no user_profile is
    given, a new one is created with the default parameters of the method
    testdb_create_user_profile().
    :param user_profile: The UserProfile of the user that owns this
                            GroundStationConfiguration object.
    :param identifier: The identifier for the new GroundStationConfiguration
                        object.
    :param ch_identifier: Identifier for the channel to be added to this Ground
                            Station.
    :return: The just-created GroundStationConfiguration object.
    """

    if not user_profile:
        user_profile = testdb_create_user_profile()

    gs = GroundStationConfiguration.objects\
        .create(user=user_profile,
                identifier=identifier,
                callsign='KAKA00',
                contact_elevation=10.3,
                longitude=43.42,
                latitude=45.45,
                country=None,
                IARU_region=1)
    gs.save()

    o = AvailableModulations.objects.create(modulation='FM')
    o.save()
    o = AvailableModulations.objects.create(modulation='AFSK')
    o.save()
    b = AvailableBands.objects\
        .create(IARU_range='UHF', IARU_band='70 cm', AMSAT_letter='U',
                IARU_allocation_minimum_frequency=435.000000,
                IARU_allocation_maximum_frequency=438.000000,
                uplink=True, downlink=True)
    b.save()
    o = AvailableBitrates.objects.create(bitrate=300)
    o.save()
    o = AvailableBitrates.objects.create(bitrate=600)
    o.save()
    o = AvailableBitrates.objects.create(bitrate=900)
    o.save()
    o = AvailableBandwidths.objects.create(bandwidth=12.500)
    o.save()
    o = AvailableBandwidths.objects.create(bandwidth=25.000)
    o.save()
    o = AvailablePolarizations.objects.create(polarization="Any")
    o.save()

    o = GroundStationConfiguration.objects\
        .add_channel(gs_identifier=identifier,
                     identifier=ch_identifier,
                     band=b,
                     modulations=AvailableModulations.objects.all(),
                     bitrates=AvailableBitrates.objects.all(),
                     bandwidths=AvailableBandwidths.objects.all(),
                     polarizations=AvailablePolarizations.objects.all())
    o.save()
    gs.channels.add(o)
    gs.save()

    return gs


def testdb_create_jrpc_once_rule():

    rule = {
        rules.__RULE_OP: rules.__RULE_OP_ADD,
        rules.__RULE_PERIODICITY: rules.__RULE_PERIODICITY_ONCE,
        rules.__RULE_DATES: {
            rules.__RULE_ONCE_DATE: '',
            rules.__RULE_ONCE_S_TIME: '11:00',
            rules.__RULE_ONCE_E_TIME: '12:00',
        },
    }

    return rule
