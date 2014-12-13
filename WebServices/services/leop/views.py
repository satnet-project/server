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
from services.leop import models as cluster_models


class ClusterManagementView(list_views.ListView):
    """
    This class helps in handling how users are shown to the network
    administrator, so that their activation can be initiated. This is the
    second step of the registration process, that takes place after a user has
    sent the registration request.
    """
    model = cluster_models.Cluster
    template_name = 'cluster_management.html'
    #queryset = cluster_models.Cluster.objects.all()
    context_object_name = 'cluster_list'

    def get_queryset(self):
        """QuerySet handler.
        Returns the set of clusters that are owned by the current user
        making the requests.
        """
        return cluster_models.Cluster.objects.filter(admin=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        POST method handler. This method is invoked once the submit button of
        the form is pressed.
        """
        #operations = utils.get_user_operations-(request.POST)
        #self.apply_user_operations(operations)
        return self.get(request, *args, **kwargs)