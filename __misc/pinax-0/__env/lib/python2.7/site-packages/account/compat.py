from django.conf import settings

import django.contrib.auth
from django.contrib.auth.models import User


AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


def get_user_model():
    if hasattr(django.contrib.auth, "get_user_model"):
        return django.contrib.auth.get_user_model()
    else:
        return User
