import boto3
import os
import json
from botocore import errorfactory
from datetime import datetime, date
from decimal import Decimal
from heaptools.client import HeapAPIClient

class JsonFormatEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def get_or_create_queue(name):
    stage = os.environ.get('STAGE', 'development')
    sqs = boto3.resource('sqs', region_name='eu-west-2')
    sqs_client = boto3.client('sqs', region_name='eu-west-2')
    queue_name = f'{name}-{stage}'
    try:
        return sqs.get_queue_by_name(QueueName=queue_name)
    except sqs_client.exceptions.QueueDoesNotExist:
        return sqs.create_queue(QueueName=queue_name)


def add(identity, properties):
    # Add the data packet to the correct SQS queue
    queue = get_or_create_queue('heap')
    data = {'identity': identity,
            'properties': properties}
    queue.send_message(MessageBody=json.dumps(data, cls=JsonFormatEncoder))


def process(id):
    queue = get_or_create_queue('heap')
    client = HeapAPIClient(id)
    m = {}
    for i in range(0, 10):
        messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=1)
        count = 0
        for message in messages:
            count += 1
            m[message.message_id] = message
        if not count:
            break
    data = [json.loads(v.body) for k, v in m.items()]
    r = client.bulk_add_user_properties(data)
    if r.status_code == 200:
        for k, v in m.items():
            v.delete()
    else:
        print("HEAP Error", r.status_code, r.content)