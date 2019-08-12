#!/bin/bash

#export AWS_DEFAULT_PROFILE=chivay

LAMBDA_NAME=myHome20
LAMBDA_DIR=../lambda/

cd $LAMBDA_DIR
#rm *.pyc 
rm ../lambda.zip 
zip  -X -r ../lambda.zip .
cd ..
aws lambda update-function-code --region=eu-west-1 --function-name $LAMBDA_NAME --zip-file fileb://lambda.zip
                                                      
rm ./lambda.zip 

