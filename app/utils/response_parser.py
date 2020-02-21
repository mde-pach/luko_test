def get_letter_status(letter_response):
    status = None
    for timeline_event in letter_response.get('shipment', {}).get('timeline', {}):
        if timeline_event.get('status', False):
            status = timeline_event.get('shortLabel')
        else:
            break
    return status
