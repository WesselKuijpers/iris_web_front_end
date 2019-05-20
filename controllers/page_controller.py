from flask import Blueprint, render_template

# register blueprint
page_controller = Blueprint('page_controller', __name__)

# route: '/'
# returns: renders the 'templates/page/index.html' template
@page_controller.route('/')
def page_index():
    return render_template('page/index.html')
