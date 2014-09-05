import os
import sys
import logging
import datetime
print sys.path
sys.path.append(os.path.dirname(os.getcwd()) + "/WebServices")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

from services.common import testing as db_tools, misc, simulation

from services.configuration.jrpc import channels as jrpc_channels_if
from services.configuration.jrpc import rules as jrpc_rules_if
from services.configuration.jrpc import serialization as jrpc_keys
from services.configuration.models import rules, availability, channels
from services.configuration import signals
from services.scheduling.models import operational


def _initDjangoDB():
    """
    This method populates the database with some information to be used
    only for this test.
    """
    __verbose_testing = False

    if not __verbose_testing:
        logging.getLogger('configuration').setLevel(level=logging.CRITICAL)
        logging.getLogger('scheduling').setLevel(level=logging.CRITICAL)

    __sc_1_id = 'xatcobeo-sc'
    __sc_1_tle_id = 'XATCOBEO'
    __sc_1_ch_1_id = 'xatcobeo-fm'
    __sc_1_ch_1_cfg = {
        jrpc_keys.FREQUENCY_K: '437000000',
        jrpc_keys.MODULATION_K: 'FM',
        jrpc_keys.POLARIZATION_K: 'LHCP',
        jrpc_keys.BITRATE_K: '300',
        jrpc_keys.BANDWIDTH_K: '12.500000000'
    }
    __gs_1_id = 'gs-la'
    __gs_1_ch_1_id = 'gs-la-fm'
    __gs_1_ch_1_cfg = {
        jrpc_keys.BAND_K:
        'UHF / U / 435000000.000000 / 438000000.000000',
        jrpc_keys.MODULATIONS_K: ['FM'],
        jrpc_keys.POLARIZATIONS_K: ['LHCP'],
        jrpc_keys.BITRATES_K: [300, 600, 900],
        jrpc_keys.BANDWIDTHS_K: [12.500000000, 25.000000000]
    }
    __gs_1_ch_2_id = 'gs-la-fm-2'
    __gs_1_ch_2_cfg = {
        jrpc_keys.BAND_K:
        'UHF / U / 435000000.000000 / 438000000.000000',
        jrpc_keys.MODULATIONS_K: ['FM'],
        jrpc_keys.POLARIZATIONS_K: ['LHCP'],
        jrpc_keys.BITRATES_K: [300, 600, 900],
        jrpc_keys.BANDWIDTHS_K: [12.500000000, 25.000000000]
    }

    signals.connect_availability_2_operational()
    signals.connect_channels_2_compatibility()
    signals.connect_compatibility_2_operational()
    signals.connect_rules_2_availability()
    signals.connect_segments_2_booking_tle()

    db_tools.init_available()
    db_tools.init_tles_database()
    __band = db_tools.create_band()
    __user_profile = db_tools.create_user_profile()
    # Default values: username=testuser, password=testuser.
    __sc_1 = db_tools.create_sc(
        user_profile=__user_profile,
        identifier=__sc_1_id,
        tle_id=__sc_1_tle_id,
    )
    __gs_1 = db_tools.create_gs(
        user_profile=__user_profile, identifier=__gs_1_id,
    )
    operational.OperationalSlot.objects.get_simulator().set_debug()

    jrpc_channels_if.gs_channel_create(
        ground_station_id=__gs_1_id,
        channel_id=__gs_1_ch_1_id,
        configuration=__gs_1_ch_1_cfg
    )

    jrpc_rules_if.add_rule(
        __gs_1_id, __gs_1_ch_1_id,
        db_tools.create_jrpc_daily_rule(
            starting_time=misc.localize_time_utc(datetime.time(
                hour=8, minute=0, second=0
            )),
            ending_time=misc.localize_time_utc(datetime.time(
                hour=23, minute=55, second=0
            ))
        )
    )

    jrpc_channels_if.sc_channel_create(
        spacecraft_id=__sc_1_id,
        channel_id=__sc_1_ch_1_id,
        configuration=__sc_1_ch_1_cfg
    )


if __name__ == '__main__':
    _initDjangoDB()
