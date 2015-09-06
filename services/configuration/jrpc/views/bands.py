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

from rpc4django import rpcmethod
from services.configuration.models import bands as band_models
from services.configuration.jrpc.serializers import channels as \
    jrpc_channels_serial
from website import settings as satnet_settings


@rpcmethod(
    name='configuration.bands.available',
    signature=[],
    login_required=satnet_settings.JRPC_LOGIN_REQUIRED
)
def get_options():
    """JRPC method: configuration.channels.getOptions
    Returns a dictionary containing all the possible configuration
    options for adding a new communications channel to a Ground Station.
    """
    return {
        jrpc_channels_serial.BANDS_K: [
            obj.get_band_name()
            for obj in band_models.AvailableBands.objects.all()
        ],
        jrpc_channels_serial.MODULATIONS_K: [
            obj.modulation
            for obj in band_models.AvailableModulations.objects.all()
        ],
        jrpc_channels_serial.POLARIZATIONS_K: [
            obj.polarization
            for obj in band_models.AvailablePolarizations.objects.all()
        ],
        jrpc_channels_serial.BITRATES_K: [
            str(obj.bitrate)
            for obj in band_models.AvailableBitrates.objects.all()
        ],
        jrpc_channels_serial.BANDWIDTHS_K: [
            str(obj.bandwidth)
            for obj in band_models.AvailableBandwidths.objects.all()
        ]
    }
