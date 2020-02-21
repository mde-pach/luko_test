from flask import jsonify, make_response, abort
from app.models.letter import Letter

def get_letter(letter_id):
    letter = Letter.query.get(letter_id)
    if letter is None:
        abort(make_response(jsonify(message="Letter with id {} not found.".format(letter.id)), 404))
    return letter
