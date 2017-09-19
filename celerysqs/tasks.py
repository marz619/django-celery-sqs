import logging
import random

from django.conf import settings

from .celery import app as celery_app

logger = logging.getLogger(__name__)


class ChanceException(Exception):
    def __init__(self, rand, chance):
        self._rand = rand
        self._chance = chance
    
    def __str__(self):
        return "ChanceException({:.6f}/{:.6f})".format(self._rand, self._chance)


@celery_app.task(bind=True, name='celerysqs.tasks.process', max_retries=3)
def process(self, task):
    if settings.DEBUG:
        logger.debug("processing task: %s", task)

    try:
        chance = float(task.get('chance', 1.0))
        rand = random.random()

        if rand < chance:
            logger.info(
                'Success: %s with chance %.6f/%.6f',
                task.get('message', 'No Message'),
                rand, chance,
            )
            return
        raise ChanceException(rand, chance)
    except (TypeError, ValueError) as err:
        logger.error('Error(%s): discarding %s', str(err), task)
    except ChanceException as ce:
        logger.error('%s: requeuing task %s', str(ce), task)
        raise self.retry(exc=ce, countdown=30)
