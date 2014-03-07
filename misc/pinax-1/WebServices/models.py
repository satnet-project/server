from django_countries import CountryField
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone, translation
from django.utils.translation import gettext_lazy as _

from account.conf import settings
from account.fields import TimeZoneField
from account.models import AnonymousAccount

"""
The Account class holds additional data fields to be added to the default ones
hold by the original Account class from django-user-accounts.
"""
class Account(models.Model):

    user = models.OneToOneField(User, related_name="Account",\
                                 verbose_name=_("Account"))
    timezone = TimeZoneField(_("timezone"))
    language = models.CharField(_("language"),
        max_length=10,
        choices=settings.ACCOUNT_LANGUAGES,
        default=settings.LANGUAGE_CODE
    )

    # Extra fields
    organization = models.CharField(_("language"), max_length=10)
    country = CountryField()

    @classmethod
    def for_request(cls, request):
        if request.user.is_authenticated():
            try:
                account = Account._default_manager.get(user=request.user)
            except Account.DoesNotExist:
                account = AnonymousAccount(request)
        else:
            account = AnonymousAccount(request)
        return account

    @classmethod
    def create(cls, request=None, **kwargs):
        create_email = kwargs.pop("create_email", True)
        confirm_email = kwargs.pop("confirm_email", None)
        account = cls(**kwargs)
        if "language" not in kwargs:
            if request is None:
                account.language = settings.LANGUAGE_CODE
            else:
                account.language = translation.get_language_from_request(request, check_path=True)
        account.save()
        if create_email and account.user.email:
            kwargs = {"primary": True}
            if confirm_email is not None:
                kwargs["confirm"] = confirm_email
            EmailAddress.objects.add_email(account.user, account.user.email, **kwargs)
        return account

    def __unicode__(self):
        return self.user.username

    def now(self):
        """
        Returns a timezone aware datetime localized to the account's timezone.
        """
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))
        timezone = settings.TIME_ZONE if not self.timezone else self.timezone
        return now.astimezone(pytz.timezone(timezone))

    def localtime(self, value):
        """
        Given a datetime object as value convert it to the timezone of
        the account.
        """
        timezone = settings.TIME_ZONE if not self.timezone else self.timezone
        if value.tzinfo is None:
            value = pytz.timezone(settings.TIME_ZONE).localize(value)
        return value.astimezone(pytz.timezone(timezone))

