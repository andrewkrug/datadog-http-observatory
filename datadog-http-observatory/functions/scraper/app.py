import botocore
import boto3
import json
import re
import requests


def get_list_of_domains():
    """Return a list of domains to scan.

    Returns:
        [list]: [A list of TLDs from AWS SSM Parameter Store.]
    """
    try:
        ssm = boto3.client("ssm")
        response = ssm.get_parameter(
            Name="/datadog/observatory_scanner_domains", WithDecryption=False
        )
        return response["Parameter"]["Value"].split(",")
    except botocore.exceptions.ClientError:
        return []


def query_cert_transparency(domain):
    """Query certificate transparency service crt.sh and return JSON payload of certificates.

    Args:
        domain ([string]): [Example: datadog.com]

    Returns:
        [list]: [A list of dictionaries containing information about certificates.]
    """

    query = requests.get(
        f"https://crt.sh/?Identity={domain}&output=json&exclude=expired"
    )
    return query.json()


def extract_domains_only(certificate_transparency_list, domain):
    """Iterate over the certificate transparency json producing only domains to scan.
    Ignore wildcard certificates for now assuming that we always scan the base domain
    using www etc.

    Args:
        certificate_transparency_list ([list]): [List of dictionaries produced by calling crt.sh.]

    Returns:
        [list]: [A list of domains to scan.]
    """
    regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    domains = []
    for item in certificate_transparency_list:
        common_name = item.get("common_name")
        if re.search(regex, common_name) or common_name.find("*") != -1:
            pass
        # Opinonated choice to strip out
        elif item.get("common_name").find(domain) != -1:
            domains.append(item.get("common_name"))
        else:
            # Do nothing maybe log in the future.
            pass

    domains.append(f"www.{domain}")

    deduped = []
    [deduped.append(x) for x in domains if x not in deduped]

    return deduped


def lambda_handler(event, context):
    """Query your domain for certificates known to certificate transparency logs.

    Args:
        event ([dict]): [The standard cloudwatch event dictionary passed in.]
        context ([type]): [An empty dictionary required by AWS Lambda.]

    Returns:
        [dict]: [dictionary of the domains to store and ultimately scan.]
    """
    response = dict(scans=[])
    domains = get_list_of_domains()
    for domain in domains:
        cert_transparency = query_cert_transparency(domain)
        reduced_list = extract_domains_only(cert_transparency, domain)
        response["scans"].extend(reduced_list)
    return response
