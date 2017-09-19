import json
import logging

from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .tasks import process

logger = logging.getLogger(__name__)


class TaskQueuer(View):
    @csrf_exempt
    def post(self, request: HttpRequest, *args, **kwargs):
        if settings.DEBUG:
            logger.debug('Queueing task', extra={'request': request})

        self._queue_task(request.body)
        return HttpResponse()  # empty 200 response

    def _queue_task(self, body: bytes):
        process.delay(json.loads(body.decode()))
