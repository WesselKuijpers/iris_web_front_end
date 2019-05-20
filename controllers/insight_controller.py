import json

from flask import Blueprint, jsonify, render_template

# register the blueprint
insight_controller = Blueprint('insight_controller', __name__)

# route: '/insight/'
# returns: insight page
@insight_controller.route('/')
def insight_index():
    return render_template('insight/index.html')

# route: '/insight/data/history'
# returns: json, fetched from the 'static/model_history/history.json' -file
@insight_controller.route('/data/history')
def insight_data_history():
    with open('static/model_history/history.json', 'r') as file:
        op = json.load(file)
    return jsonify(op)

# route: '/insight/data/report'
# returns: json, fetched from the 'static/model_history/classification_report.json' -file
@insight_controller.route('/data/report')
def insight_data_report():
    with open('static/model_history/classification_report.json', 'r') as file:
        op = json.load(file)
    return jsonify(op)

# route: '/insight/data/confusion_matrix'
# returns: json, fetched from the 'static/model_history/confusion_matrix.json' -file
@insight_controller.route('/data/confusion_matrix')
def insight_data_confusion_matrix():
    with open('static/model_history/confusion_matrix.json', 'r') as file:
        op = json.load(file)
    return jsonify(op)

# route: '/insight/data/current_situation'
# returns: json, fetched from the 'static/model_history/situations.json' -file
@insight_controller.route('/data/current_situation')
def insight_data_current_situation():
    with open('static/model_history/situations.json', 'r') as file:
        cs = json.load(file)
    return jsonify(cs)
