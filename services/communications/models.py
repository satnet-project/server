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

from django.db import models
from services.common import misc
from services.configuration.models import segments as segment_models
from services.configuration.models import channels as channel_models
from services.scheduling.models import operational as operational_models


class PassiveMessage(models.Model):
    """Message model class for received out-of-operations messages
    This class models the messages to be sent from Ground Stations to the
    network with the data passively received from satellites. This means that
    no remote operation has to be scheduled for the data to be received.
    """
    class Meta:
        app_label = 'communications'

    groundstation = models.ForeignKey(
        segment_models.GroundStation,
        verbose_name='GroundStation that tx/rx this message'
    )

    retrieved = models.BooleanField(
        'Indicates whether the message has been retrieved by a remote user.',
        default=False
    )

    doppler_shift = models.FloatField(
        'Doppler shift during the reception of the message.'
    )

    groundstation_timestamp = models.BigIntegerField(
        'Timestamp for when this message was received at the Ground Station'
    )
    reception_timestamp = models.BigIntegerField(
        'Timestamp for when this message was received at the server'
    )

    message = models.CharField(
        'Message raw data in base64',
        max_length=4000
    )

    def __unicode__(self):
        """Human readable unicode string
        Human readable representation of this object as an unicode string.
        :return: Unicode string
        """
        return '>>> message (#' + str(self.pk) + '), gs = ' +\
               str(self.groundstation) + '@' +\
               str(self.groundstation_timestamp) + ', (BASE64)=' +\
               str(self.message)


class MessageManager(models.Manager):
    """
    Manager for the messages.

    This manager handles the operations over the PassiveMessage table in the
    database.
    """

    def create(
        self, operational_slot, upwards, forwarded, tx_timestamp, message
    ):
        """Creates the object in the database.
        Creates the object in the database with the data provided and including
        the current UTC timestamp as the timestamp of the moment at which this
        message was received in the server.
        :param tx_timestamp: Timestamp of the moment at which this message was
                                received at the GroundStation.
        :param message: Binary message to be stored in the database.
        """
        gs_channel = operational_slot.groundstation_channel,
        sc_channel = operational_slot.spacecraft_channel

        return super(MessageManager, self).create(
            operational_slot=operational_slot,
            groundstation_channel=gs_channel,
            spacecraft_channel=sc_channel,
            upwards=upwards,
            forwarded=forwarded,            
            reception_timestamp=misc.get_utc_timestamp(),
            transmission_timestamp=tx_timestamp,
            message=message
        )


class Message(models.Model):
    """Message model class.

    This class includes all the information related with the relay of a
    message.
    """

    objects = MessageManager()

    operational_slot = models.ForeignKey(
        operational_models.OperationalSlot,
        verbose_name='OperationalSlot during which the message was transmitted'
    )

    groundstation_channel = models.ForeignKey(
        channel_models.GroundStationChannel,
        verbose_name='GroundStation channel that tx/rx this message'
    )
    spacecraft_channel = models.ForeignKey(
        channel_models.SpacecraftChannel,
        verbose_name='Spacecraft channel that tx/rx this message'
    )

    upwards = models.BooleanField(
        'Message relay direction(upwards = GS-to-SC, downwards = SC-to-GS)',
        default=False
    )
    forwarded = models.BooleanField(
        'Whether this message has already been forwarded to the receiver',
        default=False
    )

    reception_timestamp = models.BigIntegerField(
        'Timestamp at which this message was received at the server'
    )
    transmission_timestamp = models.BigIntegerField(
        'Timestamp at which this message was forwarded to the receiver'
    )

    message = models.BinaryField('Message raw data')
