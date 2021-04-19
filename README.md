Currently only supports failed step functions. This is half-baked so far

# Usage

```python
# settings.py

INSTALLED_APPS = [
  "django_serverless_emailer",
  # ...
]

AWS_REGION = "us-west-2"  # your region

DEFAULT_FROM_EMAIL = "an-email@email.com"  # your sender
EMAIL_HOST = "smtp.gmail.com"  # your host
EMAIL_PORT = 465  # your port
EMAIL_HOST_USER = "an-email@email.com"  # your user
EMAIL_HOST_PASSWORD = os.getenv["EMAIL_PASSWORD"]
EMAIL_USE_SSL = True  # if you're using SSL

EMAIL_RECEPIENTS = "a@b.com,c@d.com"  # comma delimited list or a plain list
```

```yml
# serverless.yml

functions:
  notify:
    handler: path/to/handler.send_email
    description: Send an email
    layers:
      - { Ref: PythonRequirementsLambdaLayer }
```

```python
# handler.py

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

from django_serverless_emailer import notify


def send_email(event, _):
    notify(event, _)

```
