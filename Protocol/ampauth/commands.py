from twisted.protocols import amp
from twisted.cred.error import UnauthorizedLogin


class PasswordLogin(amp.Command):
    """
    Command to authenticate an user.  The server response is a boolean
    granting or not the access to the client.

    :param sUsername:
        Client username for the SATNET network
    :type sUsername:
        String
    :param sPassword:
        Plain-text client password for the SATNET network
    :type sPassword:
        String

    :returns bAuthenticated:
        True if the user has been granted access and L{UnauthorizedLogin}
        otherwise.
    :rtype:
        boolean or L{UnauthorizedLogin}
    """

    arguments = [('sUsername', amp.String()),
    			 ('sPassword', amp.String())]
    response = [('bAuthenticated', amp.Boolean())]
    errors = {
        UnauthorizedLogin: 'UNAUTHORIZED_LOGIN',
        NotImplementedError: 'NOT_IMPLEMENTED_ERROR'}

