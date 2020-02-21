import pytest

from app.utils.response_parser import get_letter_status


def test_empty_response():
    assert get_letter_status({}) is None

def test_empty_shipment():
    assert get_letter_status({'shipment': {}}) is None

def test_empty_timeline():
    assert get_letter_status({'shipment': {'timeline': []}}) is None

def test_timeline_first_status():
    assert get_letter_status({'shipment': {'timeline': [
        {'status': True, 'shortLabel': 'first'},
        {'status': False, 'shortLabel': 'second'}
    ]}}) is 'first'

def test_timeline_second_status():
    assert get_letter_status({'shipment': {'timeline': [
        {'status': True, 'shortLabel': 'first'},
        {'status': True, 'shortLabel': 'second'}
    ]}}) is 'second'

def test_timeline_first_event_there_is_a_third_status():
    assert get_letter_status({'shipment': {'timeline': [
        {'status': True, 'shortLabel': 'first'},
        {'status': False, 'shortLabel': 'second'},
        {'status': True, 'shortLabel': 'third'}
    ]}}) is 'first'
