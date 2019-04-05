from flask import Flask, Blueprint
from flask import render_template

predict_controller = Blueprint('predict_controller', __name__)

@predict_controller.route('/')
def page_index():
    return render_template('page/index.html')