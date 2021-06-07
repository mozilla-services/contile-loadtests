# Contile Load Tests

## Requirements:

- [Python 3.5+](https://www.python.org/downloads/)

## Installation:

```sh
$ virtualenv venv -p python3
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```

## Usage:

The load tests make use of the following environment variables:
* `TIMEOUT`: The timeout (in seconds) for the request made to Contile (defaults to 5)
* `TARGET_URL`: The URL of the endpoint to be load tested (defaults to `http://localhost:8000/v1/tiles`)
* `TEST_LOCATION_HEADER_NAME`: The of the HTTP header used to manually specify the location from which the request originated. This should match the value of CONTILE_LOCATION_TEST_HEADER on Contile (defaults to `X-Test-Location`)

The load tests were written using
[Molotov](https://molotov.readthedocs.io/en/stable/) and can be started using
the following command:

```sh
$ molotov -c -v d <duration> -s <scenario name>
```

where `<duration>` is the length of time in seconds that you want the load test
to run, and `<scenario name>` is one of the following:
* `request_from_consistent_location_with_consistent_user_agent`: Requests all originate from the same location (USCA) and have the same user agent (Google Chrome on Windows)
* `request_from_random_location_with_consistent_user_agent`: Requests originate from randomly-chosen locations but have the same user agent (Google Chrome on Windows)
* `request_from_consistent_location_with_random_user_agent`: Requests originate from the same location but have randomly-chosen user agents
* `request_from_random_location_with_random_user_agent`: Requests originate from a randomly-chosen location and have randomly-chosen user agents

Check the Molotov documentation for details on other options available to run
the tests.

```sh
$ molotov -h
```

