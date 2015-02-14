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

from dateutil import parser as dt_parser
import pytz
import rpc4django

from services.common import misc
from services.communications import models as comms_models
from services.leop.models import launch as launch_models
from services.leop.jrpc.serializers import messages as messages_serializers


@rpc4django.rpcmethod(
    name='leop.getMessages',
    signature=['String', 'String'],
    login_required=True
)
def get_messages(launch_id, start):
    """JRPC method
    Method that retrieves the messages for this launch that have been received
    since the given start date parameter until right now.
    :param launch_id: Identifier of the launch
    :param start: Datetime start, should be sooner than now.
    :return: Array with objects of the following type:
    {
        groundstation_id: $(groundstation),
        timestamp: $(start_date_isoformat),
        message: $(message)
    }
    """
    if not start:
        raise Exception('<start> value is not valid')

    launch = launch_models.Launch.objects.get(identifier=launch_id)
    launch_gss = launch.groundstations.all()

    # start_dt = pytz.utc.localize(dt_parser.parse(start))
    start_dt = dt_parser.parse(start).astimezone(pytz.utc)
    end_dt = misc.get_now_utc()
    start_ts = misc.get_utc_timestamp(start_dt)
    end_ts = misc.get_utc_timestamp(end_dt)

    messages = comms_models.PassiveMessage.objects.filter(
        groundstation__in=launch_gss,
        groundstation_timestamp__gt=start_ts,
        groundstation_timestamp__lt=end_ts
    )

    return messages_serializers.serialize_messages(messages)