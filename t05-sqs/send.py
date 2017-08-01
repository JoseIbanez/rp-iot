import boto3

# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'https://sqs.eu-west-1.amazonaws.com/532272748741/test01'

# Send message to SQS queue
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageAttributes={
        'Title': {
            'DataType': 'String',
            'StringValue': 'The Whistler'
        },
        'Author': {
            'DataType': 'String',
            'StringValue': 'John Grisham'
        },
        'WeeksOn': {
            'DataType': 'Number',
            'StringValue': '6'
        }
    },
    MessageBody=(
        'Information about current NY Times fiction bestseller for '
        'week of 12/11/2016.'
    )
)

print(response['MessageId'])
