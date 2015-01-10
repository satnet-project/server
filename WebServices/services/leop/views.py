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

from django.core import urlresolvers as django_resolvers
from django.views.generic import list as list_views, edit as edit_views
import socket
from services.accounts import models as account_models
from services.configuration.models import tle as tle_models
from services.leop import forms as leop_forms
from services.leop.models import launch as leop_models


class LeopCreateView(edit_views.CreateView):
    """LEOP Manager create view.
    """
    model = leop_models.Launch
    form_class = leop_forms.LeopForm
    template_name = 'staff/leop_create.html'
    success_url = django_resolvers.reverse_lazy('leop_management')

    @staticmethod
    def generate_cluster_tle_source(leop_id):
        """K generator
        Generates the source for the TLE for a given LEOP cluster.
        :param leop_id: Identifier of the LEOP cluster
        :return: String with the source for the TLE
        """
        return 'tle://' + socket.getfqdn() +\
               '/leop/' + str(leop_id) + '/cluster'

    @staticmethod
    def generate_cluster_tle_id(leop_id):
        """K generator
        Generates the identifier for the TLE for a given LEOP cluster.
        :param leop_id: Identifier of the LEOP cluster
        :return: String with the identifier
        """
        cluster_tle_id = 'leop:' + str(leop_id) + ':cluster'
        return cluster_tle_id[0:(tle_models.TwoLineElement.MAX_TLE_ID_LEN - 1)]

    def form_valid(self, form):
        """Method executed after ther form is found valid.
        It is necessary to override this method for adding the admin of the
        cluster taken from the username included in the request.
        """
        form.instance.admin = account_models.UserProfile.objects.get(
            username=self.request.user
        )
        tle_id = LeopCreateView.generate_cluster_tle_id(
            form.instance.identifier
        )
        tle_source = LeopCreateView.generate_cluster_tle_source(
            form.instance.identifier
        )
        form.instance.cluster_tle = tle_models.TwoLineElement.objects.create(
            source=tle_source,
            l0=tle_id,
            l1=form.cleaned_data['tle_l1'],
            l2=form.cleaned_data['tle_l2']
        )
        return super(LeopCreateView, self).form_valid(form)


class LeopUpdateView(edit_views.UpdateView):
    """LEOP Manager Update view.
    """
    model = leop_models.Launch
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'
    form_class = leop_forms.LeopForm
    template_name = 'staff/leop_update.html'
    success_url = django_resolvers.reverse_lazy('leop_management')

    def get_context_data(self, **kwargs):

        context = super(LeopUpdateView, self).get_context_data(**kwargs)
        context['cluster_id'] = self.kwargs['identifier']
        return context


class LeopDeleteView(edit_views.DeleteView):
    """LEOP Manager delete view.
    """
    model = leop_models.Launch
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'
    template_name = 'staff/leop_confirm_delete.html'
    success_url = django_resolvers.reverse_lazy('leop_management')


class LeopManagementView(list_views.ListView):
    """
    This class helps in handling how users are shown to the network
    administrator, so that their activation can be initiated. This is the
    second step of the registration process, that takes place after a user has
    sent the registration request.
    """
    model = leop_models.Launch
    context_object_name = 'cluster_list'
    template_name = 'staff/leop_management.html'

    def get_queryset(self):
        """QuerySet handler.
        Returns the set of LEOP spacecraft that are owned by the current user
        making the requests.
        """
        return self.model.objects.filter(
            admin=account_models.UserProfile.objects.get(
                username=self.request.user
            )
        )