"""
Jinja2 environment configuration for the procurement system.
"""

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


def environment(**options):
    """
    Configure Jinja2 environment with Django-specific functions.
    """
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env

