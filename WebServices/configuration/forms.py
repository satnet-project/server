import logging
logger = logging.getLogger(__name__)

from django.forms import Form, ModelForm, HiddenInput, Textarea, CharField
from django.utils.translation import ugettext_lazy as _

from configuration.models import GroundStationConfiguration

class AddGroundStationForm(ModelForm):

    contact_elevation = CharField(label=_("Elevation (deg)")) 
    
    class Meta:
    
        model = GroundStationConfiguration
        fields = ( 'user', 'identifier', 'callsign', 'contact_elevation', \
                    'latitude', 'longitude' )
        widgets = {
            'user' : HiddenInput(),
            'latitude' : HiddenInput(),
            'longitude' : HiddenInput(),
        }

