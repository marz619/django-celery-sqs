# Celery-SQS

Sample [Django](https://www.djangoproject.com/) application that shows
how to use [Celery](https://docs.celeryproject.org/) with [Amazon
SQS](https://aws.amazon.com/sqs/) as the Broker.

## Quick guide

-   Python 3.7+ is **required**
-   Clone this repo
-   Create a virtualenv
-   Install requirements

``` sh
python3 -m venv celery-sqs
source celery-sqs/bin/activate
pip install -r requirements.txt
```

-   Add `celerysqs/secret.py` with the following template

    :::: note
    ::: title
    Note
    :::

    The SQS keys must have both [IAM Policies](#iam-policies) listed
    below
    ::::

``` python
KEY = "some secret key"  # for Django

SQS = {
    "access_key": "your aws_access_key",
    "secret_key": "your aws_secret_key",
}
```

### Django Commands

-   run the server

    ``` sh
    $> DJANGO_SETTINGS_MODULE=celerysqs.conf.aws python manage.py runserver
    ```

-   run the celery worker

    ``` sh
    $> DJANGO_SETTINGS_MODULE=celerysqs.conf.aws celery worker -A celerysqs --concurrency=1 -l info
    ```

-   queue some tasks

    ``` sh
    $> ./scripts/curls.sh
    ```

## IAM Policies

:::: note
::: title
Note
:::

**Both** policy types are required
::::

### (1) ListQueues (\*) {#listqueues-}

``` json
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
```

### (2) CRUD (prefix) {#crud-prefix-}

:::: note
::: title
Note
:::

\- Replace `{region}` with your AWS Region - Replace `{prefix}` desired
queue prefix
::::

``` json
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
```
