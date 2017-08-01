import boto3

# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'https://sqs.eu-west-1.amazonaws.com/532272748741/test01'

# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    WaitTimeSeconds=20
)

print response

try:
    message = response['Messages'][0]

except: 
    print "No message"
    quit

try:
    receipt_handle = message['ReceiptHandle']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

except: 
    print "I cannot delete message from queue"
    quit

print('Received and deleted message: %s' % message['MessageId'])
print message['Body']
