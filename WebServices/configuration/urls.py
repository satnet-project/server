from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from configuration.views import AddGroundStationView, ListGroundStationsView

urlpatterns = patterns('',

    url(r'^add_groundstation/$', \
            login_required(AddGroundStationView.as_view()), \
            name='add_groundstation'),
    url(r'^list_groundstations$', \
           login_required(ListGroundStationsView.as_view()), \
           name='list_groundstations'),

)

