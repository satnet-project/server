"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila
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

from services.common import serialization as common_serial
from services.configuration.models import rules, bands

CHANNEL_LIST_K = 'segment_channels'

# ### JSON keys for enconding/decoding GroundStation dictionaries
GS_ID_K = 'groundstation_id'
GS_LATLON_K = 'groundstation_latlon'
GS_ALTITUDE_K = 'groundstation_altitude'
GS_CALLSIGN_K = 'groundstation_callsign'
GS_ELEVATION_K = 'groundstation_elevation'

# ### JSON keys for encoding/decoding Spacecraft dictionaries
SC_ID_K = 'spacecraft_id'
SC_CALLSIGN_K = 'spacecraft_callsign'
SC_TLE_ID_K = 'spacecraft_tle_id'


# ### JSON keys for decoding data from the dictionary
CH_ID_K = 'channel_id'
# ## Keys only for GroundStation channel parameters
BAND_K = 'band'
MODULATIONS_K = 'modulations'
POLARIZATIONS_K = 'polarizations'
BITRATES_K = 'bitrates'
BANDWIDTHS_K = 'bandwidths'
AUTOMATED_K = 'automated'
# ### Keys only for Spacecraft Channel parameters
FREQUENCY_K = 'frequency'
MODULATION_K = 'modulation'
POLARIZATION_K = 'polarization'
BITRATE_K = 'bitrate'
BANDWIDTH_K = 'bandwidth'


# JRPC keys for data exchange with clients through key-indexed objects.
RULE_OP = 'rule_operation'
RULE_OP_ADD = '+'
RULE_OP_REMOVE = '-'
RULE_PERIODICITY = 'rule_periodicity'
RULE_PERIODICITY_ONCE = 'rule_periodicity_once'
RULE_PERIODICITY_DAILY = 'rule_periodicity_daily'
RULE_PERIODICITY_WEEKLY = 'rule_periodicity_weekly'
RULE_DATES = 'rule_dates'
RULE_ONCE_DATE = 'rule_once_date'
RULE_ONCE_S_TIME = 'rule_once_starting_time'
RULE_ONCE_E_TIME = 'rule_once_ending_time'
RULE_DAILY_I_DATE = 'rule_daily_initial_date'
RULE_DAILY_F_DATE = 'rule_daily_final_date'
RULE_S_TIME = 'rule_starting_time'
RULE_E_TIME = 'rule_ending_time'
RULE_WEEKLY_DATE = 'rule_weekly_date'
RULE_WEEKLY_DATE_DAY = 'rule_weekly_date_day'
RULE_WEEKLY_WEEKDAYS = (
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
    'sunday'
)

# ### Conversion in between network keys and database keys. Notice that some
# of the keys required for the transmission of data through the network are
# not required for storing/retrieving data to/from the database, since that
# information is already stored within the hiearchy of the structure of the
# database.
__net2db__ = {
    RULE_OP_ADD: rules.ADD_SLOTS,
    RULE_OP_REMOVE: rules.REMOVE_SLOTS,
    RULE_PERIODICITY_ONCE: rules.ONCE_PERIODICITY,
    RULE_PERIODICITY_DAILY: rules.DAILY_PERIODICITY,
    RULE_PERIODICITY_WEEKLY: rules.WEEKLY_PERIODICITY,
}
# ... from database 2 network:
__db2net__ = {
    rules.ADD_SLOTS: RULE_OP_ADD,
    rules.REMOVE_SLOTS: RULE_OP_REMOVE,
    rules.ONCE_PERIODICITY: RULE_PERIODICITY_ONCE,
    rules.DAILY_PERIODICITY: RULE_PERIODICITY_DAILY,
    rules.WEEKLY_PERIODICITY: RULE_PERIODICITY_WEEKLY,
}

# ### Dictionary with the operations supported
__supported_operations__ = {
    RULE_OP_ADD: True,
    RULE_OP_REMOVE: True,
}

# ### Dictionary with the periodicities supported:
__supported_periodicities__ = {
    RULE_PERIODICITY_ONCE: True,
    RULE_PERIODICITY_DAILY: True,
    RULE_PERIODICITY_WEEKLY: True,
}


