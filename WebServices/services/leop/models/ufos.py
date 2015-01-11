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

from django.db import models as django_models


class UnknownObject(django_models.Model):
    """LEOP Cluster database model.
    Database model that manages the information relative to a given leop of
    satellites during the LEOP phases.
    """
    class Meta:
        app_label = 'leop'

    identifier = django_models.PositiveSmallIntegerField('Object identifier')