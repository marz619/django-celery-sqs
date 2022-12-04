Celery-SQS
==========

Sample `Django`_ application that shows how to use `Celery`_ with `Amazon SQS`_
as the Broker.

.. _`Django`: https://www.djangoproject.com/
.. _`Celery`: https://docs.celeryproject.org/
.. _`Amazon SQS`: https://aws.amazon.com/sqs/


Quick guide
-----------

-  Python 3.7+ is **required**
-  Clone this repo
-  Create a virtualenv
-  Install requirements

.. code:: sh

   python3 -m venv celery-sqs
   source celery-sqs/bin/activate
   pip install -r requirements.txt

-  Add ``celerysqs/secret.py`` with the following template

   .. note:: The SQS keys must have both `IAM Policies`_ listed below

.. code:: python

   KEY = "some secret key"  # for Django

   SQS = {
       "access_key": "your aws_access_key",
       "secret_key": "your aws_secret_key",
   }

Django Commands
~~~~~~~~~~~~~~~

-  run the server

   .. code:: sh

      $> DJANGO_SETTINGS_MODULE=celerysqs.conf.aws python manage.py runserver

-  run the celery worker

   .. code:: sh

      $> DJANGO_SETTINGS_MODULE=celerysqs.conf.aws celery worker -A celerysqs --concurrency=1 -l info

-  queue some tasks

   .. code:: sh

      $> ./scripts/curls.sh


IAM Policies
------------

.. note:: **Both** policy types are required

.. _listqueues-:

(1) ListQueues (*)
~~~~~~~~~~~~~~~~~~

.. code:: json

   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "Stmt1234567890000",
               "Effect": "Allow",
               "Action": [
                   "sqs:ListQueues"
               ],
               "Resource": [
                   "*"
               ]
           }
       ]
   }

.. _crud-prefix-:

(2) CRUD (prefix)
~~~~~~~~~~~~~~~~~~

.. note::
   -  Replace ``{region}`` with your AWS Region
   -  Replace ``{prefix}`` desired queue prefix

.. code:: json

   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "Stmt1234567890000",
               "Effect": "Allow",
               "Action": [
                   "sqs:ChangeMessageVisibility",
                   "sqs:CreateQueue",
                   "sqs:DeleteMessage",
                   "sqs:DeleteQueue",
                   "sqs:GetQueueAttributes",
                   "sqs:GetQueueUrl",
                   "sqs:ReceiveMessage",
                   "sqs:SendMessage",
                   "sqs:SetQueueAttributes"
               ],
               "Resource": [
                   "arn:aws:sqs:{region}:*:{prefix}*"
               ]
           }
       ]
   }
