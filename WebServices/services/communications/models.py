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
from services.configuration.models import segments as segment_models


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