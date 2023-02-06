from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


def send_email_for_confirm(request, user):
    """Collection of user data to form a link letter"""
    current_site = get_current_site(request)
    context = {
        "user": user,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "domain": current_site.domain,
        "token": default_token_generator.make_token(user),
    }
    message = render_to_string('email_verify/send_email.html', context=context)

    EmailMessage('Verify email', message, to=[user.email]).send()
