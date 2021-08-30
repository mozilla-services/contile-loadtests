from molotov import scenario
from aiohttp import ClientTimeout
import os
import random
import xml.etree.ElementTree as ET

_CLDR_SUBDIVISION_FILENAME = 'unicode_cldr_subdivision_codes.xml'
_TARGET_URL = os.environ.get('TARGET_URL', 'http://localhost:8000/v1/tiles')
_TEST_LOCATION_HEADER_NAME = os.environ.get(
    'TEST_LOCATION_HEADER_NAME', 'X-Test-Location')
_TEST_FIREFOX_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; rv:10.0) Gecko/20100101 Firefox/91.0',

    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:10.0) Gecko/20100101 '
    'Firefox/91.0',

    'Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (Android 11; Mobile; rv:92.0) Gecko/92.0 Firefox/92.0',
    'Mozilla/5.0 (Android; Tablet; rv:92.0) Gecko/92.0 Firefox/92.0',

    'Mozilla/5.0 (iPod touch; CPU iPhone OS 8_3 like Mac OS X) '
    'AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 Mobile/12F69 '
    'Safari/600.1.4',

    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_5_1 like Mac OS X) '
    'AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/35.0 Mobile/15E148 '
    'Safari/605.1.15',

    'Mozilla/5.0 (iPad; CPU iPhone OS 8_3 like Mac OS X) '
    'AppleWebKit/600.1.4 (KHTML, like Gecko) FxiOS/1.0 '
    'Mobile/12F69 Safari/600.1.4'
]
_TEST_NON_FIREFOX_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/58.0.3029.110 Safari/537.36',

    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 '
    '(KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',

    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) '
    'AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 '
    'Safari/602.1',

    'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G570Y Build/MMB29K) '
    'AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 '
    'Chrome/44.0.2403.133 Mobile Safari/537.36',

    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 '
    '(KHTML, like Gecko) Version/14.1 Safari/605.1.15',

    'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile '
    'Safari/537.36',

    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) '
    'AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 '
    'Mobile/15E148 Safari/605.1',

    'Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 '
    'Safari/537.36',

    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
    'like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',

    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like '
    'Gecko) Chrome/51.0.2704.64 Safari/537.36'
]
_TIMEOUT = float(os.environ.get('TIMEOUT', 5.0))


def parse_subdivision_codes_file():
    tree = ET.parse(_CLDR_SUBDIVISION_FILENAME)
    root = tree.getroot()
    subgroups = root[1]

    return subgroups


_TEST_LOCATIONS = parse_subdivision_codes_file()


@scenario()
async def request_from_consistent_location_with_consistent_firefox_user_agent(session):  # noqa: E501
    headers = {
        'User-Agent': _TEST_FIREFOX_USER_AGENTS[0],
        _TEST_LOCATION_HEADER_NAME: 'US, USCA'
    }
    timeout = ClientTimeout(total=_TIMEOUT)

    async with session.get(_TARGET_URL,
                           headers=headers,
                           timeout=timeout) as resp:
        assert resp.status in (200, 204), resp.status


@scenario()
async def request_from_random_location_with_consistent_firefox_user_agent(session):  # noqa: E501
    headers = {
        'User-Agent': _TEST_FIREFOX_USER_AGENTS[0],
        _TEST_LOCATION_HEADER_NAME: get_random_location()
    }
    timeout = ClientTimeout(total=_TIMEOUT)

    async with session.get(_TARGET_URL,
                           headers=headers,
                           timeout=timeout) as resp:
        assert resp.status in (200, 204), resp.status


@scenario()
async def request_from_consistent_location_with_random_firefox_user_agent(session):  # noqa: E501
    headers = {
        'User-Agent': random.choice(_TEST_FIREFOX_USER_AGENTS),
        _TEST_LOCATION_HEADER_NAME: 'US, USCA'
    }
    timeout = ClientTimeout(total=_TIMEOUT)

    async with session.get(_TARGET_URL,
                           headers=headers,
                           timeout=timeout) as resp:
        assert resp.status in (200, 204), resp.status


@scenario()
async def request_from_random_location_with_random_firefox_user_agent(session):
    headers = {
        'User-Agent': random.choice(_TEST_FIREFOX_USER_AGENTS),
        _TEST_LOCATION_HEADER_NAME: get_random_location()
    }
    timeout = ClientTimeout(total=_TIMEOUT)

    async with session.get(_TARGET_URL,
                           headers=headers,
                           timeout=timeout) as resp:
        assert resp.status in (200, 204), resp.status


@scenario()
async def request_with_random_non_firefox_user_agent(session):
    user_agent = random.choice(_TEST_NON_FIREFOX_USER_AGENTS)
    headers = {'User-Agent': user_agent}
    timeout = ClientTimeout(total=_TIMEOUT)

    async with session.get(_TARGET_URL,
                           headers=headers,
                           timeout=timeout) as resp:
        # Contile should send an empty response to a request from a non-Firefox
        # user agent
        assert resp.status == 403


def get_random_location():
    subgroup = random.choice(_TEST_LOCATIONS)
    attributes = subgroup.attrib
    code = attributes['type']
    subdivisions = attributes['contains'].split(' ')
    subdivision = random.choice(subdivisions)

    return f'{code}, {subdivision.upper()}'
