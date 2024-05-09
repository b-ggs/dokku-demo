import os
from textwrap import dedent

import apprise
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from dokku_demo.celery import app


@app.task()
def send_message(message: str) -> bool:
    apobj = apprise.Apprise()

    if not (notification_apprise_url := settings.NOTIFICATION_APPRISE_URL):
        raise ImproperlyConfigured("NOTIFICATION_APPRISE_URL is unset.")

    apobj.add(notification_apprise_url)

    notification_title = "New message!"

    notification_body = dedent(
        f"""
        {message}
        This message was sent from a Docker container with the environment variables:
        - HOSTNAME: {os.getenv("HOSTNAME", "")}
        - DYNO: {os.getenv("DYNO", "")}
        """
    ).strip()

    return apobj.notify(
        body=notification_body,
        title=notification_title,
    )
