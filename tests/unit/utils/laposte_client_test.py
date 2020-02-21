import pytest
import requests

from app.utils.rest_client import SimpleLaposteClient

def test_header_presence(requests_mock):
    client = SimpleLaposteClient('https://TEST_URL.test')
    client.headers = {'should be': 'here'}

    requests_mock.get('https://TEST_URL.test/test_resource')
    res = client.get('test_resource')

    assert res.request.headers['should be'] == 'here'

def test_get_the_response(requests_mock):
    client = SimpleLaposteClient('https://TEST_URL.test')
    client.headers = {'should be': 'here'}

    requests_mock.get('https://TEST_URL.test/test_resource', text='{"message": "hello"}')
    res = client.get('test_resource')

    assert res.json() == {"message": "hello"}

def test_raise_if_error(requests_mock):
    client = SimpleLaposteClient('https://TEST_URL.test')
    client.headers = {'should be': 'here'}

    requests_mock.get('https://TEST_URL.test/test_resource', text='missing', status_code=404)

    with pytest.raises(requests.exceptions.HTTPError):
        res = client.get('test_resource')
