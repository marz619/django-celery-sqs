from .base import *  # NOQA

"""
Project config & django.conf.settings overrides
"""

# django secret key
from ..secret import KEY as SECRET_KEY
# SQS access/secret key
from ..secret import SQS

"""
AWS celery configuration
"""

from urllib.parse import quote

BROKER_URL = 'sqs://{access_key}:{secret_key}@'.format(
    access_key=quote(SQS['access_key'], safe=''),
    secret_key=quote(SQS['secret_key'], safe=''),
)

BROKER_TRANSPORT_OPTIONS = {
    'region': 'ca-central-1',
    'visibility_timeout': 60,  # 1 minutes
    'polling_interval': 5,     # 5 seconds
    'queue_name_prefix': 'sqs-celery-example-'
}

# CELERY namespaced
CELERY_BROKER_URL = BROKER_URL
CELERY_BROKER_TRANSPORT_OPTIONS = BROKER_TRANSPORT_OPTIONS
CELERY_TASK_DEFAULT_QUEUE = 'default'
