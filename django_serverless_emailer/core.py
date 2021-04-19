from django_serverless_emailer.sources import STEP_FUNCTIONS

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_notification_email(event, context, template=None):
    source = event["source"]
    detail = event["detail"]
    detail_type = event["detail-type"]
    region = settings.AWS_REGION
    if source == STEP_FUNCTIONS:
        execution_arn = detail["executionArn"]
        input_ = detail["input"]
        status = detail["status"]

        subject = f"{detail_type} - {status}"

        template = (
            template if template else "django_serverless_emailer/step-function.html"
        )

        html = render_to_string(
            template,
            {"region": region, "execution_arn": execution_arn, "input": input_},
        )
    else:
        raise AssertionError(
            f"{source} is not yet implemented in django-serverless-emailer"
        )

    recipients = settings.EMAIL_RECEPIENTS
    if type(recipients) == str:
        recipients = recipients.split(",")

    plain = strip_tags(html)

    send_mail(
        subject,
        plain,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        html_message=html,
    )