import json
import pymysql
import sys
import uuid
import boto3
import base64
from botocore.exceptions import ClientError

# Read config json file for config parameters
with open("config.json", "r") as jsonfile:
    config_data = json.load(jsonfile)
    print("Config data read successful")
print("configdata:",config_data)


# Get secrets
def get_secret():
    secret_name = config_data["rdssecretName"]
    region_name = config_data["region"]

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return secret

db_host=config_data["dbhost"]
db_name=config_data["dbname"]
table_name=config_data["tablename"]

secret = get_secret()
secret_json=json.loads(secret)
db_user = secret_json["username"]
db_pass = secret_json["password"]

def lambda_handler(event, context):
    
    uid = str(uuid.uuid4())
    data = json.loads(event["body"])
    data['id']=uid
    tags = data["tags"]
    
    try:
        with pymysql.connect(
                          host=db_host,
                          user=db_user,
                          passwd=db_pass,
                          db=db_name,
                          connect_timeout=5,
                          cursorclass=pymysql.cursors.DictCursor) as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `"+table_name+"` (`id`, `question`,`tags`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (uid, json.dumps(data), json.dumps(tags)))
            connection.commit()
    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Credentials': 'true',
                'Content-Type': 'application/json'
            },
            'body': "Please check the query and data"
        }
    else:
        print("Inserted into database")
    finally:
        cursor.close()
       
    return {
        'statusCode': 201,
        'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Credentials': 'true',
                'Content-Type': 'application/json'
            },
            'body': "Success"
    }


