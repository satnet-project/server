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
from django.db import models as django_models
from services.configuration.models import channels as channel_models
from services.configuration.models import segments as segment_models

logger = logging.getLogger(__name__)


class ChannelCompatibilityManager(django_models.Manager):
    """
    Manager for the ChannelCompatibility table.
    """

    def create(self, spacecraft_channel, groundstation_channel):
        """
        Overriden create method from the general manager.
        :param spacecraft_channel: compatible Spacecraft channel
        :param groundstation_channel: compatible GroundStation channel
        :return: the just created Compatibility object
        """
        return super(ChannelCompatibilityManager, self).create(
            spacecraft_channel=spacecraft_channel,
            spacecraft=spacecraft_channel.spacecraft,
            groundstation_channel=groundstation_channel,
            groundstation=groundstation_channel.groundstation
        )

    @staticmethod
    def diff_gs(groundstation_ch):
        """
        Calculates the differences between the current existing compatibility
        models in the database and the given Spacecraft channels for the
        provided Ground Station channel.
        :param groundstation_ch: The just updated channel
        :return: (to_be_added, to_be_removed) tuple with the differences
        """
        sc_chs = channel_models.SpacecraftChannel.objects.find_compatible(
            groundstation_ch
        )
        old_compatibility = ChannelCompatibility.objects.filter(
            groundstation_channel=groundstation_ch
        )
        old_c_sc_chs = set(
            [x.spacecraft_channel for x in old_compatibility]
        )
        compatible_sc_chs_s = set(sc_chs)

        return compatible_sc_chs_s - old_c_sc_chs,\
            old_c_sc_chs - compatible_sc_chs_s

    @staticmethod
    def patch_gs(groundstation_ch, to_be_added, to_be_removed):
        """
        This method "patches" the differences in between the existing already
        saved in the database models and the new compatibility groups.
        :param groundstation_ch: The channel to be changed
        :param to_be_added: The new compatible list of SC channels
        :param to_be_removed: The no-longer compatible list of SC channels
        """

        # 1) now we gotta add the new compatibilities
        for sc_ch in to_be_added:
            ChannelCompatibility.objects.create(
                spacecraft_channel=sc_ch,
                groundstation_channel=groundstation_ch
            )

        # 2) we also have to removed the no-longer existing ones
        ChannelCompatibility.objects.filter(
            groundstation_channel=groundstation_ch,
            spacecraft_channel__in=to_be_removed
        ).delete()

    @staticmethod
    def diff_sc(spacecraft_ch):
        """
        Calculates the differences between the current existing compatibility
        models in the database and the given Ground Station channels for the
        provided Spacecraft channel.
        :param spacecraft_ch: The just updated channel
        :return: (to_be_added, to_be_removed) tuple with the differences
        """
        sc_chs = channel_models.GroundStationChannel.objects.find_compatible(
            spacecraft_ch
        )
        old_compatibility = ChannelCompatibility.objects.filter(
            spacecraft_channel=spacecraft_ch
        )
        old_c_sc_chs = set(
            [x.groundstation_channel for x in old_compatibility]
        )
        compatible_sc_chs_s = set(sc_chs)

        return compatible_sc_chs_s - old_c_sc_chs,\
            old_c_sc_chs - compatible_sc_chs_s

    @staticmethod
    def patch_sc(spacecraft_ch, to_be_added, to_be_removed):
        """
        This method "patches" the differences in between the existing already
        saved in the database models and the new compatibility groups.
        :param spacecraft_ch: The channel to be changed
        :param to_be_added: The new compatible list of GS channels
        :param to_be_removed: The no-longer compatible list of GS channels
        """

        # 1) now we gotta add the new compatibilities
        for gs_ch in to_be_added:
            ChannelCompatibility.objects.create(
                spacecraft_channel=spacecraft_ch,
                groundstation_channel=gs_ch
            )

        # 2) we also have to removed the no-longer existing ones
        ChannelCompatibility.objects.filter(
            spacecraft_channel=spacecraft_ch,
            groundstation_channel__in=to_be_removed
        ).delete()


class ChannelCompatibility(django_models.Model):
    """
    This model permits handling a table where the information about the
    compatibility in between SpacecraftConfiguration, SpacecraftChannel,
    GroundStationChannel and GroundStationConfiguration objects is stored.
    """

    class Meta:
        app_label = 'scheduling'

    objects = ChannelCompatibilityManager()

    spacecraft_channel = django_models.ForeignKey(
        channel_models.SpacecraftChannel,
        verbose_name='Reference to the compatible Spacecraft channel',
        default=1
    )

    spacecraft = django_models.ForeignKey(
        segment_models.Spacecraft,
        verbose_name='Reference to the compatible Spacecraft segment',
        default=1
    )

    groundstation_channel = django_models.ForeignKey(
        channel_models.GroundStationChannel,
        verbose_name='Reference to the compatible Ground Station channel',
        default=1
    )

    groundstation = django_models.ForeignKey(
        segment_models.GroundStation,
        verbose_name='Reference to the compatible GroundStation segment',
        default=1
    )

    def __str__(self):
        """
        Transforms the contents of this object into a human readable string.
        """
        return u'{ sc_ch = ' + str(
            self.spacecraft_channel
        ) + u', gs_ch = ' + str(
            self.groundstation_channel
        ) + u' }'
