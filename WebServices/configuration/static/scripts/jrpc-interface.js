/**
 * Copyright 2013, 2014 Ricardo Tubio-Pardavila
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * This class handles all the remote procedure calls through JRPC. A common
 * JRPC client object is shared among all these calls.
 *
 * Each of this remote procedure call must be provided with a callback
 * function, so that after the call is completed, that function is called back
 * with the data coming from the server as the 'result' input parameter.
 *
 * In case an error occurs during the call to the remote JRPC method, a common
 * error function for all this methods is called. This function simply logs the
 * event and raises an 'alert' message to the user.
 *
 * @author rtubiopa[at]calpoly.edu
 * @constructor
 */
function ConfigurationService_JRPC() {

    /** JRPC key for exchanging the identifier of the Channel. */
    this.CH_ID = 'channel_id';
    /** JRPC key for exchaning the name of the band for a given channel. */
    this.CH_BAND = 'band';
    /** JRPC key for exchanging the list of modulations. */
    this.CH_MODS = 'modulations';
    /** JRPC key for exchanging the list of bitrates. */
    this.CH_BPS = 'bitrates';
    /** JRPC key for exchanging the list of bandwidths. */
    this.CH_BWS = 'bandwidths';
    /** JRPC key for exchanging the list of polarizations. */
    this.CH_POL = 'polarizations';
    /** JRPC key for exchanging a complete configuration structure. */
    this.CH_CFG = 'configuration';

    /** JRPC key for exchanging the identifier of the Ground Station. */
    this.GS_ID = 'groundstation_id';
    /** JRPC key for exchanging the coordinates of the Ground Station. */
    this.GS_LATLON = 'groundstation_latlon';
    /** JRPC key for exchanging the identifier of the Ground Station. */
    this.GS_CALLSIGN = 'groundstation_callsign';
    /** JRPC key for exchanging the elevation of the Ground Station. */
    this.GS_ELEVATION = 'groundstation_elevation';
    /** JRPC key for exchanging the channels of the Ground Station. */
    this.GS_CHANNELS = 'groundstation_channels';

    /** JRPC key for exchanging the type of operation for this rule. */
    this.RULE_OP = 'rule_operation';
    /** JRPC key for slots addition rules. */
    this.RULE_OP_ADD = '+';
    /** JRPC key for slots removal rules. */
    this.RULE_OP_REMOVE = '-';
    /** JRPC key for exchanging the period for this rule. */
    this.RULE_PERIODICITY = 'rule_periodicity';
    /** JRPC key for exchanging the period for this rule. */
    this.RULE_PERIODICITY_ONCE = 'rule_periodicity_once';
    /** JRPC key for exchanging the period for this rule. */
    this.RULE_PERIODICITY_DAILY = 'rule_periodicity_daily';
    /** JRPC key for exchanging the period for this rule. */
    this.RULE_PERIODICITY_WEEKLY = 'rule_periodicity_weekly';
    /** JRPC key for exchanging availability dates. */
    this.RULE_DATES = 'rule_dates';
    /** JRPC key for exchanging the date of ocurrence of this event. */
    this.RULE_ONCE_DATE = 'rule_once_date';
    /** JRPC key for exchanging the initial date for a once-time rule. */
    this.RULE_ONCE_S_TIME = 'rule_once_starting_time';
    /** JRPC key for exchanging the final date for a once-time rule. */
    this.RULE_ONCE_E_TIME = 'rule_once_ending_time';
    /** JRPC key for exchanging the initial date for a daily rule. */
    this.RULE_DAILY_I_DATE = 'rule_daily_initial_date';
    /** JRPC key for exchanging the final date for a daily rule. */
    this.RULE_DAILY_F_DATE = 'rule_daily_final_date';
    /** JRPC key for exchanging the stating time for a daily rule. */
    this.RULE_S_TIME = 'rule_starting_time';
    /** JRPC key for exchanging the ending time for a daily rule. */
    this.RULE_E_TIME = 'rule_ending_time';
    /** JRPC key for exchanging the day of the week. */
    this.RULE_WEEKLY_DATE = 'rule_weekly_date';
    /** JRPC key for exchanging the day of the week. */
    this.RULE_WEEKLY_DATE_DAY = 'rule_weekly_date_day';
    /** JRPC keys for the weekdays. */
    this.RULE_WEEKDAYS =
        ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday', 'sunday'];

    /**
     * Inner JRPC common client for all JRPC calls.
     *
     * @type {JsonRpcClient}
     * @private
     */
    this._JRPCClient = new $.JsonRpcClient({ ajaxUrl: '/jrpc/' });

    /**
     * Inner common method for all the invokations of a JRPC call to use the
     * same object.
     *
     * @param method Name of the method remotely invoked.
     * @param parameters Parameters required by that method (array).
     * @param __cb Callback function to be called back after a correct method
     *              execution.
     * @param logMessage Message providing additional information.
     * @private
     */
    this._makeJRPCCall = function (method, parameters, __cb, logMessage) {
        this._logJRPC(method, parameters, logMessage);
        this._JRPCClient.call(method, parameters, __cb, this._JRPCError);
    };

    /**
     * Method for logging a JRPC call.
     *
     * @param method Name of the method remotely invoked.
     * @param parameters Parameters required by that method (array).
     * @param message Message providing additional information.
     * @private
     */
    this._logJRPC = function(method, parameters, message) {
        if ( ( message == null ) || ( message == '' ) )
            { message = '(no additional info)'; }
        if (__DEBUG__) console.log('>>> JRPC call (' + method
                                    + '), params = ' + parameters
                                    + ', reason = ' + message);
    };

    /**
     * Common error handling function. This function is called automatically by
     * the JRPC client objects each time an error occurs during the
     * communications or an error is returned as a result of the execution of
     * the remote procedure.
     *
     * @param error The error object in accordance with JRPC client object's
     *              output.
     * @private
     */
    this._JRPCError = function(error)
        { __log_error(error['message']); };

/*
/////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////// JRPC Methods
/////////////////////////////////////////////////////////////////////////////
 */

    /**
     * Remote method for getting all the options available for the different
     * parameters that define the configuration of a channel.
     *
     * @param __cb Callback function to be called back with the result provided
     *              by a correct execution of the remote procedure.
     */
    this.getChannelOptions = function(__cb) {
        this._makeJRPCCall('configuration.gs.channel.getOptions',
                            [], __cb, ''
    );};

    /**
     * Remote method for checking whether the given channel identifier already
     * exists in the database or not.
     *
     * @param __cb Callback function to be called back with the result provided
     *              by a correct execution of the remote procedure.
     * @param ch_id The identifier of the channel whose uniqueness needs to be
     *              checked.
     */
    this.verifyChannelId = function(__cb, ch_id) {
        this._makeJRPCCall('configuration.gs.channel.isUnique',
                            [ ch_id ], __cb, ''
    );};

    /**
     * Remote method for creating a channel associated to a Ground Station.
     *
     * @param __cb Callback function to be called back with the result provided
     *              by a correct execution of the remote procedure.
     * @param gs_id Ground Station that owns this channel.
     * @param ch_id The identifier for the new channel.
     * @param ch_cfg The configuration for the new channel.
     * @constructor
     */
    this.createChannel = function(__cb, gs_id, ch_id, ch_cfg) {
        this._makeJRPCCall('configuration.gs.channel.create',
                            [ gs_id, ch_id, ch_cfg ], __cb, ''
    );};

    /**
     * Remote method for deleting the given channel.
     *
     * @param __cb Callback function to be called back with the result provided
     *              by a correct execution of the remote procedure.
     * @param gs_id Ground Station that owns this channel.
     * @param ch_id The identifier for the new channel.
     */
    this.deleteChannel = function(__cb, gs_id, ch_id) {
        this._makeJRPCCall('configuration.gs.channel.delete',
                            [ gs_id, ch_id ], __cb, ''
    );};

    /**
     * Returns the configuration for the given channel that is owned by the
     * given Ground Station.
     *
     * @param __cb Callback function to be called back with the result provided
     *              by a correct execution of the remote procedure.
     * @param gs_id Ground Station that owns this channel.
     * @param ch_id The identifier for the new channel.
     */
    this.getChannelConfiguration = function(__cb, gs_id, ch_id) {
        this._makeJRPCCall('configuration.gs.channel.getConfiguration',
                            [gs_id, ch_id], __cb, ''
    );};

    /**
     * Sets the configuration for the given channel that is owned by the given
     * Ground Station.
     *
     * @param __cb Callback function to be called back with the result provided
     *              by a correct execution of the remote procedure.
     * @param gs_id Ground Station that owns this channel.
     * @param ch_id The identifier for the new channel.
     * @param cfg Configuration to be set for this Ground Station.
     */
    this.setChannelConfiguration = function(__cb, gs_id, ch_id, cfg) {
        this._makeJRPCCall('configuration.gs.channel.setConfiguration',
                            [gs_id, ch_id, cfg], __cb, ''
    );};

    /**
     * Deletes the given Ground Station.
     *
     * @param __cb Callback function to be called back with the result provided
     *              by a correct execution of the remote procedure.
     * @param gs_id Ground Station identifier.
     */
    this.deleteGroundStation = function(__cb, gs_id) {
        this._makeJRPCCall('configuration.gs.delete',
                            [gs_id], __cb, ''
    );};

    /**
     * Returns the configuration of the given Ground Station.
     *
     * @param __cb Callback function to be called back with the result provided
     *              by a correct execution of the remote procedure.
     * @param gs_id Ground Station identifier.
     */
    this.getGroundStationConfiguration = function(__cb, gs_id) {
        this._makeJRPCCall('configuration.gs.getConfiguration',
                            [gs_id], __cb, ''
    );};

    /**
     * Sets the configuration of the given Ground Station.
     *
     * @param __cb Callback function to be called back with the result provided
     *              by a correct execution of the remote procedure.
     * @param gs_id Ground Station identifier.
     * @param cfg New configuration values for the Ground Station.
     */
    this.setGroundStationConfiguration = function(__cb, gs_id, cfg) {
        this._makeJRPCCall('configuration.gs.setConfiguration',
                            [gs_id, cfg], __cb, ''
    );};

    /**
     * Gets a list with the identifiers of all the channels owned by the
     * given Ground Station.
     *
     * @param __cb Callback function to be called back with the result provided
     *              by a correct execution of the remote procedure.
     * @param gs_id Ground Station identifier.
     */
    this.getGroundStationChannels = function(__cb, gs_id) {
        this._makeJRPCCall('configuration.gs.getChannels',
                            [gs_id], __cb, ''
    );};

    /**
     * Sets a new rule for the definition of the availability of a channel for
     * a given ground station.
     *
     * @param __cb Callback function to be called back with the result provided
     *              by a correct execution of the remote procedure.
     * @param gs_id Ground Station that owns this channel.
     * @param ch_id The identifier for the new channel.
     * @param rule_cfg Configuration parameters for this availability rule.
     */
    this.addAvailabilityRule = function(__cb, gs_id, ch_id, rule_cfg) {
        this._makeJRPCCall('configuration.gs.channel.addRule',
                            [gs_id, ch_id, rule_cfg], __cb, ''
    );};

}
