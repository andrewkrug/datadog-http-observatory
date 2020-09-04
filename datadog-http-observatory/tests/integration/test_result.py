from functions.result import app


test_event = {
    "in_progress": [],
    "complete": [
        {
            "date": "2020-09-04T00:05:05.121601",
            "domain": "home.andrewkrug.com",
            "grade": "F",
            "score": 0,
            "tests_passed": 6,
            "tests_failed": 6,
        },
        {
            "date": "2020-09-04T00:05:05.604717",
            "domain": "hope-manage-dev.andrewkrug.com",
            "grade": "D+",
            "score": 40,
            "tests_passed": 8,
            "tests_failed": 4,
        },
        {
            "date": "2020-09-04T00:05:51.660820",
            "domain": "home.andrewkrug.com",
            "grade": "F",
            "score": 0,
            "tests_passed": 6,
            "tests_failed": 6,
        },
        {
            "date": "2020-09-04T00:05:52.117428",
            "domain": "hope-manage-dev.andrewkrug.com",
            "grade": "D+",
            "score": 40,
            "tests_passed": 8,
            "tests_failed": 4,
        },
        {
            "date": "2020-09-04T00:05:52.584278",
            "domain": "www.andrewkrug.com",
            "grade": "F",
            "score": 20,
            "tests_passed": 7,
            "tests_failed": 5,
        },
        {
            "date": "2020-09-04T00:05:53.036927",
            "domain": "home.andrewkrug.com",
            "grade": "F",
            "score": 0,
            "tests_passed": 6,
            "tests_failed": 6,
        },
        {
            "date": "2020-09-04T00:05:53.506074",
            "domain": "home.andrewkrug.com",
            "grade": "F",
            "score": 0,
            "tests_passed": 6,
            "tests_failed": 6,
        },
    ],
}


def test_handler():
    app.lambda_handler(test_event, context={})
