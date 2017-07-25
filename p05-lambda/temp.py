import logging
import boto3
import json
import decimal
import datetime



logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('Test')


def lambda_handler(event, context):
    logger.info('got event{}'.format(event))
    logger.info('SNS Message:'+event['Records'][0]['Sns']['Message']);


    line="P1,2017-02-26 12:13,23.2"
    (probe,date,temp)=line.split(",")
    date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


    response = table.put_item(
       Item={
            'date': date,
            'probe': probe,
            'temp': temp
            }
    )

    logger.info("PutItem succeeded:")
    logger.info(json.dumps(response, indent=4, cls=DecimalEncoder))




    return 'Hello World!'



# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

