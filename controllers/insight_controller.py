import json

from flask import Blueprint, jsonify, render_template

# register the blueprint
insight_controller = Blueprint('insight_controller', __name__)

# route: '/insight/'
# returns: insight page
@insight_controller.route('/')
def insight_index():
    return render_template('insight/index.html')
