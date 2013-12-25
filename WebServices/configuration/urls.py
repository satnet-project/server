from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from configuration.views import AddGroundStationView, ListGroundStationsView,\
                                ConfigureGroundStationView

urlpatterns = patterns('',

    url(r'^list_groundstations$', \
           login_required(ListGroundStationsView.as_view()), \
           name='list_groundstations'),
    url(r'^add_groundstation/$', \
            login_required(AddGroundStationView.as_view()), \
            name='add_groundstation'),
    url(r'^configure_groundstation/(?P<pk>\d+)$', \
            login_required(ConfigureGroundStationView.as_view()), \
            name='configure_groundstation'),
)

