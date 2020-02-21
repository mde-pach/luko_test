from flask import Blueprint, request, jsonify, make_response
from app import app
from flask_cors import CORS

from app.models.letter import Letter
from app.utils.rest_client import SimpleLaposteClient


v1 = Blueprint("v1", __name__)
CORS(v1)

laposte_client = SimpleLaposteClient(app.config['LAPOSTE_API_BASE_URL'])    
laposte_client.headers = {
    'X-Okapi-Key': app.config['LAPOSTE_API_KEY'],
    'Accept': 'application/json'
}


def get_letter(letter_id):
    letter = Letter.query.get(letter_id)
    if letter is None:
        abort(make_response(jsonify(message="Letter with id {} not found.".format(letter.id)), 404))
    return letter

def get_letter_status_from_response(letter_response):
    status = None
    for timeline_event in letter_response.get('shipment', {}).get('timeline', {}):
        if timeline_event.get('status', False):
            status = timeline_event.get('shortLabel')
        else:
            break
    return status

@v1.route('/ping', methods=['GET'])
def ep_ping():
    return "pong", 200

@v1.route('/letters', methods=['GET', 'POST'])
def letters():
    if request.method == 'GET':
        return make_response(jsonify([letter.serialize() for letter in Letter.query.all()]), 200)
    elif request.method == 'POST':
        letter = Letter()
        letter.add()
        return "All done : letter object {} has been created".format(letter.id), 200

@v1.route('/letters/<int:letter_id>', methods=['GET'])
def specific_letter_get(letter_id):
    letter = get_letter(letter_id)
    return make_response(jsonify(letter.serialize()), 200)

@v1.route('/letters/<int:letter_id>/status', methods=['PATCH'])
def specific_letter_status_update(letter_id):
    letter = get_letter(letter_id)
    res = laposte_client.get(letter.tracking_number)
    letter.status = get_letter_status_from_response(res.json())
    letter.update()
    return "Status of letter with id {} correctly updated".format(letter.id), 204

@v1.route('/letters/status', methods=['PATCH'])
def letters_status_update():
    letters = Letter.query.all()
    for letter in letters:
        try:
            res = laposte_client.get(letter.tracking_number)
        except:
            continue
        letter.status = get_letter_status_from_response(res.json())
        letter.update()

    return "All letter status are updated", 204

