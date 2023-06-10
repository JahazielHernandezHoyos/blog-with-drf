# from sendgrid import SendGridAPIClient
import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from jinja2 import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from apps.utils.redis import client as redis


def send_email(subject: str, to_email: str, template: str, context: dict):
    """
    Send email to user

    Args:
        subject (str): Subject of the email.
        to_email (str): Email address of the recipient.
        template (str): Email template.
        context (dict): Context data for the template.

    Returns:
        SendGrid response.
    """
    template_id = "d-59a3ad2c8b2f49c482f5627463e1b11c"
    message = Mail(
        from_email=os.getenv("SENDGRID_FROM_EMAIL"),
        to_emails=to_email,
        subject=subject,
    )
    message.template_id = template_id
    message.dynamic_template_data = context
    sg = SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
    response = sg.send(message)
    return response


def send(**kwargs):
    from_email = ""
    subject = kwargs.get("subject")
    to_email = kwargs.get("to_email")
    template = kwargs.get("template")
    context = kwargs.get("context")

    setup = redis.get_json("setup")
    settings.EMAIL_HOST = setup.get("email_host")
    settings.EMAIL_HOST_USER = setup.get("email_host_user")

    template = get_template(template)
    html_template = template.render(context)
    msg = EmailMultiAlternatives(subject, subject, from_email, to=[to_email])
    msg.attach_alternative(html_template, "text/html")
    msg.send()
    return kwargs


# def send_email(subject: str, to_email: str, context: dict, template_id: str):
# """
# Send email to user, receiving a template and context
# Parameters
# ----------
# subject : str The subject of the email
# to_email : str The email of the recipient
# context : dict The context variables to render
# template_id : str The template name to render

# data = {
#     "personalizations": [
#         {
#             "to": [{"email": to_email}],
#             "dynamic_template_data": context,
#             "subject": subject,
#         }
#     ],
#     "from": {"email": os.getenv("FROM_EMAIL")},
#     "template_id": template_id,
#     "subject": subject,
# }
# sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
# response = sg.client.mail.send.post(request_body=data)
# return response"""
