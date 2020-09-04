import datetime
import json
import requests
from functions.scraper import app
from mock import Mock
from mock import patch


parameter_fixture = {
    "Parameter": {
        "Name": "/datadog/observatory_scanner_domains",
        "Type": "StringList",
        "Value": "andrewkrug.com,datadog.com",
        "Version": 1,
        "LastModifiedDate": datetime.datetime(2020, 9, 2, 10, 28, 6, 568000),
        "ARN": "arn:aws:ssm:us-west-2:671642278147:parameter/datadog/observatory_scanner_domains",
        "DataType": "text",
    },
    "ResponseMetadata": {
        "RequestId": "473add88-2668-4e9c-8f0b-3a082eb5def5",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "server": "Server",
            "date": "Wed, 02 Sep 2020 17:29:04 GMT",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "273",
            "connection": "keep-alive",
            "x-amzn-requestid": "473add88-2668-4e9c-8f0b-3a082eb5def5",
        },
        "RetryAttempts": 0,
    },
}

crt_fixture = [
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "*.datadog.com",
        "name_value": "*.datadog.com",
        "id": 3154562643,
        "entry_timestamp": "2020-07-28T11:06:27.479",
        "not_before": "2020-07-25T00:00:00",
        "not_after": "2021-08-25T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "*.datadog.com",
        "name_value": "*.datadog.com",
        "id": 3137124906,
        "entry_timestamp": "2020-07-25T03:23:55.431",
        "not_before": "2020-07-25T00:00:00",
        "not_after": "2021-08-25T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "docs.datadoghq.com",
        "name_value": "docs.datadog.com",
        "id": 3073290701,
        "entry_timestamp": "2020-07-11T15:17:03.002",
        "not_before": "2020-07-09T00:00:00",
        "not_after": "2021-08-09T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "docs.datadoghq.com",
        "name_value": "docs.datadog.com",
        "id": 3063548898,
        "entry_timestamp": "2020-07-09T13:52:39.191",
        "not_before": "2020-07-09T00:00:00",
        "not_after": "2021-08-09T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "*.datadog.com",
        "name_value": "*.datadog.com",
        "id": 1805563525,
        "entry_timestamp": "2019-08-24T12:29:11.412",
        "not_before": "2019-08-22T00:00:00",
        "not_after": "2020-09-22T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "*.datadog.com",
        "name_value": "*.datadog.com",
        "id": 1796000057,
        "entry_timestamp": "2019-08-22T02:27:13.158",
        "not_before": "2019-08-22T00:00:00",
        "not_after": "2020-09-22T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "docs.datadoghq.com",
        "name_value": "docs.datadog.com",
        "id": 1706252409,
        "entry_timestamp": "2019-07-25T14:38:44.588",
        "not_before": "2019-07-23T00:00:00",
        "not_after": "2020-08-23T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "docs.datadoghq.com",
        "name_value": "docs.datadog.com",
        "id": 1699778086,
        "entry_timestamp": "2019-07-23T15:14:06.874",
        "not_before": "2019-07-23T00:00:00",
        "not_after": "2020-08-23T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "*.datadog.com",
        "name_value": "*.datadog.com",
        "id": 781620458,
        "entry_timestamp": "2018-09-23T18:35:35.238",
        "not_before": "2018-09-20T00:00:00",
        "not_after": "2019-10-20T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "*.datadog.com",
        "name_value": "*.datadog.com",
        "id": 771432758,
        "entry_timestamp": "2018-09-20T16:54:00.477",
        "not_before": "2018-09-20T00:00:00",
        "not_after": "2019-10-20T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "docs.datadoghq.com",
        "name_value": "docs.datadog.com",
        "id": 637884636,
        "entry_timestamp": "2018-08-08T18:42:28.224",
        "not_before": "2018-08-06T00:00:00",
        "not_after": "2019-09-06T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "docs.datadoghq.com",
        "name_value": "docs.datadog.com",
        "id": 635888481,
        "entry_timestamp": "2018-08-06T19:19:00.482",
        "not_before": "2018-08-06T00:00:00",
        "not_after": "2019-09-06T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "go.datadoghq.com",
        "name_value": "go.datadog.com",
        "id": 501975761,
        "entry_timestamp": "2018-06-02T06:45:37.285",
        "not_before": "2017-04-24T00:00:00",
        "not_after": "2018-05-24T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "docs.datadoghq.com",
        "name_value": "docs.datadog.com",
        "id": 184027152,
        "entry_timestamp": "2017-08-04T18:42:41.628",
        "not_before": "2017-08-02T00:00:00",
        "not_after": "2018-09-02T12:00:00",
    },
    {
        "issuer_ca_id": 9324,
        "issuer_name": "C=US, O=Amazon, OU=Server CA 1B, CN=Amazon",
        "common_name": "docs.datadoghq.com",
        "name_value": "docs.datadog.com",
        "id": 29445288,
        "entry_timestamp": "2016-08-22T11:37:42.206",
        "not_before": "2016-08-16T00:00:00",
        "not_after": "2017-09-16T12:00:00",
    },
    {
        "issuer_ca_id": 1492,
        "issuer_name": "C=US, O=GeoTrust Inc., CN=RapidSSL SHA256 CA",
        "common_name": "*.datadog.com",
        "name_value": "*.datadog.com\ndatadog.com",
        "id": 28475272,
        "entry_timestamp": "2016-08-14T11:44:06.065",
        "not_before": "2016-08-04T00:00:00",
        "not_after": "2018-10-19T23:59:59",
    },
    {
        "issuer_ca_id": 1492,
        "issuer_name": "C=US, O=GeoTrust Inc., CN=RapidSSL SHA256 CA",
        "common_name": "datadog.com",
        "name_value": "datadog.com\nwww.datadog.com",
        "id": 26854398,
        "entry_timestamp": "2016-08-04T10:22:02.382",
        "not_before": "2016-08-04T00:00:00",
        "not_after": "2019-08-04T23:59:59",
    },
    {
        "issuer_ca_id": 1492,
        "issuer_name": "C=US, O=GeoTrust Inc., CN=RapidSSL SHA256 CA",
        "common_name": "*.datadog.com",
        "name_value": "*.datadog.com\ndatadog.com",
        "id": 26853521,
        "entry_timestamp": "2016-08-04T10:00:26.916",
        "not_before": "2016-08-04T00:00:00",
        "not_after": "2018-10-19T23:59:59",
    },
    {
        "issuer_ca_id": 1558,
        "issuer_name": "C=US, O=GeoTrust Inc., CN=RapidSSL SHA256 CA - G3",
        "common_name": "*.datadog.com",
        "name_value": "*.datadog.com\ndatadog.com",
        "id": 10305556,
        "entry_timestamp": "2015-10-23T19:14:42.381",
        "not_before": "2015-10-18T19:57:01",
        "not_after": "2018-10-19T22:50:21",
    },
]


@patch("boto3.client")
def test_get_list_of_domains(mock_client):
    mock_client.return_value = mock_client
    mock_client.get_parameter.return_value = parameter_fixture
    result = app.get_list_of_domains()
    print(result)
    assert result is not None
    assert isinstance(result, list)


@patch.object(requests, "get")
def test_query_cert_transparency(mock_get):
    mock_response = Mock()
    mock_get.return_value = mock_response
    mock_response.json.return_value = crt_fixture
    result = app.query_cert_transparency("datadog.com")
    print(result)
    assert isinstance(result, list)


@patch.object(requests, "get")
def test_extract_domains_only(mock_get):
    mock_response = Mock()
    mock_get.return_value = mock_response
    mock_response.json.return_value = crt_fixture
    domains = app.query_cert_transparency("datadog.com")
    result = app.extract_domains_only(domains, "datadog.com")
    assert isinstance(result, list)
