import boto3
import os
import json
from botocore import errorfactory


def get_or_create_queue(name):
    stage = os.environ.get('STAGE', 'development')
    sqs = boto3.resource('sqs', region_name='eu-west-2')
    sqs_client = boto3.client('sqs', region_name='eu-west-2')
    queue_name = f'{name}-{stage}'
    try:
        return sqs.get_queue_by_name(QueueName=queue_name)
    except sqs_client.exceptions.QueueDoesNotExist:
        return sqs.create_queue(QueueName=queue_name)


def add(data):
    # Add the data packet to the correct SQS queue
    queue = get_or_create_queue('heap')
    queue.send_message(MessageBody=json.dumps(data))


def process(id):
    queue = get_or_create_queue('heap')
    m = {}
    for i in range(0, 10):
        messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=1)
        count = 0
        for message in messages:
            count += 1
            m[message.message_id] = message
        if not count:
            break
    data = [v.body for k, v in m.items()]
    for d in data:
        print('---------')
        print(d)
    for k, v in m.items():
        v.delete()