def check_gs_channel_configuration(configuration):
    """
    This method checks whether the given dictionary contains or not all the
    keys that are required for a valid channel configuration. In case it
    doesn't, an exception is raised.
    """
    if not BAND_K in configuration:
        raise Exception("Parameter not provided, key = " + BAND_K)
    if not MODULATIONS_K in configuration:
        raise Exception("Parameter not provided, key = " + MODULATIONS_K)
    if not POLARIZATIONS_K in configuration:
        raise Exception("Parameter not provided, key = " + POLARIZATIONS_K)
    if not BITRATES_K in configuration:
        raise Exception("Parameter not provided, key = " + BITRATES_K)
    if not BANDWIDTHS_K in configuration:
        raise Exception("Parameter not provided, key = " + BANDWIDTHS_K)
    if not AUTOMATED_K in configuration:
        raise Exception("Parameter not provided, key = " + AUTOMATED_K)


def check_sc_channel_configuration(configuration):
    """
    This method checks whether the given dictionary contains or not all the
    keys that are required for a valid channel configuration. In case it
    doesn't, an exception is raised.
    """
    if not FREQUENCY_K in configuration:
        raise Exception("Parameter not provided, key = " + FREQUENCY_K)
    if not MODULATION_K in configuration:
        raise Exception("Parameter not provided, key = " + MODULATION_K)
    if not POLARIZATION_K in configuration:
        raise Exception("Parameter not provided, key = " + POLARIZATION_K)
    if not BITRATE_K in configuration:
        raise Exception("Parameter not provided, key = " + BITRATE_K)
    if not BANDWIDTH_K in configuration:
        raise Exception("Parameter not provided, key = " + BANDWIDTH_K)


def serialize_gs_channel_configuration(channel):
    """
    This method returns a dictionary with the key, value pairs containing
    the current configuration for the given channel object. The keys used are
    the ones required by the JRPC protocol.
    """
    return {
        CH_ID_K: channel.identifier,
        BAND_K: channel.band.get_band_name(),
        AUTOMATED_K: channel.automated,
        MODULATIONS_K: sorted(
            [obj.modulation for obj in channel.modulations.all()]
        ),
        POLARIZATIONS_K: sorted(
            [obj.polarization for obj in channel.polarizations.all()]
        ),
        BITRATES_K: sorted(
            [obj.bitrate for obj in channel.bitrates.all()]
        ),
        BANDWIDTHS_K: sorted(
            [obj.bandwidth for obj in channel.bandwidths.all()]
        )
    }


def serialize_sc_channel_configuration(channel):
    """
    This method returns a dictionary with the key, value pairs containing
    the current configuration for the given channel object. The keys used are
    the ones required by the JRPC protocol.
    """
    return {
        CH_ID_K: channel.identifier,
        FREQUENCY_K: channel.frequency,
        MODULATION_K: channel.modulation.modulation,
        POLARIZATION_K: channel.polarization.polarization,
        BITRATE_K: channel.bitrate.bitrate,
        BANDWIDTH_K: channel.bandwidth.bandwidth
    }


def deserialize_sc_channel_parameters(configuration):
    """
    Spacecraft channel parameters are returned from within the configuration
    structure passed as first parameter.
    :param configuration: The configuration structure with all the data.
    :return: Tuple containing all parameters as separate variables.
    """
    check_sc_channel_configuration(configuration)

    return configuration[FREQUENCY_K],\
        bands.AvailableModulations.objects.get(
            modulation=configuration[MODULATION_K]
        ),\
        bands.AvailableBitrates.objects.get(
            bitrate=configuration[BITRATE_K]
        ),\
        bands.AvailableBandwidths.objects.get(
            bandwidth=configuration[BANDWIDTH_K]
        ),\
        bands.AvailablePolarizations.objects.get(
            polarization=configuration[POLARIZATION_K]
        )


def deserialize_gs_channel_parameters(configuration):
    """
    This method gets a list of the objects of the database based on the list
    of identifiers provided.
    :param configuration: The configuration structure with all the data.
    :return: Tuple containing all parameters as separate variables.
    """
    check_gs_channel_configuration(configuration)

    mod_l = []
    bps_l = []
    bws_l = []
    pol_l = []

    for e_i in configuration[MODULATIONS_K]:
        mod_l.append(bands.AvailableModulations.objects.get(modulation=e_i))
    for e_i in configuration[BITRATES_K]:
        bps_l.append(bands.AvailableBitrates.objects.get(bitrate=e_i))
    for e_i in configuration[BANDWIDTHS_K]:
        bws_l.append(bands.AvailableBandwidths.objects.get(bandwidth=e_i))
    for e_i in configuration[POLARIZATIONS_K]:
        pol_l.append(bands.AvailablePolarizations.objects.get(polarization=e_i))

    return (
        configuration[BAND_K],
        configuration[AUTOMATED_K],
        mod_l, bps_l, bws_l, pol_l
    )


