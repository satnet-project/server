"""
Tests for the verification of the channel models access to the database.
"""

__author__ = 'rtubiopa@calpoly.edu'

from django.test import TestCase

from accounts.models import UserProfile
from configuration.models import AvailableModulations, AvailablePolarizations,\
    AvailableBitrates, AvailableBandwidths, GroundStationChannel, \
    GroundStationConfiguration
from configuration.models_bands import AvailableBands

from django.contrib.auth.models import User


class ChannelsTest(TestCase):
    """
    Test class for the channel model testing process. It helps in managing the
    required testing database.

    The 'create' method is not tested since it is utilized for populating the
    testing database. Therefore, the correct exectuion of the rest of the tests
    involves a correct functioning of this method.
    """

    def setUp(self):
        """
        Populates the initial database with a set of objects required to run
        the following tests.
        """
        #[12:20:53.968] ({name:"chan-u-2", bandwidths:["12.500", "25.000"],
        # polarizations:["RHCP"], band:"UHF / U / 435.000000 / 438.000000",
        # bitrates:[300, 600, 900], modulations:["FM"]})

        user = User.objects.create(username='rtubio',
                                   email='rtubiopa@calpoly.edu',
                                   password='password',
                                   is_staff=False,
                                   is_superuser=False)
        user.save()

        user_profile = UserProfile.objects\
            .create(organization='Testing',country='ES',
                    is_verified='true',is_blocked='false')
        user_profile.save()

        gs_identifier = 'gs-castrelos'
        gs = GroundStationConfiguration.objects\
            .create(user=user_profile,
                    identifier=gs_identifier,
                    callsign='KAKA00',
                    contact_elevation=10.3,
                    longitude=43.42,
                    latitude=45.45,
                    country=None,
                    IARU_region=1)
                    #channels=None)
        gs.save()

        o = AvailableModulations.objects.create(modulation='FM')
        o.save()
        o = AvailableModulations.objects.create(modulation='AFSK')
        o.save()
        o = AvailableBands.objects\
            .create(IARU_range='UHF', IARU_band='70 cm', AMSAT_letter='U',
                    IARU_allocation_minimum_frequency=435.000000,
                    IARU_allocation_maximum_frequency=438.000000,
                    uplink=True, downlink=True)
        band_name = o.get_band_name()
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
        o = AvailablePolarizations.objects.create(polarization="Any")
        o.save()

        o = GroundStationChannel.objects\
            .create(gs_identifier=gs_identifier,
                    identifier='chan-u-0',
                    band_name="UHF / U / 435.000000 / 438.000000",
                    modulations_list=AvailableModulations.objects.all(),
                    bitrates_list=AvailableBitrates.objects.all(),
                    bandwidths_list=AvailableBandwidths.objects.all(),
                    polarizations_list=AvailablePolarizations.objects.all())
        o.save()
        gs.channels.add(o)
        gs.save()

    def test_channel_update(self):
        """
        Test that the update method of a channel works properly. Take into
        consideration the fact that it must support a partial definition of
        all the properties of a channel object.
        """
        print '>>> TEST (test_channel_update):'

        ch = GroundStationChannel.objects.update(
            current_identifier='chan-u-0', identifier='chan-u-X')

        gs, ch2 = GroundStationConfiguration.objects.get_channel(
            ground_station_id='gs-castrelos', channel_id='chan-u-X')
        self.assertEquals(ch.identifier, ch2.identifier)
