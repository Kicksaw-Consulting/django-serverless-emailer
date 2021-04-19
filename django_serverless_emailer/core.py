import json

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def notify(event, _):
    records = event["Records"]

    for record in records:
        print(record)
        body = json.loads(record["body"])
        detail = body["detail"]
        detail_type = body["detail-type"]
        execution_arn = detail["executionArn"]
        input_ = detail["input"]
        status = detail["status"]

        subject = f"{detail_type} - {status}"

        region = settings.AWS_REGION

        html = render_to_string(
            "django_serverless_emailer/step-function.html",
            {"region": region, "execution_arn": execution_arn, "input": input_},
        )
        plain = strip_tags(html)

        recipients = settings.EMAIL_RECEPIENTS
        if type(recipients) == str:
            recipients = recipients.split(",")

        send_mail(
            subject,
            plain,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            html_message=html,
        )
