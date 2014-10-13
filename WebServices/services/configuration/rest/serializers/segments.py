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

from rest_framework import serializers

from services.accounts import serializers as account_serializers
from services.configuration.models import segments as segment_models


class GroundStationSerializer(serializers.ModelSerializer):
    """
    This class serializes a GroundStation object for the REST framework.
    """
    class Meta:
        model = segment_models.GroundStation

    user = account_serializers.UserProfileSerializer(required=False)

    def get_validation_exclusions(self, **kwargs):
        """
        Method that returns the fields to be excluded from the validation
        process. For this model, the field 'user' should be excluded.
        :param **kwargs: additional parameters.
        """
        exclusions = super(GroundStationSerializer, self)\
            .get_validation_exclusions()
        return exclusions + ['user']


class SpacecraftSerializer(serializers.ModelSerializer):
    """
    This class serializes a Spacecraft object for the REST framework.
    """
    class Meta:
        model = segment_models.Spacecraft

    user = account_serializers.UserProfileSerializer(required=False)

    def get_validation_exclusions(self, **kwargs):
        """
        Method that returns the fields to be excluded from the validation
        process. For this model, the field 'user' should be excluded.
        :param **kwargs: additional parameters.
        """
        exclusions = super(SpacecraftSerializer, self)\
            .get_validation_exclusions()
        return exclusions + ['user']