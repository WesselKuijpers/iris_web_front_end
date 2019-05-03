from flask import Flask, Blueprint, jsonify
from flask import render_template
import json

insight_controller = Blueprint('insight_controller', __name__)

@insight_controller.route('/')
def insight_index():
    return render_template('insight/index.html')

@insight_controller.route('/data')
def insight_data():
    with open('static/model_history/history.json', 'r') as file:
        op = json.load(file)
    return jsonify(op)