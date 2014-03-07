from django_countries import CountryField
from django.utils.translation import ugettext_lazy as _
from django.db import models

from account.models import Account
from account.conf import settings

class snAccount(models.Model):

    #account = models.OneToOneField(Account,\
    #                                    related_name="sn_account",\
    #                                    verbose_name=_("snAccount"))

    account = models.ForeignKey(Account)

    organization = models.CharField(_("language"),
        max_length=10,
        choices=settings.ACCOUNT_LANGUAGES,
        default=settings.LANGUAGE_CODE
    )
    
    country = CountryField()

    @classmethod
    def create(cls, request=None, **kwargs):
        """    
        Factory method that creates a new instance of the Account class. This
        instance contains the original data of the Account class as taken from
        the django-user-accounts library and adds extra information fields.
        """
        create_email = kwargs.pop("create_email", True)
        user = kwargs.pop("user", None)
        acc = Account.create(request, user=user, create_email=create_email)
        x_account = cls(**kwargs)
        x_account.user = request.user
        x_account.save()
        return x_account
        
