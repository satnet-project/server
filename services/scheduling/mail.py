"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'rtubiopa@calpoly.edu'

import logging
logger = logging.getLogger('scheduling')

from django.contrib.auth import models as auth_models
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string


def send_gs_accepted_mail(
    groundstation, spacecraft,
    to=None,
    subject="Slot Request Accepted",
    template="slot-gs-accepted.txt"
):
    """services.scheduling
    Sends an email to the owner of the Spacecraft in order to notify that
    a given slot request has been accepted by the Spacecraft owner.

    :param groundstation: Ground station object
    :param spacecraft: Spacecraft object
    :param to: Destination email
    :param subject: Subject for the email
    :param template: Template with the text for the email
    """
    send_slot_mail(
        groundstation, spacecraft, to=to,
        subject=subject, template=template
    )


def send_gs_denied_mail(
    groundstation, spacecraft,
    to=None,
    subject="Slot Request Denied",
    template="slot-gs-denied.txt"
):
    """services.scheduling
    Sends an email to the owner of the Spacecraft in order to notify that
    a given slot request has been canceled by the Spacecraft owner.

    :param groundstation: Ground station object
    :param spacecraft: Spacecraft object
    :param to: Destination email
    :param subject: Subject for the email
    :param template: Template with the text for the email
    """
    send_slot_mail(
        groundstation, spacecraft, to=to,
        subject=subject, template=template
    )


def send_sc_canceled_mail(
    groundstation, spacecraft,
    to=None,
    subject="Slot Request Canceled",
    template="slot-sc-canceled.txt"
):
    """services.scheduling
    Sends an email to the owner of the Ground Station in order to notify that
    a given slot request has been canceled by the Spacecraft owner.

    :param groundstation: Ground station object
    :param spacecraft: Spacecraft object
    :param to: Destination email
    :param subject: Subject for the email
    :param template: Template with the text for the email
    """
    send_slot_mail(
        groundstation, spacecraft, to=to,
        subject=subject, template=template
    )


def send_slot_mail(
    groundstation, spacecraft,
    to=None,
    subject="Slots Requested",
    subject_tag='[satnet]',
    template="slot-request.txt"
):
    """sevices.scheduling
    Sends an email with the information about the given slot request.

    :param groundstation: Reference to DB's Ground Station object
    :param spacecraft: Reference to DB's Spacecraft object
    :param to: String with the mail destination
    :param subject: Subject for the email
    :param subject_tag: Tag to be added before the given subject
    :param template: TXT template for the email
    """
    if not to:
        raise ValueError('Must specified a destination for the mail')

    ctx = Context({
        'username': spacecraft.user.username,
        'groundstation': groundstation.identifier,
        'spacecraft': spacecraft.identifier
    })

    if not subject:
        subject = 'Slot Reservation'

    subject = subject_tag + ' ' + subject
    from_email = auth_models.User.objects.get(is_superuser=True).email

    message = render_to_string(template, context_instance=ctx)
    EmailMessage(subject, message, to=to, from_email=from_email).send()
