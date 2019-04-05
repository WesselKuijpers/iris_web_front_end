from flask import Flask, Blueprint
from flask import render_template

page_controller = Blueprint('page_controller', __name__)

@page_controller.route('/')
def page_index():
    return render_template('page/index.html')
