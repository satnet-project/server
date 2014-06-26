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
import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.models import User
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from configuration.forms import AddGroundStationForm
from configuration.models.segments import GroundStation
from common.misc import get_remote_user_location


class AddGroundStationView(CreateView):

    template_name = 'add_groundstation.html'
    form_class = AddGroundStationForm
    success_url = '/configuration/list_groundstations'
    
    def get(self, request, *args, **kwargs):
        """
        Process a 'get' request to this view. This is mainly used for getting
        the current IP of the remote user and centering the map where the
        user is going to set the location for the ground station
        """

        # 1) get remote ip and geolocation
        remote_ip = request.META['REMOTE_ADDR']
        latitude, longitude = get_remote_user_location(ip=remote_ip)
        
        # 2) initialize form and context for requests
        user = User.objects.get(username=request.user.username)
        form = self.form_class(
            initial={
                'user': user.id, 'latitude': latitude,
                'longitude': longitude,
                'country': 'US',
                'IARU_region': '1'
            }
        )
        context = RequestContext(request, {'form': form})
        
        return TemplateResponse(request, self.template_name, context)


class ListGroundStationsView(ListView):

    model = GroundStation
    template_name = 'list_groundstations.html'
    context_object_name = 'groundstations_list'

    def get_queryset(self):
    
        user = User.objects.get(username=self.request.user.username)
        return GroundStation.objects.filter(user=user.id)


class ConfigureGroundStationView(DetailView):

    model = GroundStation
    template_name = 'configure_groundstation.html'
    gs_object_name = 'g'
    channels_object_name = 'chs'
    weekdays_object_name = 'weekdays'
    weekdays = [
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
        'sunday'
    ]

    def get_context_data(self, **kwargs):

        context = super(ConfigureGroundStationView, self).get_context_data(
            **kwargs
        )

        context[self.gs_object_name] = self.object
        context[self.channels_object_name] = self.object.channels.all()
        context[self.weekdays_object_name] = self.weekdays

        return context