def serialize_once_dates(rule, child_rule):
    """
    Function that serializes the dates from a once rule object as taken from
    the database.
    :param rule: The parent rule to be fully serialized.
    :return: An object serializable structure.
    """
    return {
        RULE_ONCE_DATE: common_serial.serialize_iso8601_date(
            rule.starting_date
        ),
        RULE_ONCE_S_TIME: common_serial.serialize_iso8601_time(
            child_rule.starting_time
        ),
        RULE_ONCE_E_TIME: common_serial.serialize_iso8601_time(
            child_rule.ending_time
        )
    }


def serialize_daily_dates(rule, child_rule):
    """
    Function that serializes the dates from a daily rule object as taken from
    the database.
    :param rule: The daily rule to be serialized.
    :return: An object serializable structure.
    """
    return {
        RULE_DAILY_I_DATE: common_serial.serialize_iso8601_date(
            rule.starting_date
        ),
        RULE_DAILY_F_DATE: common_serial.serialize_iso8601_date(
            rule.ending_date
        ),
        RULE_S_TIME: common_serial.serialize_iso8601_time(
            child_rule.starting_time
        ),
        RULE_E_TIME: common_serial.serialize_iso8601_time(
            child_rule.ending_time
        )
    }


def serialize_weekly_dates(rule, child_rule):
    """
    Function that serializes the dates from a weekly rule object as taken from
    the database.
    :param rule: The reference to the dates as taken from the database.
    :return: An object serializable structure.
    """
    dates = []
    for d in RULE_WEEKLY_WEEKDAYS:
        dates.append({
            RULE_WEEKLY_DATE_DAY: d,
            RULE_S_TIME: common_serial.serialize_iso8601_time(
                child_rule[d + '_starting_time']
            ),
            RULE_E_TIME: common_serial.serialize_iso8601_time(
                child_rule[d + '_ending_time']
            )
        })
    return {
        RULE_DAILY_I_DATE: common_serial.serialize_iso8601_date(
            rule.starting_date
        ),
        RULE_DAILY_F_DATE: common_serial.serialize_iso8601_date(
            rule.ending_date
        ),
        RULE_DATES: dates
    }

__date_serializers__ = {
    RULE_PERIODICITY_ONCE: serialize_once_dates,
    RULE_PERIODICITY_DAILY: serialize_daily_dates,
    RULE_PERIODICITY_WEEKLY: serialize_weekly_dates,
}


def serialize_rules(channel_rules):
    """
    This method serializes in JSON format all the rule objects contained in
    the list given as a parameter.
    :param channel_rules: The array of objects with the rules as read from the
    database.
    :return: JSON structure with all the rules.
    """
    jrules = []
    for r in channel_rules:

        periodicity = __db2net__[r.periodicity]
        child_r = rules.AvailabilityRule.objects.get_specific_rule(r.id)
        serializer = __date_serializers__[periodicity]

        if serializer is None:
            continue

        jrules.append({
            RULE_OP: __db2net__[r.operation],
            RULE_PERIODICITY: __db2net__[r.periodicity],
            RULE_DATES: serializer(r, child_r),
        })

    return jrules


def deserialize_dates(period, dates):
    """
    This method deserializes the dates contained within the parameters required
    by a
    :param period: The period that this rule represents.
    :param dates: The dates object as obtained from the network.
    :return: All the date parameters returned as a N-tuple.
    """
    if period == RULE_PERIODICITY_ONCE:
        return deserialize_once_dates(dates)
    if period == RULE_PERIODICITY_DAILY:
        return deserialize_daily_dates(dates)
    if period == RULE_PERIODICITY_WEEKLY:
        return deserialize_weekly_dates(dates)


def deserialize_once_dates(dates):
    """
    Deserializes the dates as expected within a once dates object.
    :param dates: The dates object.
    :return: A 3-tuple containing all the deserialized date parameters.
    """
    return\
        common_serial.deserialize_iso8601_date(dates[RULE_ONCE_DATE]),\
        common_serial.deserialize_iso8601_time(dates[RULE_ONCE_S_TIME]),\
        common_serial.deserialize_iso8601_time(dates[RULE_ONCE_E_TIME])


def deserialize_daily_dates(dates):
    """
    Deserializes the dates as expected within a daily dates object.
    :param dates: The dates object.
    :return: A 4-tuple containing all the deserialized date parameters (
    initial date, final date, starting daily hour and ending daily hour.
    """
    return\
        common_serial.deserialize_iso8601_date(dates[RULE_DAILY_I_DATE]), \
        common_serial.deserialize_iso8601_date(dates[RULE_DAILY_F_DATE]), \
        common_serial.deserialize_iso8601_time(dates[RULE_S_TIME]),\
        common_serial.deserialize_iso8601_time(dates[RULE_E_TIME])


