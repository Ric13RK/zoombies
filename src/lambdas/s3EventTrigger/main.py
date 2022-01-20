import json
import logging
import os
import boto3


REGION = os.environ['REGION']

FARGATE_CLUSTER = os.environ['FARGATE_CLUSTER']
FARGATE_TASK_DEF_NAME = os.environ['FARGATE_TASK_DEF_NAME']
FARGATE_SUBNET_ID = os.environ['FARGATE_SUBNET_ID']
FARGATE_SEC_GROUP = os.environ['FARGATE_SEC_GROUP']
FARGATE_CONTAINER = os.environ['FARGATE_CONTAINER']


logger = logging.getLogger(__name__)


def run_fargate_task(S3_OBJECT_KEY):
    client = boto3.client('ecs', region_name=REGION)
    logger.info(f"Running '${FARGATE_TASK_DEF_NAME}' Fargate task in '${FARGATE_CLUSTER}' cluster")
    response = client.run_task(
        cluster=FARGATE_CLUSTER,
        launchType = 'FARGATE',
        taskDefinition=FARGATE_TASK_DEF_NAME,
        count = 1,
        platformVersion='LATEST',
        networkConfiguration={
            'awsvpcConfiguration': {
                # 'subnets': [FARGATE_SUBNET_ID,],
                # 'securityGroups': [FARGATE_SEC_GROUP],
                'assignPublicIp': 'DISABLED'
            }
        },
        overrides={
            'containerOverrides': [
                {
                    'name': FARGATE_CONTAINER,
                    'environment': [
                        {
                            'name': 'S3_OBJECT_KEY',
                            'value': S3_OBJECT_KEY
                        },
                    ],
                },
            ],
        },
        tags=[
            {
                'key': 'Team',
                'value': 'Zoombies'
            },
            {
                'key': 'CreatedBy',
                'value': 'Rishi'
            },
        ]
    )
    return str(response)


def lambda_handler(event, context):
    print(json.dumps(event.get("Records")[0], indent=4, default=str))
    s3_info = event.get("Records")[0]
    bucket_name = s3_info.get("s3").get("bucket").get("name")
    key = s3_info.get("s3").get("object").get("key")
    
    s3_object_key = "s3://" + bucket_name + "/" + key
    
    # add event info
    logger.info(f"S3 event type: ${s3_info.get('eventName')}")
    # add s3 object location
    logger.info(f"S3 object key: ${s3_object_key}")
    res = run_fargate_task(s3_object_key)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
