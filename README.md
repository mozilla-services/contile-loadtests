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

The load tests were written using
[Molotov](https://molotov.readthedocs.io/en/stable/) and can be started using
the following command:

```sh
$ molotov -c -v d <duration>
```

where `<duration>` is the length of time in seconds that you want the load test
to run.

Check the Molotov documentation for details on other options available to run
the tests.

```sh
$ molotov -h
```

