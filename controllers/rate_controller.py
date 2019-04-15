from flask import Flask, Blueprint
from flask import render_template

rate_controller = Blueprint('rate_controller', __name__)

@rate_controller.route('/')
def rate_index():
    return render_template('rate/index.html')