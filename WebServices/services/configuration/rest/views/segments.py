"""
   Copyright 2014 Ricardo Tubio-Pardavila

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

from rest_framework import generics, permissions

from services.configuration.models import segments as segment_models
from services.configuration.rest.serializers import segments as \
    segment_serializers


class ListGroundStationsView(generics.ListAPIView):
    """
    View for handling the invocation of the list of ground stations for a
    given user.
    """
    model = segment_models.GroundStation
    serializer_class = segment_serializers.GroundStationSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        """
        Overrides the default queryset method.
        """
        queryset = super(ListGroundStationsView, self).get_queryset()
        return queryset.filter(user__username=self.request.user)


class ListSpacecraftView(generics.ListAPIView):
    """
    View for handling the invocation of the list of spacecraft for a given
    user.
    """
    model = segment_models.Spacecraft
    serializer_class = segment_serializers.SpacecraftSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def get_queryset(self):
        """
        Overrides the default queryset method.
        """
        queryset = super(ListSpacecraftView, self).get_queryset()
        return queryset.filter(user__username=self.request.user)