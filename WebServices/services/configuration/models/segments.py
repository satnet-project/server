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

from django.core import validators
from django.db import models
from django.db.models import signals
from django_countries import fields
import logging
from services.accounts import models as account_models
from services.common import gis
from services.configuration.models import channels, tle as tle_models

logger = logging.getLogger('models.segments')


class SpacecraftManager(models.Manager):
    """
    Manager that contains all the methods required for accessing to the
    contents of the SpacecraftConfiguration database models.
    """

    def create_ufo(self, **kwargs):
        """
        Method that creates a new Spacecraft object as an UFO object. Necessary
        for the LEOP phase.
        :param kwargs: All the other arguments necessary for the creation of
                        the object.
        :return: Reference to the newly created object.
        """
        return self.create(is_ufo=True, **kwargs)

    def create(self, tle_id, is_ufo=False, **kwargs):
        """
        Overriden "create" that receives an identifier for a TLE, gets the
        correspondent TLE object from within the CELESTRAK TLE database and
        associates it with this new Spacecraft.
        :param tle_id: Identifier of the TLE to be associated with this
                        spacecraft.
        :param kwargs: Arguments to be used for this spacecraft object.
        :return: Spacecraft object reference.
        """
        tle = tle_models.TwoLineElement.objects.get(identifier=tle_id)
        return super(SpacecraftManager, self).create(
            tle=tle, is_ufo=is_ufo, **kwargs
        )

    def add_channel(self, sc_identifier=None, **kwargs):
        """
        This method creates a new communications channel and associates it to
        the Spacecraft whose identifier is given as a parameter.
        """
        sc = self.get(identifier=sc_identifier)
        sc_ch = channels.SpacecraftChannel.objects.create(
            enabled=True, **kwargs
        )
        sc.channels.add(sc_ch)
        sc.save()

        # ### IMPORTANT ###
        # The signal 'post_save' is sent again since the first 'post_save' (as
        # a result of the invokation of the .create() method) has to be
        # filtered out by all those methods that require to access to the
        # related Spacecraft object through: spacecraft_set.all()[0]
        signals.post_save.send(
            sender=channels.SpacecraftChannel,
            instance=sc_ch,
            raw=False,
            created=False,
            using=channels.SpacecraftChannel.get_app_label(),
            update_fields=None
        )

        return sc_ch


class Spacecraft(models.Model):
    """
    This class models the configuration required for managing any type of
    spacecraft in terms of communications and pass simulations.
    """
    class Meta:
        app_label = 'configuration'

    objects = SpacecraftManager()

    user = models.ForeignKey(
        account_models.UserProfile,
        verbose_name='Owner of the Spacecraft'
    )

    identifier = models.CharField(
        'Identifier',
        max_length=30,
        unique=True,
        validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_spacecraft_identifier'
        )]
    )
    callsign = models.CharField(
        'Radio amateur callsign',
        max_length=10,
        validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_callsign'
        )]
    )

    channels = models.ManyToManyField(
        channels.SpacecraftChannel,
        verbose_name='Available spacecraft communications channels'
    )
    tle = models.ForeignKey(
        tle_models.TwoLineElement,
        verbose_name='TLE object for this Spacecraft'
    )

    is_ufo = models.BooleanField(
        'Flag that defines whether this object is an UFO or not',
        default=False
    )

    def update(self, callsign=None, tle_id=None):
        """
        Updates the configuration for the given GroundStation object. It is not
        necessary to provide all the parameters for this function, since only
        those that are not null will be updated.
        """
        changes = False

        if callsign and self.callsign != callsign:
            self.callsign = callsign
            changes = True

        if tle_id and self.tle.identifier != tle_id:
            self.tle = tle_models.TwoLineElement.objects.get(identifier=tle_id)
            changes = True

        if changes:
            self.save()

    def __unicode__(self):
        """
        Prints in a unicode string the most remarkable data for this
        spacecraft object.
        """
        return ' >>> SC, id = ' + str(self.identifier)


