import logging
logger = logging.getLogger(__name__)

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from configuration.forms import AddGroundStationForm
from configuration.models import GroundStationConfiguration
from configuration.utils import get_remote_user_location

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
        form = self.form_class(initial={ 'user' : user.id, \
                                            'latitude' : latitude, \
                                            'longitude' : longitude })        
        context = RequestContext(request, { 'form' : form })
        
        return(TemplateResponse(request, self.template_name, context))

class ListGroundStationsView(ListView):

    model = GroundStationConfiguration
    template_name = 'list_groundstations.html'
    context_object_name = "groundstations_list"     # list for the template

    def get_queryset(self):
    
        user = User.objects.get(username=self.request.user.username)
        return GroundStationConfiguration.objects.filter(user=user.id)

