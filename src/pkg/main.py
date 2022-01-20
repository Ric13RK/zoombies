import json
import logging
import nltk
import os
from pprint import pprint
import re

from Questgen.main import QGen

import boto3
from botocore.exceptions import ClientError


qg = QGen()
logger = logging.getLogger(__name__)


def get_s3(region=None):
    """
    Get a Boto 3 Amazon S3 resource with a specific AWS Region or with your
    default AWS Region.
    """
    return boto3.resource('s3', region_name=region) if region else boto3.resource('s3')


def get_object(bucket, object_key):
    """
    Gets an object from a bucket.

    Usage is shown in usage_demo at the end of this module.

    :param bucket: The bucket that contains the object.
    :param object_key: The key of the object to retrieve.
    :return: The object data in bytes.
    """
    try:
        # s3_resource = boto3.resource('s3')
        # body = s3_resource.Object(bucket, object_key).get()['Body'].read()
        client = boto3.client('s3')
        body = client.get_object(Bucket=bucket, Key=object_key)['Body'].read()
        logger.info("Got object '%s' from bucket '%s'.", object_key, bucket)
    except ClientError:
        logger.exception(("Couldn't get object '%s' from bucket '%s'.",
                          object_key, bucket.name))
        raise
    else:
        return body


def clean_md_file(txt):
    #remove: #
    txt = txt.replace("#### ", "")
    txt = txt.replace("### ", "")
    txt = txt.replace("## ", "")
    txt = txt.replace("# ", "")

    #replace: [text](*) -> text
    found_sub = True
    while found_sub:
        sub = re.search("\[(.+?)\]\(.*?\)", txt)
        if sub:
            txt = re.sub("\[(.+?)\]\(.*?\)", sub.group(1), txt)
        else:
            found_sub = False

    #remove: <a * /a>
    txt = re.sub("\<a name=.+?\></a>","",txt)
    
    #remove: ```
    txt = txt.replace("```", "")
    
    #remove: + **
    txt = txt.replace("**", "")
    txt = txt.replace("+ **", "")
    
    #replace: \. -> .
    #replace: \( -> (
    #replace: \) -> )
    #replace: \- -> )
    txt = txt.replace("\\", "")
    
    #replace: _*text* -> _text

    #replace \n\n -> \n
    txt =txt.replace("\n\n", "\n")
    
    return txt


def get_tag(object_key):
    tag = object_key.split('/')[0]

    return tag.replace("amazon", "").replace("developer-guide", "").replace("user-guide", "").replace("admin-guide", "").replace("-doc", "").replace("developer-guide", "").replace("-", "")


def transform_ml_inference(inference, tag):
    # more options = i.get("extra_options")
    # context = i.get("context")
    return [
        {
            "question": i.get("question_statement"),
            "correct_answer": i.get("answer"),
            "incorrect_answer": i.get("options"),
            "tags": [tag]
        } for i in inference.get("questions")
    ]
    

def get_inference(payload):
    return qg.predict_mcq({ "input_text": payload })
    

if __name__ == "__main__":
    bucket = os.getenv("S3_BUCKET_NAME", None)
    key = os.getenv("S3_OBJECT_KEY", None)

    # don't proceed if key contain "*-examples/"
    if bucket and key and "-examples/" not in key:
        line_body = get_object(bucket, key)
        text = clean_md_file(line_body.decode("utf-8"))
        print(f"Got object with key {key} and body:")

        inference = get_inference(text)
        print(json.dumps(inference, indent=4, default=str))

        qna = transform_ml_inference(inference, get_tag(key))
        print(json.dumps(qna, indent=4, default=str))