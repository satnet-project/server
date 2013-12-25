import logging
logger = logging.getLogger(__name__)


from django.contrib.auth.decorators import login_required

from jsonview.decorators import json_view
from jsonview.exceptions import BadRequest

from configuration.models import AvailableModulations

@json_view
@login_required
def get_available_modulations(request):
    """
    AJAX GET method for retrieving available ground station configuration
    channel options.
    """
    
    logger.info(__name__ + ',  get_available_modulations(AJAX)')
    
    available_modulations = AvailableModulations.objects.all()
    return available_modulations

