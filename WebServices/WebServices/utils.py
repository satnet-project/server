import traceback

def get_traceback_as_str():
    """
    This method simply returns a string that contains the frames of the current
    traceback stack.
    """

    return ''.join(str(e) for e in traceback.format_stack())

"""
# ### (patch-begin)
        if username:
            logger.debug(">>>> " + __name__ + ", redirect_to_login, 1")
            m = md5()
            m.update(username)
            mark = m.digest()
            logger.debug(">>>> " + __name__ + ", redirect_to_login, user = " \
                                + username \
                                + ", mark = " + m.hexdigest())
            querystring[prev_user_field_name] = m.hexdigest()
# ### (patch-end)
"""

