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

import datetime
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.test.client import RequestFactory

from accounts.models import UserProfile
from common import gis, misc, serialization as common_serial
from configuration.jrpc import serialization
from configuration.models.bands import AvailableModulations, AvailableBands,\
    AvailableBandwidths, AvailablePolarizations, AvailableBitrates
from configuration.models import channels, segments
from registration.models import RegistrationProfile
from scheduling.models.tle import TwoLineElementsManager


def create_user(username='testuser', password='testuser.'):
    """
    This method creates a new user in the database.
    :return: Reference to the just-created user.
    """
    user = User.objects.create_user(
        username=username, email='test@test.test', password=password)
    user.save()
    return user


def create_user_profile(username='testuser', password='testuser.'):
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

    with transaction.atomic():
        user_profile = UserProfile.objects.create(
            username=username,
            first_name=first_name, last_name=last_name,
            email=email,
            organization=organization, country=country,
            is_active=False, is_verified=False, is_blocked=False
        )

    user_id = user_profile.user_ptr_id
    new_user = User.objects.get(id=user_id)
    new_user.set_password(password)
    new_user.save()
    RegistrationProfile.objects.create_profile(new_user)

    return user_profile


def create_request(url='/test', user_profile=None):
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
        request.user = create_user_profile()

    return request


def create_sc(
    user_profile=None, identifier='sc-uvigo',
    callsign='BABA00',
    tle_id='XATCOBEO'
):

    username = 'testuser'

    try:
        if not user_profile:
            user_profile = create_user_profile(username=username)
    except IntegrityError:
        print 'User already exists, getting a reference to it...'
        user_profile = UserProfile.objects.get(username=username)

    return segments.Spacecraft.objects.create(
        user=user_profile,
        identifier=identifier,
        callsign=callsign,
        tle_id=tle_id
    )


def init_available():

    o = AvailableModulations.objects.create(modulation='FM')
    o.save()
    o = AvailableModulations.objects.create(modulation='AFSK')
    o.save()
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
    o = AvailablePolarizations.objects.create(polarization='LHCP')
    o.save()
    o = AvailablePolarizations.objects.create(polarization='RHCP')
    o.save()


def init_tles_database():

    TwoLineElementsManager.load_tles()


def create_band(minimum_frequency=435000000, maximum_frequency=438000000):

    return AvailableBands.objects.create(
        IARU_range='UHF',
        IARU_band='70 cm',
        AMSAT_letter='U',
        IARU_allocation_minimum_frequency=minimum_frequency,
        IARU_allocation_maximum_frequency=maximum_frequency,
        uplink=True,
        downlink=True
    )


def create_gs(
        user_profile=None,
        identifier='gs-castrelos',
        callsign='KAKA00',
        contact_elevation=10,
        latitude=33.9333,
        longitude=-118.3880,
        altitude=20,
        country=None,
        iaru_region=1
):

    if not user_profile:
        user_profile = create_user_profile()

    if altitude is None:
        altitude = gis.get_altitude(latitude, longitude)

    return segments.GroundStation.objects.create(
        user=user_profile,
        identifier=identifier,
        callsign=callsign,
        contact_elevation=contact_elevation,
        longitude=longitude,
        latitude=latitude,
        altitude=altitude,
        country=country,
        IARU_region=iaru_region
    )


def sc_add_channel(
    sc,
    frequency,
    channel_id,
    modulation=None,
    bitrate=None,
    bandwidth=None,
    polarization=None
):

    if not modulation:
        modulation = AvailableModulations.objects.all()[0]
    if not bitrate:
        bitrate = AvailableBitrates.objects.all()[0]
    if not bandwidth:
        bandwidth = AvailableBandwidths.objects.all()[0]
    if not polarization:
        polarization = AvailablePolarizations.objects.get(polarization='RHCP')

    return segments.Spacecraft.objects.add_channel(
        sc_identifier=sc.identifier,
        identifier=channel_id,
        frequency=frequency,
        modulation=modulation,
        bitrate=bitrate,
        bandwidth=bandwidth,
        polarization=polarization,
    )


def remove_sc(spacecraft_id):

    segments.Spacecraft.objects.get(identifier=spacecraft_id).delete()


def remove_sc_channel(sc_ch_id):

    sc_ch = channels.SpacecraftChannel.objects.get(identifier=sc_ch_id)
    sc_ch.spacecraft_set.all()[0].channels.remove(sc_ch)
    sc_ch.delete()


def gs_add_channel(
        gs, band, gs_ch_id,
        modulations=None, bitrates=None, bandwidths=None, polarizations=None
):

    if modulations is None:
        modulations = AvailableModulations.objects.all()
    if bitrates is None:
        bitrates = AvailableBitrates.objects.all()
    if bandwidths is None:
        bandwidths = AvailableBandwidths.objects.all()
    if polarizations is None:
        polarizations = AvailablePolarizations.objects.all()

    gs_ch = segments.GroundStation.objects.add_channel(
        gs_identifier=gs.identifier,
        identifier=gs_ch_id,
        band=band,
        modulations=modulations,
        bitrates=bitrates,
        bandwidths=bandwidths,
        polarizations=polarizations
    )

    return gs_ch


def remove_gs_channel(gs_id, gs_ch_id):

    segments.GroundStation.objects.get(identifier=gs_id).channels.all().get(
        identifier=gs_ch_id
    ).delete()


def create_jrpc_once_rule(
        operation=serialization.RULE_OP_ADD,
        date=None,
        starting_time=None,
        ending_time=None,
):

    if date is None:
        date = misc.get_today_utc() + datetime.timedelta(days=1)

    now = misc.get_now_utc()
    if starting_time is None:
        starting_time = now + datetime.timedelta(minutes=30)
    if ending_time is None:
        ending_time = now + datetime.timedelta(minutes=45)

    return {
        serialization.RULE_OP: operation,
        serialization.RULE_PERIODICITY: serialization.RULE_PERIODICITY_ONCE,
        serialization.RULE_DATES: {
            serialization.RULE_ONCE_DATE: common_serial.serialize_iso8601_date(
                date
            ),
            serialization.RULE_ONCE_S_TIME: common_serial.serialize_iso8601_time(
                starting_time
            ),
            serialization.RULE_ONCE_E_TIME: common_serial.serialize_iso8601_time(
                ending_time
            )
        },
    }


def create_jrpc_daily_rule(
        operation=serialization.RULE_OP_ADD,
        date_i=None, date_f=None,
        starting_time=None, ending_time=None
):

    if date_i is None:
        date_i = misc.get_today_utc() + datetime.timedelta(days=1)
    if date_f is None:
        date_f = misc.get_today_utc() + datetime.timedelta(days=366)

    now = misc.get_now_utc()
    if starting_time is None:
        starting_time = now + datetime.timedelta(minutes=30)
    if ending_time is None:
        ending_time = now + datetime.timedelta(minutes=45)

    return {
        serialization.RULE_OP: operation,
        serialization.RULE_PERIODICITY: serialization.RULE_PERIODICITY_DAILY,
        serialization.RULE_DATES: {
            serialization.RULE_DAILY_I_DATE:
                common_serial.serialize_iso8601_date(date_i),
            serialization.RULE_DAILY_F_DATE:
                common_serial.serialize_iso8601_date(date_f),
            serialization.RULE_S_TIME:
                common_serial.serialize_iso8601_time(starting_time),
            serialization.RULE_E_TIME:
                common_serial.serialize_iso8601_time(ending_time),
        },
    }


def create_identifier_list(json_slot_list):
    identifier_l = []

    for l_i in json_slot_list:

        identifier_l.append(l_i['identifier'])

    return identifier_l