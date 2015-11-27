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

from django.views.generic import list as list_views
from services.configuration.models import segments as segment_models
from services.communications import models as comms_models


class PassiveMessages(list_views.ListView):
    """
    This class loads the messages uploaded by one user.
    """
    model = comms_models.PassiveMessage
    context_object_name = 'message_list'
    template_name = 'users/messages.html'
    paginate_by = 10

    def get_queryset(self):
        """QuerySet handler.
        Returns the set of LEOP spacecraft that are owned by the current user
        making the requests.
        """
        # noinspection PyUnresolvedReferences
        user_groundstations = segment_models.GroundStation.objects.filter(
            user=self.request.user
        ).all()
        return self.model.objects.filter(
            groundstation__in=user_groundstations
        )
