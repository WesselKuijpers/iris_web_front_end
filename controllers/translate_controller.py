import json

from flask import Blueprint, jsonify

# register blueprint
translate_controller = Blueprint('translate_controller', __name__)


# route: '/translate/'
# returns: json data containing translation data read from the 'static/translations/translation.json' -file
@translate_controller.route('/')
def get_translations():
    with open('static/translations/translation.json', 'r', encoding='utf-8') as file:
        op = json.load(file)
    return jsonify(op)
