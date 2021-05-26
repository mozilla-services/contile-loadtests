from molotov import scenario
from aiohttp import ClientTimeout
import os
import random
import xml.etree.ElementTree as ET

_CLDR_SUBDIVISION_FILENAME = 'unicode_cldr_subdivision_codes.xml'
_TARGET_URL = os.environ.get('TARGET_URL', 'http://localhost:8000/v1/tiles')
_TEST_LOCATION_HEADER_NAME = os.environ.get(
    'TEST_LOCATION_HEADER_NAME', 'X-Test-Location')
_TEST_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/58.0.3029.110 Safari/537.36',

    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) '
    'Gecko/20100101 Firefox/53.0',

    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',

    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 '
    '(KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',

    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) '
    'AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 '
    'Mobile/14E304 Safari/602.1',

    'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G570Y Build/MMB29K) '
    'AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 '
    'Chrome/44.0.2403.133 Mobile Safari/537.36',

    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 '
    '(KHTML, like Gecko) Version/14.1 Safari/605.1.15',

    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',

    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/90.0.4430.212 Safari/537.36',

    'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko'
]
_TIMEOUT = float(os.environ.get('TIMEOUT', 5.0))


def parse_subdivision_codes_file():
    tree = ET.parse(_CLDR_SUBDIVISION_FILENAME)
    root = tree.getroot()
    subgroups = root[1]

    return subgroups


_TEST_LOCATIONS = parse_subdivision_codes_file()


@scenario()
async def request_from_consistent_location_with_consistent_user_agent(session):  # noqa: E501
    headers = {
        'User-Agent': _TEST_USER_AGENTS[0],
        _TEST_LOCATION_HEADER_NAME: 'US, USCA'
    }
    timeout = ClientTimeout(total=_TIMEOUT)

    async with session.get(_TARGET_URL,
                           headers=headers,
                           timeout=timeout) as resp:
        assert resp.status == 200


@scenario()
async def request_from_random_location_with_consistent_user_agent(session):  # noqa: 501
    headers = {
        'User-Agent': _TEST_USER_AGENTS[0],
        _TEST_LOCATION_HEADER_NAME: get_random_location()
    }
    timeout = ClientTimeout(total=_TIMEOUT)

    async with session.get(_TARGET_URL,
                           headers=headers,
                           timeout=timeout) as resp:

        assert resp.status == 200


@scenario()
async def request_from_consistent_location_with_random_user_agent(session):  # noqa: 501
    headers = {
        'User-Agent': get_random_user_agent(),
        _TEST_LOCATION_HEADER_NAME: 'US, USCA'
    }
    timeout = ClientTimeout(total=_TIMEOUT)

    async with session.get(_TARGET_URL,
                           headers=headers,
                           timeout=timeout) as resp:
        assert resp.status == 200


@scenario()
async def request_from_random_location_with_random_user_agent(session):  # noqa: 501
    headers = {
        'User-Agent': get_random_user_agent(),
        _TEST_LOCATION_HEADER_NAME: get_random_location()
    }
    timeout = ClientTimeout(total=_TIMEOUT)

    async with session.get(_TARGET_URL,
                           headers=headers,
                           timeout=timeout) as resp:
        assert resp.status == 200


def get_random_location():
    subgroup = random.choice(_TEST_LOCATIONS)
    attributes = subgroup.attrib
    code = attributes['type']
    subdivisions = attributes['contains'].split(' ')
    subdivision = random.choice(subdivisions)

    return f'{code}, {subdivision.upper()}'


def get_random_user_agent():
    return random.choice(_TEST_USER_AGENTS)
