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
from django.db import models as django_models
import logging
from services.accounts import models as account_models
from services.common import gis, misc
from services.configuration.models import segments as segment_models

logger = logging.getLogger('network')


class ServerManager(django_models.Manager):
    """Network Server model manager.
    Manager for handling the complex non-supported by default operations over
    the Server model.
    """

    def load_local_server(self):
        """
        This method loads the information for the local server, updating any
        change in the IP address that may have happened. In case the server
        does not exist in the database, it creates the local server for the
        very first time.
        """
        s_local = None

        try:

            s_local = self.get_local()
            logger.info('>>> Local server found: ' + str(s_local))
            hostname, ip_address = misc.get_fqdn_ip()

            if s_local.ip_address != ip_address:

                logger.info('>>> Updating ip_address to: ' + str(ip_address))
                s_local.ip_address = ip_address
                s_local.save()

        except Server.DoesNotExist:

            logger.warning('>>> Local server NOT found, creating instance')
            Server.objects.create(is_me=True)

    def get_local(self):
        """
        Returns a reference to the object that defines the local Server within
        the database.
        :return: Reference to the database object.
        """
        return Server.objects.get(is_me=True)

    def create(self, identifier=None, ip_address=None, **kwargs):
        """
        Creates a server and automatically adds the FQDN hostname as the
        identifier.
        :param identifier: Identifier for the server. If not given, the FQDN
                            for the current host will be used as the identifier.
        :param ip_address: IP address of the server. If not given, the IP
                            address of the current server will be used,
                            together with the associated FQDN for the current
                            host as an identifier of the server.
        :param kwargs: Rest of the parameters for the Server model.
        :return: Reference to the just-created object.
        """
        if not ip_address:
            identifier, ip_address = misc.get_fqdn_ip()
        else:
            identifier = misc.get_fqdn(ip_address)

        latitude, longitude = gis.get_remote_user_location(ip_address)
        timestamp = misc.get_utc_timestamp()

        owner = account_models.UserProfile.objects.get(pk=1)

        return super(ServerManager, self).create(
            identifier=identifier, ip_address=ip_address,
            latitude=latitude, longitude=longitude,
            timestamp=timestamp,
            owner=owner,
            **kwargs
        )


class Server(django_models.Model):
    """Network Server model.
    Class that models the information related to the configuration of the
    available network servers.
    """
    class Meta:
        app_label = 'network'

    objects = ServerManager()

    is_me = django_models.BooleanField(
        'Flag that defines whether this object represents the current server',
        default=False
    )
    is_external = django_models.BooleanField(
        'Flag that defines whether this server belongs to this subnetwork',
        default=False
    )

    owner = django_models.ForeignKey(
        account_models.UserProfile,
        verbose_name='Owner of this network server'
    )

    identifier = django_models.CharField(
        'LEOP identifier',
        max_length=30,
        unique=True,
        validators=[validators.RegexValidator(
            regex='^[a-zA-Z0-9.\-_]*$',
            message="Alphanumeric or '.-_' required",
            code='invalid_leop_identifier'
        )]
    )

    groundstations = django_models.ManyToManyField(
        segment_models.GroundStation,
        verbose_name='LEOP ground stations',
    )

    ip_address = django_models.IPAddressField(
        'IP address of this network server'
    )
    latitude = django_models.FloatField(
        'Latitude for the estimated position of this server'
    )
    longitude = django_models.FloatField(
        'Longitude for the estimated position of this server'
    )
    timestamp = django_models.BigIntegerField(
        'UTC time (in microseconds) of the last position estimation'
    )

    def __unicode__(self):
        return ">>> Network Server {" + '}'