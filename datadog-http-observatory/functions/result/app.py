import botocore
import boto3
import requests
import time
import uuid
from datadog import initialize, api

LOG_INTAKE = "https://http-intake.logs.datadoghq.com/v1/input"


def get_datadog_api_key():
    """Return the datadog api key from an ssm parameter secure string.

    Returns:
        [list]: [A list of TLDs from AWS SSM Parameter Store.]
    """
    try:
        ssm = boto3.client("ssm")
        response = ssm.get_parameter(
            Name="/datadog/observatory_dd_api_key", WithDecryption=True
        )
        return response["Parameter"]["Value"]
    except botocore.exceptions.ClientError:
        return ""


def send_to_datadog(observatory_log, datadog_api_key):
    """Generate a payload of Datadog event data to send to the logs endpoint.

    Args:
        observatory_log ([dict]): ["Dictionary of information from the Mozilla Web Observatory"]
        datadog_api_key ([string]): ["The datadog API key that will be used to post."]

    Returns:
        [object]: ["Result of the request operation as an object."]
    """
    payload = observatory_log
    payload["event_id"] = uuid.uuid4().hex
    payload["ddsource"] = "mozilla-web-observatory"
    payload["service"] = "datadog-http-observatory"
    payload["host"] = observatory_log["domain"]
    payload[
        "ddtags"
    ] = "environment:production,origin:crt.sh,source:mozilla-web-observatory"
    payload["status"] = "INFO"

    headers = {"Content-Type": "application/json", "DD-API-KEY": datadog_api_key}
    result = requests.post(LOG_INTAKE, headers=headers, json=payload)
    return result


def update_metrics(observatory_log, datadog_api_key):
    """Send metrics to Datadog for use in dashboards.

    Args:
        observatory_log ([dict]): ["Dictionary of information from the Mozilla Web Observatory"]
        datadog_api_key ([string]): ["The datadog API key that will be used to post."]
    """
    api.Metric.send(
        metric="mozilla.observatory-scan-score",
        points=observatory_log["score"],
        host=observatory_log["domain"],
        tags=[],
    )

    api.Metric.send(
        metric="mozilla.observatory-failed-tests",
        points=observatory_log["tests_failed"],
        host=observatory_log["domain"],
        tags=[],
    )

    api.Metric.send(
        metric="mozilla.observatory-passed-tests",
        points=observatory_log["tests_passed"],
        host=observatory_log["domain"],
        tags=[],
    )


def lambda_handler(event, context):
    """The event as it is passed through the step functions workflow.

    Args:
        event ([dict]): [Standard lambda event dictionary.]
        context ([dict]): [Empty dictionary.]
    """
    datadog_api_key = get_datadog_api_key()
    options = {"api_key": datadog_api_key}
    initialize(**options)

    for observatory_log in event["complete"]:
        send_to_datadog(observatory_log, datadog_api_key)
        update_metrics(observatory_log, datadog_api_key)
