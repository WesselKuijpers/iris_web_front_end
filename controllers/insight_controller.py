from flask import Flask, Blueprint
from flask import render_template

insight_controller = Blueprint('insight_controller', __name__)

@insight_controller.route('/')
def rate_index():
    return render_template('insight/index.html')