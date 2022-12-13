import boto3
import json
from urllib import request


def get_stack_tags_as_dict(stackid):
    cf = boto3.client("cloudformation")
    stack = cf.describe_stacks(StackName=stackid)["Stacks"][0]
    tags = dict((t["Key"], t["Value"]) for t in stack["Tags"])
    return tags


# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-requests.html
# https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
def lambda_handler(event, context):
    print(f"Request: {event}")
    response_data = {}

    # For Delete requests, immediately send a SUCCESS response.
    if event["RequestType"] == "Delete":
        send_response(event, context, "SUCCESS", response_data)
        return

    try:
        tags = get_stack_tags_as_dict(event["StackId"])
        response_status = "SUCCESS"
        response_data = tags.copy()
        # response_data["_all"] = tags
    except Exception as e:
        response_data = {"Error": e}
        response_status = "FAILED"
        print(e)

    try:
        send_response(event, context, response_status, response_data)
        return {"statusCode": 200, "body": json.dumps(response_data)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(repr(e))}


# https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-responses.html
def send_response(event, context, response_status, response_data):
    response = dict(
        Status=response_status,
        Reason=f"Details in CloudWatch Log Stream: {context.log_stream_name}",
        PhysicalResourceId=f"{event['StackId']}-tags",
        StackId=event["StackId"],
        RequestId=event["RequestId"],
        LogicalResourceId=event["LogicalResourceId"],
        Data=response_data,
    )
    print(f"Response: {response}")

    httpreq = request.Request(
        event["ResponseURL"],
        data=json.dumps(response).encode("utf-8"),
        headers={"content-type": "application/json"},
        method="PUT",
    )
    # try:
    httpresp = request.urlopen(httpreq)
    print(httpresp)
    # except Exception as e:
    #     print(e)
    #     raise
