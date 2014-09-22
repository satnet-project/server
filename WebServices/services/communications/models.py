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
from services.configuration.models import channels
from services.scheduling.models import operational


class PassiveMessageManager(models.Manager):
    """Manager for the passive messages.

    This manager handles the operations over the PassiveMessage table in the
    database.
    """

    def create(self, gs_channel_id, gs_timestamp, doppler_shift, message):
        """Creates the object in the database.
        Creates the object in the database with the data provided and including
        the current UTC timestamp as the timestamp of the moment at which this
        message was received in the server.
        :param gs_channel_id: Identifier of the channel of the GroundStation
                                that retrieved this message.
        :param gs_timestamp: Timestamp of the moment at which this message was
                                received at the GroundStation.
        :param doppler_shift: Doppler shift during the reception of the message.
        :param message: Binary message to be stored in the database.
        """
        return super(PassiveMessageManager, self).create(
            groundstation_channel=channels.GroundStationChannel.objects.get(
                identifier=gs_channel_id
            ),
            groundstation_timestamp=gs_timestamp,
            reception_timestamp=misc.get_utc_timestamp(),
            doppler_shift=doppler_shift,
            #message=message
        )


class PassiveMessage(models.Model):
    """Message model class for received out-of-operations messages.

    This class models the messages to be sent from Ground Stations to the
    network with the data passively received from satellites. This means that
    no remote operation has to be scheduled for the data to be received.
    """
    class Meta:
        app_label = 'configuration'

    objects = PassiveMessageManager()

    groundstation_channel = models.ForeignKey(
        channels.GroundStationChannel,
        verbose_name='GroundStationChannel that tx/rx this message'
    )

    retrieved = models.BooleanField(
        'Flag that indicates whether the message has already been retrieved '
        'by a remote user.',
        default=False
    )

    doppler_shift = models.FloatField(
        'Doppler shift during the reception of the message.'
    )

    groundstation_timestamp = models.IntegerField(
        'Timestamp that indicates the moment at which this message was '
        'received at the Ground Station.'
    )

    reception_timestamp = models.IntegerField(
        'Timestamp that indicates the moment when this message was received at'
        'the server.'
    )
    transmission_timestamp = models.IntegerField(
        'Timestamp that indicates the moment when this message was '
        'transmitted to the receiver',
        default=0
    )

    message = models.BinaryField('Message raw data')


class Message(models.Model):
    """Message model class.

    This class includes all the information related with the relay of a
    message.
    """
    operational_slot = models.ForeignKey(
        operational.OperationalSlot,
        verbose_name='OperationalSlot during which the message was transmitted'
    )

    groundstation_channel = models.ForeignKey(
        channels.GroundStationChannel,
        verbose_name='GroundStation channel that tx/rx this message'
    )
    spacecraft_channel = models.ForeignKey(
        channels.SpacecraftChannel,
        verbose_name='Spacecraft channel that tx/rx this message'
    )

    upwards = models.BooleanField(
        'Message relay direction(upwards = GS-to-SC, downwards = SC-to-GS)'
    )
    forwarded = models.BooleanField(
        'Flag that indicates whether the message has already been forwarded '
        'to the receiver'
    )

    reception_timestamp = models.IntegerField(
        'Timestamp that indicates the moment when this message was received at'
        'the server.'
    )
    transmission_timestamp = models.IntegerField(
        'Timestamp that indicates the moment when this message was '
        'transmitted to the receiver'
    )

    message = models.BinaryField('Message raw data')