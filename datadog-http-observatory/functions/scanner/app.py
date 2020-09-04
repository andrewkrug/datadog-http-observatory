import requests
import socket
import time

from datetime import datetime
from requests.exceptions import Timeout

HIDDEN = True
API_URL = "https://http-observatory.security.mozilla.org/api/v1"


def is_alive(domain):
    """Basic test to see if the port is even available for scanning

    Args:
        domain ([string]): [the domain we are scanning]

    Returns:
        [bool]: [Truthy]
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        result = requests.get(f"http://{domain}", timeout=5, headers=headers)

        if result.status_code in [301, 302, 200, 201, 202]:
            alive = True
        else:
            alive = False
    except Exception:
        alive = False

    return alive


def inititiate_scan(domain):
    """Initiate the observatory scan.  Scans are async and can take a while to yield a result.

    Args:
        domain ([string]): [The domain we are scanning.]

    Returns:
        [string]: [The ID of the observatory worker job to poll later on.]
    """
    if is_alive(domain):
        url = f"{API_URL}/analyze"
        result = requests.post(
            url, params={"host": f"{domain}", "hidden": HIDDEN}, timeout=1
        )

        if result.status_code == 200:
            return result.json()
        else:
            return None
    else:
        return None


def check_scan(domain):
    """Take an observatory scan id.  Return a scan result or empty.

    Args:
        scan_id ([string]): [The ID of the scan job.]

    Returns:
        [dict]: [A dictionary of information or {}]
    """
    scan_result = {}
    url = f"{API_URL}/analyze"
    result = requests.post(
        url, params={"host": f"{domain}", "hidden": HIDDEN}, timeout=1
    )
    if result.status_code == 200 and result.json().get("state") == "FINISHED":
        scan_result = result.json()

    return scan_result


def lambda_handler(event, context):
    """The event as it is passed through the step functions workflow.

    Args:
        event ([dict]): [Standard lambda event dictionary.]
        context ([dict]): [Empty dictionary.]
    """
    results = dict()
    results["in_progress"] = []
    results["complete"] = []

    for domain in event["scans"]:
        scan_id = inititiate_scan(domain)
        results["in_progress"].append(dict(id=scan_id, domain=domain))

    while len(results["in_progress"]) > 0:
        for scan in results["in_progress"]:
            result = check_scan(scan["domain"])
            if result.get("state") != "FINISHED":
                time.sleep(3)
                pass
            else:
                results["complete"].append(
                    dict(
                        date=datetime.utcnow().isoformat(),
                        domain=scan["domain"],
                        grade=result["grade"],
                        score=result["score"],
                        tests_passed=result["tests_passed"],
                        tests_failed=result["tests_failed"],
                    )
                )
                results["in_progress"].pop()
                event["in_progress"] = results["in_progress"]
                event["complete"] = [
                    i
                    for n, i in enumerate(results["complete"])
                    if i not in results["complete"][n + 1 :]
                ]
    return event