class GroundStationsManager(models.Manager):
    """
    Manager that contains all the methods required for accessing to the
    contents of the GroundStationConfiguration database models.
    """

    def create(
        self, latitude, longitude, altitude=None, username=None, user=None,
        **kwargs
    ):
        """
        Method that creates a new GroundStation object using the given user as
        the owner of this new segment.
        TODO IARU region has to be defined yet...
        :param latitude: Ground Station's latitude.
        :param longitude: Ground Station's Longitude.
        :param altitude: Ground Station's Altitude.
        :param kwargs: Additional parameters.
        :return: The just created GroundStation object.
        """
        if not username is None:
            user = account_models.UserProfile.objects.get(username=username)
            if user is None:
                raise Exception('User <' + username + '> could not be found.')

        if altitude is None:
            altitude = gis.get_altitude(latitude, longitude)[0]

        results = gis.get_region(latitude, longitude)
        iaru_region = 0

        return super(GroundStationsManager, self).create(
            latitude=latitude,
            longitude=longitude,
            altitude=altitude,
            country=results[gis.COUNTRY_SHORT_NAME],
            IARU_region=iaru_region,
            user=user,
            **kwargs
        )

    def add_channel(self, gs_identifier=None, **kwargs):
        """
        This method creates a new communications channel and associates it to
        the GroundStation whose identifier is given as a parameter.
        """
        gs = self.get(identifier=gs_identifier)
        gs_ch = channels.GroundStationChannel.objects.create(**kwargs)
        gs.channels.add(gs_ch)
        gs.save()

        # ### IMPORTANT ###
        # The signal 'post_save' is sent again since the first 'post_save' (as
        # a result of the invokation of the .create() method) has to be
        # filtered out by all those methods that require to access to the
        # related Spacecraft object through: spacecraft_set.all()[0]
        signals.post_save.send(
            sender=channels.GroundStationChannel,
            instance=gs_ch,
            raw=False,
            created=False,
            using=channels.GroundStationChannel.get_app_label(),
            update_fields=None
        )

        return gs_ch


class GroundStation(models.Model):
    """
    This class models the configuration required for managing a generic ground
    station, in terms of communication channels and pass simulations.
    """
    class Meta:
        app_label = 'configuration'

    objects = GroundStationsManager()

    user = models.ForeignKey(
        account_models.UserProfile,
        verbose_name='User to which this GroundStation belongs to'
    )

    identifier = models.CharField(
        'Unique alphanumeric identifier for this GroundStation',
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z0-9.\-_]*$',
                message="Alphanumeric or '.-_' required",
                code='invalid_spacecraft_identifier'
            )
        ]
    )
    callsign = models.CharField(
        'Radio amateur callsign for this GroundStation',
        max_length=10,
        validators=[
            validators.RegexValidator(
                regex='^[a-zA-Z0-9.\-_]*$',
                message="Alphanumeric or '.-_' required",
                code='invalid_callsign'
            )
        ]
    )

    contact_elevation = models.FloatField(
        'Minimum elevation for contact(degrees)'
    )
    latitude = models.FloatField('Latitude of the Ground Station')
    longitude = models.FloatField('Longitude of the Ground Station')
    altitude = models.FloatField('Altitude of the Ground Station')

    # Necessary for matching this information with the IARU database for band
    # regulations.
    country = fields.CountryField('Country where the GroundStation is located')
    IARU_region = models.SmallIntegerField('IARU region identifier')

    channels = models.ManyToManyField(
        channels.GroundStationChannel,
        verbose_name='Communication channels that belong to this GroundStation'
    )

    is_automatic = models.BooleanField(
        'Flag that defines this GroundStation as a fully automated one,'
        'so that it will automatically accept any operation request from a '
        'remote Spacecraft operator',
        default=False
    )

    def update(
        self, callsign=None,
        contact_elevation=None,
        latitude=None,
        longitude=None,
        is_automatic=None
    ):
        """
        Updates the configuration for the given GroundStation object. It is not
        necessary to provide all the parameters for this function, since only
        those that are not null will be updated.
        """
        changes = False
        change_altitude = False

        if callsign and self.callsign != callsign:
            self.callsign = callsign
            changes = True
        if not contact_elevation is None and\
                self.contact_elevation != contact_elevation:
            self.contact_elevation = contact_elevation
            changes = True

        if is_automatic and self.is_automatic != is_automatic:
            self.is_automatic = is_automatic
            changes = True

        if latitude and self.latitude != latitude:
            self.latitude = latitude
            changes = True
            change_altitude = True
        if longitude and self.longitude != longitude:
            self.longitude = longitude
            changes = True
            change_altitude = True

        if change_altitude:
            self.altitude = gis.get_altitude(self.latitude, self.longitude)[0]
        if changes:
            self.save()

    def has_channel(self, gs_channel_id):
        """Checker method.

        This method checks whether this GroundStation has the given Channel
        or not associated with it.
        :param gs_channel_id: identifier of the Channel of the GroundStation
                                whose ownership to this segment is to be
                                checked.
        :return: 'True' if the channel is associated with this GroundStation.
        """
        return self.channels\
            .filter(enabled=True)\
            .filter(identifier=gs_channel_id)\
            .exists()

    def __unicode__(self):
        """
        Prints in a unicode string the most remarkable data for this
        spacecraft object.
        """
        return ' >>> GS, id = ' + str(self.identifier) + ', callsign = ' + str(
            self.callsign
        )