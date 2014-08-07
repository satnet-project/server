from twisted.cred.credentials import IUsernamePassword
from commands import *
from twisted.cred.error import UnauthorizedLogin


class UnhandledCredentials(Exception):
    """
    L{login} was passed a credentials object which did not provide a 
    recognized credentials interface.
    """

def login(client, credentials):
    """
    Begin the authentication process by asking the server to verify the 
    user credentials using the given L{AMP} instance. The protocol must 
    be connected to a server with responders for L{PasswordLogin}.

    :param client:
        A connected L{AMP} instance which will be used to issue remote 
        authentication commands.
    :type client:
        L{AMP}
    :param credentials: 
        An L{IUsernamePassword} object containing the user credentials 
        which will be send to the server.
    :type credentials:
        L{IUsernamePassword}

    :return: 
        A L{Deferred} which fires when authentication has succeeded or
        which fails with L{UnauthorizedLogin} if the server rejects the
        authentication attempt.
    :rtype:
        L{Deferred}
    """
    if not IUsernamePassword.providedBy(credentials):
        raise UnhandledCredentials()
    
    print "Login attempt: " + credentials.username
    d = client.callRemote(
        PasswordLogin, sUsername=credentials.username, sPassword=credentials.password)
    def result(_ignored):
        return True
    d.addCallback(result)
    def trapUnauthorizedLogin(result):
       raise UnauthorizedLogin()
    d.addErrback(trapUnauthorizedLogin)

    return d.addCallback(lambda ignored: client)
