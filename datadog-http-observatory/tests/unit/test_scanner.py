import requests
from mock import Mock
from mock import patch

from functions.scanner import app


sample_pending_scan = {
    "algorithm_version": 2,
    "end_time": None,
    "grade": None,
    "hidden": False,
    "likelihood_indicator": None,
    "response_headers": None,
    "scan_id": 15549700,
    "score": None,
    "start_time": "Thu, 03 Sep 2020 15:08:48 GMT",
    "state": "PENDING",
    "status_code": None,
    "tests_failed": 0,
    "tests_passed": 0,
    "tests_quantity": 12,
}

sample_complete_scan = {
    "algorithm_version": 2,
    "end_time": "Thu, 03 Sep 2020 15:08:53 GMT",
    "grade": "B",
    "hidden": False,
    "likelihood_indicator": "MEDIUM",
    "response_headers": {},
    "scan_id": 15549700,
    "score": 75,
    "start_time": "Thu, 03 Sep 2020 15:08:48 GMT",
    "state": "FINISHED",
    "status_code": 200,
    "tests_failed": 2,
    "tests_passed": 10,
    "tests_quantity": 12,
}


@patch.object(requests, "post")
def test_initiate_scan(mock_post):
    mock_response = Mock()
    mock_post.return_value = mock_response
    mock_response.json.return_value = sample_pending_scan
    mock_response.status_code = 200

    result = app.inititiate_scan("www.datadog.com")
    assert result is not None

    mock_response.status_code = 500
    result = app.inititiate_scan("www.datadog.com")
    assert result is None


@patch.object(requests, "post")
def test_check_scan(mock_post):
    mock_response = Mock()
    mock_post.return_value = mock_response
    mock_response.json.return_value = sample_complete_scan
    mock_response.status_code = 200
    result = app.check_scan("www.datadog.com")
    assert result["grade"] is "B"

    mock_post.return_value = mock_response
    mock_response.json.return_value = sample_pending_scan
    mock_response.status_code = 200
    result = app.check_scan("www.datadog.com")
    assert result == {}


def test_lambda_handler():
    # Domain list for this test is random from alexa top 100 plus some others.
    event = {
        "scans": [
            "www.datadog.com",
            "andrewkrug.com",
            "mozilla.org",
            "netflix.com",
            "okezone.com",
        ]
    }
    result = app.lambda_handler(event, context={})
