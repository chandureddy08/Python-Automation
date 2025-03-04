import boto3
from botocore.exceptions import ClientError

def start_instances_by_tag(tags, region):
    ec2 = boto3.client("ec2", region_name = region)
    tag_filters = [
        {
            "Name": f"tag:{key}",
            "Values": [value]
        } for key, value in tags.items()
    ]
    tag_filters.append({"Name": "instance-state-name", "Values":["stopped"]})  #Includes only stopped instances

    try:
        paginator = ec2.get_paginator("describe_instances")
        page_iterator = paginator.paginate(Filters=tag_filters)

        instance = []
        for page in page_iterator:
            for reservation in page["Reservations"]:
                for instances in reservation["Instances"]:
                    instances.append(instance["InstanceId"])

        if instances:
            start_responce = ec2.start_instances(InstanceIds=instances)
            print(f"Started instances: {instances}")
            return start_responce
        else:
            print("No stopped instances found with the specific tags.")
    except ClientError as e:
        print(f"An error occured:{e}")

def lambda_handler(event,context):

    tags = {
        "Auto-instance-sheduler": "yes",
        "Environment": "Dev"
    }
    region = "us-east-1"
    start_instances_by_tag(tags, region)