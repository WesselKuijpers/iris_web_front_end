from flask import Flask, Blueprint, jsonify
from flask import render_template
import json

translate_controller = Blueprint('translate_controller', __name__)

@translate_controller.route('/')
def get_translations():
    with open('static/translations/translation.json', 'r', encoding='utf-8') as file:
        op = json.load(file)
        print(op)
    return jsonify(op)