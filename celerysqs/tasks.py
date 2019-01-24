import logging
import random

from django.conf import settings

from .celery import app as celery_app

logger = logging.getLogger(__name__)


class ChanceException(Exception):
    def __init__(self, probability: float, failure_rate: float):
        self.probability = probability
        self.failure_rate = failure_rate

    def __repr__(self):
        return f'ChanceException({self.probability:.6f}, {self.failure_rate:.6f})'

    def __str__(self):
        return f'[ChanceException [probability={self.probability:.6f} failure_rate={self.failure_rate:.6f}]]'


@celery_app.task(bind=True, name='celerysqs.tasks.process', max_retries=3)
def process(self, task):
    if settings.DEBUG:
        logger.debug('processing task: %s', task)

    try:
        failure_rate = float(task.get('failure_rate', 1.0))
        probability = random.random()
        if probability > failure_rate:
            raise ChanceException(probability, failure_rate)
    except (TypeError, ValueError) as err:
        logger.error('Error(%s): discarding %s', str(err), task)
    except ChanceException as ce:
        logger.error('%s: requeuing task %s', str(ce), task)
        raise self.retry(exc=ce, countdown=30)
    else:
        logger.info(
            'Success: Task \'%s\' with failure_rate %.6f/%.6f',
            task.get('message', 'No Message'),
            probability, failure_rate,
        )
