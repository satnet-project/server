# First of all we need to add satnet-release-1/WebServices to the path
# to import Django modules
import os, sys
sys.path.append(os.path.dirname(os.getcwd())+"/WebServices")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

# Import your models for use in your script
from zope.interface import implements, Interface
from twisted.python import log
from twisted.cred import portal, checkers, credentials
from twisted.cred.error import UnauthorizedLogin
from twisted.internet import defer
from twisted.protocols.amp import IBoxReceiver
from twisted.internet import reactor

from django.contrib.auth.models import User

from server_amp import Server


"""
Verifies the user credentials against the Django users DB.
"""
class DjangoAuthChecker:
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def _passwordMatch(self, matched, user):
        if matched:
            log.msg('User ' + user.username + ' -> correct password')
            return user
        else:
            
            raise UnauthorizedLogin('Incorrect password')

    def requestAvatarId(self, creds):
        try:
            user = User.objects.get(username=creds.username)
            if user.check_password(creds.password):
                log.msg('User authenticated correctly')
            return defer.maybeDeferred(user.check_password,
                creds.password).addCallback(self._passwordMatch, user)
        except User.DoesNotExist:
            return defer.fail(UnauthorizedLogin('Incorrect username'))


class Realm:
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IBoxReceiver in interfaces:
            print avatarId
            return (IBoxReceiver, Server(), lambda: None)
        raise NotImplementedError()