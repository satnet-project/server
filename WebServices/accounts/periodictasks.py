import logging
logger = logging.getLogger(__name__)

from periodically.decorators import daily
from registration.models import RegistrationProfile

@daily()
def accounts_delete_expired_users():
    """
    Task to be executed periodically for cleaning up all users whose activation
    key is expired and they did not complete still their registration process.
    """

    logger.debug("DeleteExpiredUsers, daily task execution!")
    RegistrationProfile.objects.delete_expired_users()

