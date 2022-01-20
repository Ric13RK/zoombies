import json
import os
import boto3


# REGION = os.environ['REGION']

# FARGATE_CLUSTER = os.environ['FARGATE_CLUSTER']
# FARGATE_TASK_DEF_NAME = os.environ['FARGATE_TASK_DEF_NAME']
# FARGATE_SUBNET_ID = os.environ['FARGATE_SUBNET_ID']
# FARGATE_SEC_GROUP = os.environ['FARGATE_SEC_GROUP']
# FARGATE_CONTAINER = os.environ['FARGATE_CONTAINER']

REGION = "ap-southeast-2"
FARGATE_CLUSTER="zoombies"
FARGATE_CONTAINER="571747411449.dkr.ecr.ap-southeast-2.amazonaws.com/qna-ml-algo-x:latest"
FARGATE_SEC_GROUP="sg-08eb06c89f9de80e7"
FARGATE_SUBNET_IDS=["subnet-0a7f90b9cf3559fc4", "subnet-008faf56519281544", "subnet-0bacbf530f2eadf33"]
FARGATE_TASK_DEF_NAME="qna-ml-algo-x-task-definition:3"
REGION="ap-southeast-2"


def run_fargate_task(S3_BUCKET_NAME, S3_OBJECT_KEY):
    ecs = boto3.client('ecs', region_name=REGION)
    print("Running task.")
    response = ecs.run_task(
        cluster = FARGATE_CLUSTER,
        count = 1,
        launchType = 'FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': FARGATE_SUBNET_IDS,
                'securityGroups': [FARGATE_SEC_GROUP],
                'assignPublicIp': 'ENABLED'
            }
        },
        overrides={
            # 'containerOverrides': [
            #     {
            #         'name': FARGATE_CONTAINER,
            #         'environment': [
            #             {
            #                 'name': 'S3_BUCKET_NAME',
            #                 'value': S3_BUCKET_NAME
            #             },
            #             {
            #                 'name': 'S3_OBJECT_KEY',
            #                 'value': S3_OBJECT_KEY
            #             },
            #         ],
            #     },
            # ],
            'cpu': '4096',
            'memory': '10240',
        },

        platformVersion='LATEST',
        taskDefinition=FARGATE_TASK_DEF_NAME,
    )
    return response


if __name__ == "__main__":
    # print(json.dumps(event.get("Records")[0], indent=4, default=str))
    # s3_info = event.get("Records")[0]
    # bucket_name = s3_info.get("s3").get("bucket").get("name")
    # key = s3_info.get("s3").get("object").get("key")
    
    # add event info
    # logger.info(f"S3 event type: ${s3_info.get('eventName')}")
    # # add s3 object location
    # logger.info(f"S3 object key: ${s3_object_key}")
    
    bucket_name = "unprocessed-git-md-files-manual"
    key = "docs/amazon-application-discovery-user-guide/doc_source/agent-data-collected.md"
    print(bucket_name)
    res = run_fargate_task(bucket_name, key)
   
    print(json.dumps(res, indent=4, default=str))
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
