import boto3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('topic_arn')
args = parser.parse_args()

session = boto3.Session()
sns = session.client('sns')

sns.publish(
  TopicArn=args.topic_arn,
  Message='hello',
  Subject='test',
)
