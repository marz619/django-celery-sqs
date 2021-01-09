Celery-SQS
==========

A sample Django App that shows how to use Celery with Amazon SQS as the Broker.

Quick guide
-----------

-  Clone this repo
-  Create a virtualenv
-  Install requirements
-  Python 3 is **required**

.. code:: sh

   python3 -m venv celery-sqs
   source celery-sqs/bin/activate
   pip install -r requirements.txt

-  Add ``celerysqs/secret.py`` with the following template

   .. note:: the access/secret keys must have *both* IAM Policies listed below attached

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

      DJANGO_SETTINGS_MODULE=celerysqs.conf.aws python manage.py runserver

-  run the celery worker

   .. code:: sh

      DJANGO_SETTINGS_MODULE=celerysqs.conf.aws celery worker -A celerysqs --concurrency=1 -l info

-  queue some tasks

   .. code:: sh

      ./scripts/curls.sh

IAM Policy Requirements
-----------------------

.. note:: *Both are required*

.. _listqueues-:

ListQueues (*)
~~~~~~~~~~~~~~

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

CRUD (prefix-)
~~~~~~~~~~~~~~

.. note:: replace ``{region}`` and ``{prefix}`` with your amazon region, and desired prefix

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
                   "arn:aws:sqs:{region}:*:{prefix}-*"
               ]
           }
       ]
   }