def deserialize_weekly_dates(dates):
    """
    Since the value for the days of the weeks are not stored within the table
    in the database, in this case the object that is obtained directly from
    the network can be utilized for accessing the database. Therefore,
    only a brief validation of the data contained in that structure is
    necessary.
    :param dates: The days of the week with the time intervals per day.
    :return: The structure with the time intervals per weekday.
    """
    check_weekdays = list(RULE_WEEKLY_WEEKDAYS)
    if dates is None or len(dates) == 0:
        raise Exception('Weekly dates provided is empty.')
    for d in dates:
        if not d in RULE_WEEKLY_WEEKDAYS:
            raise Exception('Day <' + d + '> not supported.')
        if not d in check_weekdays:
            raise Exception('Day <' + d + '> is duplicated.')
        else:
            check_weekdays.remove(d)
    return dates

# Switch-like dictionary for date deserialization functions
__dates_deserialization__ = {
    RULE_PERIODICITY_ONCE: deserialize_once_dates,
    RULE_PERIODICITY_DAILY: deserialize_daily_dates,
    RULE_PERIODICITY_WEEKLY: deserialize_weekly_dates,
}


def deserialize_rule_cfg(rule_cfg):
    """
    This method deserializes the parameters required for the configuration
    of a given rule, as that configuration object is obtained from within the
    network.
    :param rule_cfg: Configuration object as obtained from the network.
    :return: All the parameteres returned as a N-tuple.
    """
    operation = rule_cfg[RULE_OP]
    if not operation in __supported_operations__:
        raise Exception('Operation ' + operation + ' not supported.')

    periodicity = rule_cfg[RULE_PERIODICITY]
    if not periodicity in __supported_periodicities__:
        raise Exception('Period ' + periodicity + ' not supported.')

    dates_reader = __dates_deserialization__[periodicity]
    dates = dates_reader(rule_cfg[RULE_DATES])
    return __net2db__[operation], __net2db__[periodicity], dates


def serialize_channels(channel_list):
    """
    Transform a list of channels into a JSON-like array with the identifiers
    of the channels.
    :param channel_list: list with the channel objects from the database.
    :return: JSON-like array with the identifiers of the channels.
    """
    return {
        CHANNEL_LIST_K: [c.identifier for c in channel_list]
    }


def serialize_sc_configuration(sc):
    """
    Internal method for serializing the complete configuration of a
    SpacecraftConfiguration object.
    :param sc: The object to be serialized.
    :return: The serializable version of the object.
    """
    return {
        SC_ID_K: sc.identifier,
        SC_CALLSIGN_K: sc.callsign,
        SC_TLE_ID_K: sc.tle.identifier,
    }


def deserialize_sc_configuration(configuration):
    """
    This method de-serializes the parameters for a Ground Station as provided
    in the input configuration parameter.
    :param configuration: Structure with the configuration parameters for the
                            Ground Station.
    :return: All the parameteres returned as a N-tuple (callsign, tle_id)
    """

    callsign = None
    tle_id = None

    if SC_CALLSIGN_K in configuration:
        callsign = configuration[SC_CALLSIGN_K]
    if SC_TLE_ID_K in configuration:
        tle_id = configuration[SC_TLE_ID_K]

    return callsign, tle_id


def serialize_gs_configuration(gs):
    """
    Internal method for serializing the complete configuration of a
    GroundStationConfiguration object.
    :param gs: The object to be serialized.
    :return: The serializable version of the object.
    """
    return {
        GS_ID_K: gs.identifier,
        GS_CALLSIGN_K: gs.callsign,
        GS_ELEVATION_K: gs.contact_elevation,
        GS_LATLON_K: [gs.latitude, gs.longitude],
        GS_ALTITUDE_K: gs.altitude
    }


def deserialize_gs_configuration(configuration):
    """
    This method de-serializes the parameters for a Ground Station as provided
    in the input configuration parameter.
    :param configuration: Structure with the configuration parameters for the
                            Ground Station.
    :return: All the parameteres returned as a N-tuple.
    """

    callsign = None
    contact_elevation = None
    latitude = None
    longitude = None

    if GS_CALLSIGN_K in configuration:
        callsign = configuration[GS_CALLSIGN_K]
    if GS_ELEVATION_K in configuration:
        contact_elevation = configuration[GS_ELEVATION_K]
    if GS_LATLON_K in configuration:
        latlon = configuration[GS_LATLON_K]
        latitude = latlon[0]
        longitude = latlon[1]

    return callsign, contact_elevation, latitude, longitude